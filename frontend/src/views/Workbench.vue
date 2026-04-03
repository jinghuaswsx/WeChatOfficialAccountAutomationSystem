<template>
  <div class="workbench">
    <h2>文章工作台</h2>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>AI 原稿（只读）</template>
          <div class="draft-content" v-html="aiDraft || '<p style=\'color:#999\'>等待流水线生成...</p>'" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            编辑终稿
            <el-button type="primary" size="small" style="float:right" @click="submitForScore">
              提交评分
            </el-button>
          </template>
          <MdEditor v-model="finalDraft" language="zh-CN" :style="{ height: '500px' }" />
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px" v-if="images.length > 0">
      <template #header>配图预览</template>
      <el-row :gutter="10">
        <el-col :span="8" v-for="(img, i) in images" :key="i">
          <el-image :src="img" fit="cover" style="width: 100%; height: 200px" />
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { ElMessage } from 'element-plus'
import api from '../api'

const aiDraft = ref('')
const finalDraft = ref('')
const images = ref<string[]>([])

async function submitForScore() {
  if (!finalDraft.value.trim()) {
    ElMessage.warning('请先编辑终稿')
    return
  }
  try {
    const resp = await api.post('/api/scorer/score', { text: finalDraft.value })
    ElMessage.success(`评分完成: ${resp.data.total_score} 分`)
  } catch (e) {
    ElMessage.error('评分失败')
  }
}
</script>

<style scoped>
.workbench { padding: 20px; }
.draft-content { min-height: 500px; padding: 10px; background: #fafafa; border-radius: 4px; white-space: pre-wrap; }
</style>
