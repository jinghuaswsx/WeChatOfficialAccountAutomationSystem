<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>今日发布状态</template>
          <el-tag :type="publishable ? 'success' : 'info'" size="large">
            {{ publishable ? '有可发布内容' : '暂无可发布内容' }}
          </el-tag>
          <p style="margin-top: 10px; color: #999">
            今日扫描到 {{ sessionCount }} 个会话
          </p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>流水线状态</template>
          <el-tag :type="pipelineStatus === 'idle' ? 'info' : 'warning'" size="large">
            {{ pipelineStatus }}
          </el-tag>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>系统健康</template>
          <el-tag :type="healthy ? 'success' : 'danger'" size="large">
            {{ healthy ? '正常运行' : '异常' }}
          </el-tag>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api'

const publishable = ref(false)
const sessionCount = ref(0)
const pipelineStatus = ref('idle')
const healthy = ref(false)

onMounted(async () => {
  try {
    const health = await api.get('/api/health')
    healthy.value = health.data.status === 'ok'

    const scan = await api.get('/api/collector/scan')
    publishable.value = scan.data.publishable
    sessionCount.value = scan.data.sessions

    const pipeline = await api.get('/api/pipeline/status')
    pipelineStatus.value = pipeline.data.status
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.dashboard { padding: 20px; }
.el-card { margin-bottom: 20px; }
</style>
