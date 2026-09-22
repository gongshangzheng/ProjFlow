#!/usr/bin/env node
// 构建期把 management/docs/ 编译为前端可读的静态数据（web/public/docs-data.json）。
//
// 为什么在这里生成：静态托管（GitHub Pages 等）上没有 FastAPI。文档页在生产构建里
// 改读这份数据；本地开发仍走后端 API（见 web/src/api/docs.js）。
//
// 字段与排序逐项复刻 server/routers/management.py：
//   - 列表项 slug/title/author/date/tags/summary/id/order
//   - 详情项另加 content（去 frontmatter 的正文）与 sidecar
//   - 排序链：文件夹优先级(DOCS_FOLDER_ORDER) → order → id → date 降序 → slug
//   - 扫描跳过下划线前缀目录（_assets/ 等）
//
// frontmatter 只支持本仓库实际用到的 YAML 子集（单行 key: value / 内联数组 / 数字）。
// 遇到不支持的写法直接报错退出，绝不静默产出缺字段的数据。

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { basename, dirname, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const WEB_DIR = resolve(__dirname, '..')
const REPO_ROOT = resolve(WEB_DIR, '..')
const DOCS_DIR = join(REPO_ROOT, 'management', 'docs')
const CONFIG_FILE = join(REPO_ROOT, 'server', 'config.py')
const OUT_FILE = join(WEB_DIR, 'public', 'docs-data.json')
const ASSETS_SRC = join(DOCS_DIR, '_assets')
const ASSETS_OUT = join(WEB_DIR, 'public', 'docs-assets')

function fail(message) {
  console.error(`[build-docs-data] ${message}`)
  process.exit(1)
}

/** 从 server/config.py 读取 DOCS_FOLDER_ORDER 的字面量，保持与后端同一事实来源。 */
function readFolderOrder() {
  if (!existsSync(CONFIG_FILE)) fail(`找不到 ${relative(REPO_ROOT, CONFIG_FILE)}`)
  const source = readFileSync(CONFIG_FILE, 'utf8')
  const matched = source.match(/^\s*DOCS_FOLDER_ORDER\s*=\s*\[([^\]]*)\]/m)
  if (!matched) fail(`在 ${relative(REPO_ROOT, CONFIG_FILE)} 中找不到 DOCS_FOLDER_ORDER = [...]`)
  return matched[1]
    .split(',')
    .map((item) => item.trim().replace(/^['"]|['"]$/g, ''))
    .filter((item) => item.length > 0)
}

function walkMarkdown(dir) {
  const found = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    // 下划线前缀目录存放资产（_assets/ 等），与后端扫描行为一致
    if (entry.isDirectory()) {
      if (entry.name.startsWith('_')) continue
      found.push(...walkMarkdown(join(dir, entry.name)))
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      found.push(join(dir, entry.name))
    }
  }
  return found
}

/** 统计目录下的文件数（忽略点文件，如 .gitkeep）。 */
function countFiles(dir) {
  let count = 0
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) count += countFiles(join(dir, entry.name))
    else if (entry.isFile() && !entry.name.startsWith('.')) count += 1
  }
  return count
}

/**
 * 把 management/docs/_assets/ 整树复制到 web/public/docs-assets/。
 * 先清空目标：静态托管产物是「本次构建的完整快照」，残留旧图会让已删除的图仍可访问。
 * 源目录不存在时跳过（构建照常成功）。
 */
function syncAssets() {
  rmSync(ASSETS_OUT, { recursive: true, force: true })
  if (!existsSync(ASSETS_SRC)) return 0
  // 跳过点文件（.gitkeep 等占位文件），与 assetCount 的口径一致
  cpSync(ASSETS_SRC, ASSETS_OUT, { recursive: true, filter: (src) => !basename(src).startsWith('.') })
  return countFiles(ASSETS_OUT)
}

function unquote(value) {
  const s = value.trim()
  if (s.length >= 2) {
    const first = s[0]
    const last = s[s.length - 1]
    if ((first === '"' && last === '"') || (first === "'" && last === "'")) return s.slice(1, -1)
  }
  return s
}

function parseScalar(raw) {
  const v = raw.trim()
  if (v === '') return ''
  if (v.startsWith('[') && v.endsWith(']')) {
    const inner = v.slice(1, -1).trim()
    if (!inner) return []
    return inner.split(',').map((item) => unquote(item))
  }
  if (/^-?\d+$/.test(v)) return Number(v)
  if (/^-?\d+\.\d+$/.test(v)) return Number(v)
  return unquote(v)
}

/** 返回 [meta, body]；body 切法与后端 _parse_frontmatter 一致。 */
function parseFrontmatter(content, file) {
  if (!content.startsWith('---')) return [{}, content]
  const end = content.indexOf('---', 3)
  if (end < 0) fail(`${file}: frontmatter 起始 --- 之后没有结束 ---`)
  const head = content.slice(3, end).split('\n')
  const meta = {}
  head.forEach((line, index) => {
    if (!line.trim()) return
    if (/^\s*#/.test(line)) return
    if (/^\s/.test(line)) {
      fail(`${file}:${index + 2} frontmatter 不支持缩进/多行（仅支持单行 key: value）：${line}`)
    }
    const matched = line.match(/^([A-Za-z0-9_-]+):\s?(.*)$/)
    if (!matched) fail(`${file}:${index + 2} 无法解析的 frontmatter 行：${line}`)
    meta[matched[1]] = parseScalar(matched[2])
  })
  return [meta, content.slice(end + 3).trim()]
}

/** 与后端 _doc_number 一致：数字或数字字符串 → Number，其余 → Infinity（排最后）。 */
function docNumber(value) {
  if (value === null || value === undefined || value === '') return Infinity
  if (typeof value === 'number') return Number.isFinite(value) ? value : Infinity
  if (typeof value === 'boolean') return Infinity
  const text = String(value)
  return /^-?\d+(\.\d+)?$/.test(text) ? Number(text) : Infinity
}

/** 与后端 _doc_date_ordinal 一致：ISO 日期 → 时间戳；非法/缺失 → 0。 */
function dateOrdinal(value) {
  if (!value) return 0
  const stamp = Date.parse(String(value).slice(0, 10))
  return Number.isNaN(stamp) ? 0 : stamp
}

/** 显式比较：不能用 a - b 的真假判断（Infinity - Infinity = NaN 会被当成 0）。 */
function cmp(a, b) {
  if (a === b) return 0
  return a < b ? -1 : 1
}

function main() {
  if (!existsSync(DOCS_DIR)) fail(`找不到文档目录：${DOCS_DIR}`)
  const folderOrder = readFolderOrder()
  const files = walkMarkdown(DOCS_DIR)
  if (!files.length) fail(`文档目录中没有 .md 文件：${DOCS_DIR}`)

  const docs = []
  const details = {}

  for (const file of files.sort()) {
    const raw = readFileSync(file, 'utf8')
    const [meta, body] = parseFrontmatter(raw, relative(REPO_ROOT, file))
    const slug = relative(DOCS_DIR, file).split(sep).join('/').replace(/\.md$/, '')

    const base = {
      slug,
      title: meta.title ?? slug,
      author: meta.author ?? '',
      date: meta.date === undefined || meta.date === null ? '' : String(meta.date),
      tags: Array.isArray(meta.tags) ? meta.tags : [],
      summary: meta.summary ?? '',
      id: meta.id ?? null,
      order: meta.order ?? null,
    }

    let sidecar = {}
    const sidecarFile = file.replace(/\.md$/, '.json')
    if (existsSync(sidecarFile)) {
      try {
        sidecar = JSON.parse(readFileSync(sidecarFile, 'utf8') || '{}')
      } catch (error) {
        fail(`${relative(REPO_ROOT, sidecarFile)} 不是合法 JSON：${error.message}`)
      }
    }

    docs.push(base)
    details[slug] = { ...base, content: body, sidecar }
  }

  const folderRank = (doc) => {
    const top = doc.slug.includes('/') ? doc.slug.split('/')[0] : ''
    const index = folderOrder.indexOf(top)
    return index === -1 ? folderOrder.length : index
  }

  // 复刻 _doc_sort_key：文件夹优先级 → order → id → date 降序 → slug
  docs.sort((a, b) =>
    cmp(folderRank(a), folderRank(b)) ||
    cmp(docNumber(a.order), docNumber(b.order)) ||
    cmp(docNumber(a.id), docNumber(b.id)) ||
    cmp(dateOrdinal(b.date), dateOrdinal(a.date)) ||
    cmp(a.slug, b.slug),
  )

  const orderedDetails = {}
  for (const doc of docs) orderedDetails[doc.slug] = details[doc.slug]

  const assetCount = syncAssets()

  mkdirSync(dirname(OUT_FILE), { recursive: true })
  writeFileSync(
    OUT_FILE,
    JSON.stringify(
      { generatedAt: new Date().toISOString(), folderOrder, assetCount, docs, details: orderedDetails },
      null,
      2,
    ) + '\n',
    'utf8',
  )

  console.log(`[build-docs-data] ${docs.length} 篇文档、${assetCount} 个图像资产 → ${relative(REPO_ROOT, OUT_FILE)}`)
}

main()
