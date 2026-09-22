<template>
  <div class="markdown-body" ref="containerRef" v-html="rendered" @click="handleClick"></div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownIt from 'markdown-it'
import checkbox from 'markdown-it-task-checkbox'
import { slugify } from '../../utils/markdown'
import mermaid from 'mermaid'
import * as katexPluginModule from '@vscode/markdown-it-katex'
import 'katex/dist/katex.min.css'
import { useThemeStore } from '../../stores/theme'

const props = defineProps({
  content: { type: String, default: '' },
})

const containerRef = ref(null)
const themeStore = useThemeStore()
const router = useRouter()

function handleClick(e) {
  const anchor = e.target.closest('a')
  if (!anchor) return
  const href = anchor.getAttribute('href')
  if (!href) return
  // 文内锚点：按 id 找到标题并平滑滚动，与右侧 TOC 行为一致（不改 URL）
  if (href.startsWith('#')) {
    e.preventDefault()
    const el = document.getElementById(decodeURIComponent(href.slice(1)))
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    return
  }
  if (href.startsWith('/management/')) {
    e.preventDefault()
    router.push(href)
  }
}

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true,
})
  .use(checkbox, {
    disabled: true,
    divWrap: false,
    liClass: 'task-list-item',
  })

// `@vscode/markdown-it-katex` 是 CJS（`exports.default = fn`）：
//   dev（esbuild 预打包）→ 默认导出是**命名空间对象** `{ default: fn }`
//   build（Rollup）      → 默认导出直接是函数
// 这里归一化一次，否则 dev 下 `md.use()` 拿到对象会抛错、整块正文渲染失败。
const katexPlugin = typeof katexPluginModule.default === 'function'
  ? katexPluginModule.default
  : katexPluginModule.default?.default

if (typeof katexPlugin === 'function') {
  // LaTeX 数学：`$...$` 行内、`$$...$$` 块级 → KaTeX
  // （katex.css 由本文件顶部引入；Mermaid 图内的 $$ 公式也依赖这份样式）
  md.use(katexPlugin, { throwOnError: false })
  guardInlineMathDelimiter()
} else {
  console.error('[MarkdownRenderer] KaTeX 插件加载异常，公式将按原文显示')
}

// 插件的行内规则只校验「闭定界符之后是非单词字符」，不校验内容首尾空白，
// 于是「价格从 $5 到 $10 不等」里的 `$10 不等，还有 $` 会被当成公式（内容首尾带空白）。
// 这里补上标准守卫（GitHub / KaTeX auto-render 同款）：内容首尾不得为空白；
// 不满足时回滚该 token 与位置，交回后续规则按普通文本处理。
function guardInlineMathDelimiter() {
  const rules = md.inline.ruler.__rules__
  const original = rules?.find((r) => r.name === 'math_inline')?.fn
  if (typeof original !== 'function') {
    console.warn('[MarkdownRenderer] 未找到 math_inline 规则，跳过美元符号守卫')
    return
  }
  md.inline.ruler.at('math_inline', (state, silent) => {
    const startPos = state.pos
    const tokensBefore = state.tokens.length
    if (!original(state, silent)) return false
    if (silent) return true
    const token = state.tokens[state.tokens.length - 1]
    const isMath = token && token.type === 'math_inline'
    if (isMath && /^\s|\s$/.test(token.content)) {
      state.tokens.length = tokensBefore
      state.pos = startPos
      return false
    }
    return true
  })
}

// Heading auto-ID
const defaultHeadingRender = md.renderer.rules.heading_open ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const nextToken = tokens[idx + 1]
  if (nextToken && nextToken.children) {
    const text = nextToken.children
      .filter(t => t.type === 'text' || t.type === 'code_inline')
      .map(t => t.content)
      .join('')
    if (text) {
      token.attrSet('id', slugify(text))
    }
  }
  return defaultHeadingRender(tokens, idx, options, env, self)
}

// Mermaid code block: render as <pre class="mermaid"> instead of <pre><code>
const defaultFence = md.renderer.rules.fence ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

md.renderer.rules.fence = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const info = token.info ? token.info.trim() : ''
  if (info === 'mermaid') {
    const escaped = md.utils.escapeHtml(token.content)
    return `<pre class="mermaid">${escaped}</pre>\n`
  }
  return defaultFence(tokens, idx, options, env, self)
}

// Image: 统一输出 <img loading="lazy">；图题由所在段落的 figure 包装负责（见下）
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx]
  const src = md.utils.escapeHtml(token.attrGet('src') || '')
  const alt = md.utils.escapeHtml(token.content || '')
  const title = token.attrGet('title')
  const titleAttr = title ? ` title="${md.utils.escapeHtml(title)}"` : ''
  return `<img src="${src}" alt="${alt}" loading="lazy"${titleAttr}>`
}

// 整段只有一张带 alt 的图 → 包装为语义化 figure，alt 兼作图题
const defaultParagraphOpen = md.renderer.rules.paragraph_open ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }
const defaultParagraphClose = md.renderer.rules.paragraph_close ||
  function (tokens, idx, options, env, self) { return self.renderToken(tokens, idx, options) }

function loneFigureImage(tokens, idx) {
  const inline = tokens[idx + 1]
  if (!inline || inline.type !== 'inline' || !Array.isArray(inline.children)) return null
  // 忽略纯空白文本节点（breaks:true 下可能残留）
  const kids = inline.children.filter(t => !(t.type === 'text' && !t.content.trim()))
  if (kids.length !== 1) return null
  const only = kids[0]
  if (only.type !== 'image' || !only.content) return null
  return only
}

md.renderer.rules.paragraph_open = function (tokens, idx, options, env, self) {
  const img = loneFigureImage(tokens, idx)
  if (img) {
    env.__figureAlt = img.content
    return '<figure>'
  }
  return defaultParagraphOpen(tokens, idx, options, env, self)
}

md.renderer.rules.paragraph_close = function (tokens, idx, options, env, self) {
  if (env && env.__figureAlt) {
    const alt = md.utils.escapeHtml(env.__figureAlt)
    delete env.__figureAlt
    return `<figcaption>${alt}</figcaption></figure>`
  }
  return defaultParagraphClose(tokens, idx, options, env, self)
}

const rendered = computed(() => {
  if (!props.content) return '<p class="text-light">暂无内容</p>'
  let src = props.content
  // Task links: [[proj#t2-3]] or [[proj#t2-3|display]] → project tree with task selected
  src = src.replace(/\[\[([^#|\]]+)#([^|\]]+)\|([^\]]+)\]\]/g, (_, proj, task, text) =>
    `[${text.trim()}](/management/projects?slug=${proj.trim()}&task=${task.trim()})`)
  src = src.replace(/\[\[([^#|\]]+)#([^|\]]+)\]\]/g, (_, proj, task) =>
    `[${proj.trim()}/${task.trim()}](/management/projects?slug=${proj.trim()}&task=${task.trim()})`)
  // Doc links: [[slug]] or [[slug|display]] → doc detail page
  src = src.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, slug, text) => `[${text.trim()}](/management/docs/${slug.trim()})`)
  src = src.replace(/\[\[([^\]]+)\]\]/g, (_, slug) => `[${slug.trim()}](/management/docs/${slug.trim()})`)
  return md.render(src)
})

async function renderMermaid() {
  if (!containerRef.value) return
  const nodes = containerRef.value.querySelectorAll('pre.mermaid')
  if (!nodes.length) return

  for (const node of nodes) {
    if (!node.dataset.source) {
      node.dataset.source = node.textContent
    } else {
      node.textContent = node.dataset.source
      node.removeAttribute('data-processed')
    }
    const svgEl = node.querySelector('svg')
    if (svgEl) svgEl.remove()
  }

  try {
    mermaid.initialize({
      startOnLoad: false,
      theme: themeStore.isDark ? 'dark' : 'default',
      securityLevel: 'loose',
      fontFamily: 'system-ui, sans-serif',
    })
    await mermaid.run({ nodes: Array.from(nodes) })
  } catch (e) {
    console.warn('Mermaid render error:', e)
  }
}

watch(
  [rendered, () => themeStore.isDark],
  async () => {
    await nextTick()
    await renderMermaid()
  },
  { immediate: true }
)
</script>

<style scoped lang="scss">
.markdown-body {
  :deep(h1),
  :deep(h2),
  :deep(h3),
  :deep(h4) {
    scroll-margin-top: 4rem;
  }

  :deep(.task-list-item) {
    list-style: none;
    margin-left: -20px;
  }
  :deep(.task-list-item input[type='checkbox']) {
    margin-right: 8px;
    transform: translateY(1px);
    accent-color: var(--color-primary);
    width: 14px;
    height: 14px;
    cursor: default;
  }

  :deep(pre.mermaid) {
    background: transparent;
    padding: 16px;
    margin: 16px 0;
    text-align: center;
    overflow-x: auto;

    svg {
      max-width: 100%;
      height: auto;
    }
  }

  :deep(.d-error) {
    display: none;
  }

  :deep(a) {
    color: var(--color-primary);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
