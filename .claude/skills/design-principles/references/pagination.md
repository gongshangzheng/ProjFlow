# 分页设计规范

> 所属 skill：design-principles。列表/结果页设计分页时读本文件。

## 1. 原则

页面列出多项结果（论文、图片、视频、任务、成员等）时**必须分页**，不要一次渲染全部：

- 数据量不确定（几十条到几百条），全量渲染导致页面卡顿
- 用户浏览习惯是一页一页翻
- 避免大数据量下 DOM 节点过多

**例外**：数据量固定且很小（< 10 条，如里程碑列表）；树形结构天然有折叠/展开（如项目树）。

## 2. 客户端分页 vs 服务端分页

| 场景 | 方式 | 理由 |
|------|------|------|
| 数据源是一个已全量加载的 JSON（如 results.json ≤ 数百条） | **客户端 slice** | 数据本来就要全拉（做筛选/统计），分页只是渲染节流 |
| 数据源是目录扫描 / 数据库（量级未知、可能上千） | **服务端分页** | 不能全量拉取，由后端切片 |

### 客户端 slice（参考 SpeedRun.vue / PaperList.vue）

```js
const page = ref(1)
const pageSize = 20
const pageCount = computed(() => Math.ceil(filteredResults.value.length / pageSize))
const pagedResults = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredResults.value.slice(start, start + pageSize)
})
watch([filterModel, filterVideo], () => { page.value = 1 })  // 筛选变化必须重置页码
```

```vue
<n-pagination
  v-if="filteredResults.length > pageSize"
  v-model:page="page" :page-count="pageCount" :page-size="pageSize"
  size="small" style="margin-top: 12px; justify-content: center"
/>
```

### 服务端分页（参考 DatasetBrowser.vue + server/routers/datasets.py）

后端契约：`page`/`size` query 参数 + 完整回显：

```
GET /api/datasets/{id}/browse?path=xxx&page=1&size=20
→ { "items": [...], "total": N, "page": 1, "size": 20, "pages": ceil(N/size) }
```

```python
@router.get("/{dataset_id}/browse")
async def browse(dataset_id: str, path: str = Query(""),
                 page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    ...
    pages = (total + size - 1) // size if total > 0 else 0
    start = (page - 1) * size
    return {"items": items[start:start + size], "total": total,
            "page": page, "size": size, "pages": pages}
```

前端翻页时重新 fetch：

```vue
<n-pagination
  v-if="browseData.pages > 1"
  v-model:page="page" :page-count="browseData.pages" :page-size="pageSize"
  size="small" @update:page="loadBrowse"
/>
```

> 表格型数据 API 也可用 `offset/limit`（返回 `{total, offset, limit, items}`），两者选一后**同模块内保持一致**。

## 3. 页面类型 → 策略速查

| 页面类型 | 策略 | 组件 | page_size |
|---------|------|------|-----------|
| 数据表格 | 远程分页 + 页码器 | `n-data-table` remote + `n-pagination` | 50 |
| 卡片/图片/视频网格 | 页码器（数据已全量在手）或"加载更多"（远程追加） | `n-pagination` / 按钮 | 12–24 |
| 详情内嵌列表 | 懒加载 + "加载更多" | 初始 N 条，按钮扩展 | 12 |
| 输出文件/日志 | 远程分页 + 页码器 | `n-pagination` | 100 |

## 4. 重字段剥离

列表 API 不返回详情页才需要的重字段：

- 评测结果列表：返回摘要（id、model、dataset、status、metrics），不返回完整 `outputs` 数组
- 训练运行列表：返回 `id、title、status`，不返回 `test_metrics` 和 `viz`（图片 base64）
- 详情页单独请求完整数据

## 5. 轮询与缓存

- 只在有"进行中"任务时才轮询（3s 间隔），全部完成后 `clearInterval`；`onUnmounted` 兜底清理
- 轮询 handler 用 `try {} catch {}` 包裹，瞬时失败不中断轮询
- 后端：频繁读取的文件（results.json、metrics.json）加 mtime-aware TTL 缓存
- 前端：列表页用 `keep-alive` 或本地缓存，切换回来不重新 fetch（除非主动刷新）

## 6. 可选进阶（尚未落地，做时再取用）

- **URL query 同步页码**：`?page=3` 可分享/刷新保持（当前各页均用内存 ref）
- **localStorage 持久化浏览位置**：参考 digital_human 的 `localStorage['projflow:speed-run']` 模式——存 model/subject/sample 下钻位置，载入时校验存在性并 clamp 范围
