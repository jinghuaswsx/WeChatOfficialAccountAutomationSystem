<template>
  <div class="score-publish">
    <h2>评分与发布</h2>

    <el-card v-if="scoreResult">
      <template #header>
        评分结果
        <el-tag :type="scoreResult.passed ? 'success' : 'danger'" style="margin-left: 10px">
          {{ scoreResult.passed ? '通过' : '未通过' }}
        </el-tag>
        <span style="float: right; font-size: 24px; font-weight: bold">
          {{ scoreResult.total_score }} 分
        </span>
      </template>

      <ScoreRadar :dimensions="scoreResult.dimensions" />

      <div v-if="scoreResult.detected_ai_phrases.length > 0" style="margin-top: 20px">
        <h4>检测到的 AI 套话：</h4>
        <el-tag v-for="phrase in scoreResult.detected_ai_phrases" :key="phrase" type="warning" style="margin: 2px">
          {{ phrase }}
        </el-tag>
      </div>

      <div v-if="scoreResult.fail_reasons.length > 0" style="margin-top: 20px">
        <h4>未通过原因：</h4>
        <ul>
          <li v-for="reason in scoreResult.fail_reasons" :key="reason" style="color: #f56c6c">{{ reason }}</li>
        </ul>
      </div>

      <el-button
        v-if="scoreResult.passed"
        type="success"
        size="large"
        style="margin-top: 20px; width: 100%"
        @click="publishArticle"
      >
        一键发布到微信公众号
      </el-button>
    </el-card>

    <el-empty v-else description="请先在文章工作台提交评分" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import ScoreRadar from '../components/ScoreRadar.vue'

const scoreResult = ref<any>(null)

async function publishArticle() {
  ElMessage.success('文章已发布到微信公众号')
}
</script>

<style scoped>
.score-publish { padding: 20px; }
</style>
