<template>
  <div class="markdown-body" v-html="rendered"></div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import checkbox from 'markdown-it-task-checkbox'
import { slugify } from '../../utils/markdown'

const props = defineProps({
  content: { type: String, default: '' },
})

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

const rendered = computed(() => {
  if (!props.content) return '<p class="text-light">暂无内容</p>'
  return md.render(props.content)
})
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
}
</style>
