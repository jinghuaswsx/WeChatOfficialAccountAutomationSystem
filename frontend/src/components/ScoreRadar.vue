<!-- frontend/src/components/ScoreRadar.vue -->
<template>
  <div class="score-radar">
    <div v-for="(dim, key) in dimensions" :key="key" class="score-bar">
      <span class="label">{{ labels[key] || key }}</span>
      <el-progress
        :percentage="dim.final_score"
        :color="dim.final_score >= 80 ? '#67c23a' : dim.final_score >= 60 ? '#e6a23c' : '#f56c6c'"
        :stroke-width="20"
        :text-inside="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ dimensions: Record<string, any> }>()

const labels: Record<string, string> = {
  content_quality: '内容质量',
  ai_trace: 'AI 痕迹',
  style_match: '文风匹配',
  readability: '可读性',
  formatting: '排版规范',
}
</script>

<style scoped>
.score-bar { margin-bottom: 15px; }
.label { display: inline-block; width: 80px; font-size: 14px; }
.el-progress { display: inline-block; width: calc(100% - 90px); }
</style>
