<template>
  <div class="style-manage">
    <h2>风格管理</h2>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>当前风格画像</template>
          <pre v-if="profile" class="profile-json">{{ JSON.stringify(profile, null, 2) }}</pre>
          <el-empty v-else description="暂无风格画像，请上传样本文章" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>上传样本文章</template>
          <el-input
            v-model="sampleText"
            type="textarea"
            :rows="10"
            placeholder="粘贴你过往写的文章..."
          />
          <el-button type="primary" style="margin-top: 10px" @click="uploadSample">
            提交样本
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const profile = ref<any>(null)
const sampleText = ref('')

onMounted(async () => {
  try {
    const resp = await api.get('/api/style/profile')
    profile.value = resp.data.profile
  } catch (e) { console.error(e) }
})

async function uploadSample() {
  if (!sampleText.value.trim()) return
  try {
    await api.post('/api/style/samples', { samples: [sampleText.value] })
    ElMessage.success('样本已提交')
    sampleText.value = ''
  } catch (e) {
    ElMessage.error('提交失败')
  }
}
</script>

<style scoped>
.style-manage { padding: 20px; }
.profile-json { background: #f5f7fa; padding: 15px; border-radius: 4px; font-size: 13px; overflow: auto; max-height: 400px; }
</style>
