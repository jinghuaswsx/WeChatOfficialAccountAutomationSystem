<template>
  <div class="settings">
    <h2>系统设置</h2>
    <el-tabs>
      <el-tab-pane label="AI 模型配置">
        <el-form label-width="120px">
          <el-form-item label="Claude API Key">
            <el-input v-model="settings.claude_key" type="password" show-password />
          </el-form-item>
          <el-form-item label="DeepSeek API Key">
            <el-input v-model="settings.deepseek_key" type="password" show-password />
          </el-form-item>
          <el-form-item label="Gemini API Key">
            <el-input v-model="settings.gemini_key" type="password" show-password />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="发布平台">
        <el-form label-width="120px">
          <el-form-item label="微信 AppID">
            <el-input v-model="settings.wechat_app_id" />
          </el-form-item>
          <el-form-item label="微信 AppSecret">
            <el-input v-model="settings.wechat_app_secret" type="password" show-password />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="评分阈值">
        <el-form label-width="140px">
          <el-form-item label="通过阈值">
            <el-slider v-model="settings.pass_threshold" :min="50" :max="100" show-input />
          </el-form-item>
          <el-form-item label="AI 痕迹底线">
            <el-slider v-model="settings.ai_trace_limit" :min="30" :max="100" show-input />
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="插件管理">
        <el-table :data="plugins" style="width: 100%">
          <el-table-column prop="type" label="类型" width="150" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default>
              <el-tag type="success">已加载</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <el-button type="primary" style="margin-top: 20px" @click="saveSettings">保存设置</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const settings = ref({
  claude_key: '', deepseek_key: '', gemini_key: '',
  wechat_app_id: '', wechat_app_secret: '',
  pass_threshold: 80, ai_trace_limit: 70,
})
const plugins = ref<any[]>([])

onMounted(async () => {
  try {
    const resp = await api.get('/api/plugins')
    const data = resp.data
    plugins.value = [
      ...data.ai_models.map((n: string) => ({ type: 'AI 模型', name: n, status: 'loaded' })),
      ...data.publishers.map((n: string) => ({ type: '发布平台', name: n, status: 'loaded' })),
      ...data.formatters.map((n: string) => ({ type: '排版引擎', name: n, status: 'loaded' })),
      ...data.image_generators.map((n: string) => ({ type: '图片生成', name: n, status: 'loaded' })),
    ]
  } catch (e) { console.error(e) }
})

function saveSettings() {
  ElMessage.success('设置已保存')
}
</script>

<style scoped>
.settings { padding: 20px; }
</style>
