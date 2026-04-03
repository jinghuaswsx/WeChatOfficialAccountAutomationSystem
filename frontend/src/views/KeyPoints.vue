<template>
  <div class="key-points">
    <h2>要点管理</h2>
    <el-button type="primary" @click="scanSessions" :loading="scanning">
      扫描今日会话
    </el-button>
    <el-table :data="points" style="margin-top: 20px" v-if="points.length > 0">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="content" label="要点内容" />
      <el-table-column label="脱敏内容" width="300">
        <template #default="{ row }">
          <el-input v-model="row.sanitized_content" placeholder="编辑脱敏内容" type="textarea" :rows="2" />
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_selected ? 'success' : 'info'">
            {{ row.is_selected ? '已选' : '未选' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <el-empty v-else description="暂无要点，请先扫描会话" />

    <el-button
      v-if="points.length > 0"
      type="success"
      style="margin-top: 20px"
      @click="submitPoints"
    >
      确认提交，开始写作
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const points = ref<any[]>([])
const scanning = ref(false)

async function scanSessions() {
  scanning.value = true
  try {
    const resp = await api.get('/api/collector/scan')
    if (resp.data.publishable) {
      const kpResp = await api.get('/api/collector/key-points')
      points.value = kpResp.data
      if (points.value.length === 0) {
        ElMessage.info('扫描完成，暂无新要点')
      }
    } else {
      ElMessage.info('今日无可发布内容')
    }
  } catch (e) {
    ElMessage.error('扫描失败')
  } finally {
    scanning.value = false
  }
}

async function submitPoints() {
  ElMessage.success('要点已提交，流水线开始运行')
}
</script>

<style scoped>
.key-points { padding: 20px; }
</style>
