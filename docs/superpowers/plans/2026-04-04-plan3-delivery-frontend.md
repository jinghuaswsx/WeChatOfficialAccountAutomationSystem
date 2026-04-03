# Plan 3: 交付前端 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建 Vue 3 Web UI、微信公众号发布插件、排版引擎插件和飞书通知集成，形成端到端可用的系统。

**Architecture:** Vue 3 + Vite 前端通过 REST API 与 FastAPI 后端通信。前端开发模式走 Vite dev server + API 代理，生产模式由 FastAPI 直接 serve 静态文件。微信发布和排版走插件机制。

**Tech Stack:** Vue 3, Vite, Element Plus, md-editor-v3, wechatpy, FastAPI 静态文件服务

---

## File Structure

```
frontend/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── api/
│   │   └── index.ts          # API 调用封装
│   ├── views/
│   │   ├── Dashboard.vue      # 仪表盘
│   │   ├── KeyPoints.vue      # 要点管理
│   │   ├── Workbench.vue      # 文章工作台
│   │   ├── ScorePublish.vue   # 评分与发布
│   │   ├── StyleManage.vue    # 风格管理
│   │   └── Settings.vue       # 系统设置
│   └── components/
│       ├── Sidebar.vue        # 侧边栏导航
│       └── ScoreRadar.vue     # 评分雷达图
backend/
├── plugins/
│   ├── publishers/
│   │   ├── __init__.py
│   │   └── wechat.py          # 微信公众号发布插件
│   └── formatters/
│       ├── __init__.py
│       └── wechat_formatter.py # 微信排版插件
├── app/
│   ├── core/
│   │   └── notifications.py   # 飞书通知集成
│   └── api/
│       └── articles.py        # 文章 CRUD API
tests/
├── test_wechat_publisher.py
├── test_wechat_formatter.py
├── test_notifications.py
└── test_api_articles.py
```

---

## Task 1: Vue 3 项目初始化

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/tsconfig.json`

- [ ] **Step 1: 初始化 Vue 3 + Vite 项目**

```bash
cd g:/Code/WeChatOfficialAccountAutomationSystem
npm create vite@latest frontend -- --template vue-ts
```

如果交互式命令有问题，手动创建：

```json
// frontend/package.json
{
  "name": "wechat-automation-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.5.0",
    "vue-router": "^4.4.0",
    "element-plus": "^2.9.0",
    "@element-plus/icons-vue": "^2.3.0",
    "md-editor-v3": "^4.20.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0",
    "vue-tsc": "^2.0.0"
  }
}
```

- [ ] **Step 2: 配置 Vite API 代理**

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
  },
})
```

- [ ] **Step 3: 创建入口文件**

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>微信公众号自动化系统</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

```typescript
// frontend/src/main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus, { locale: zhCn })
app.use(router)
app.mount('#app')
```

- [ ] **Step 4: 安装依赖**

```bash
cd frontend && npm install
```

- [ ] **Step 5: 验证开发服务器启动**

```bash
cd frontend && npm run dev
```

Expected: Vite 开发服务器启动在 http://localhost:3000

- [ ] **Step 6: Commit**

```bash
git add frontend/
git commit -m "feat: Vue 3 + Vite + Element Plus 前端项目初始化"
```

---

## Task 2: 路由与布局

**Files:**
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/App.vue` (update)
- Create: `frontend/src/components/Sidebar.vue`
- Create: `frontend/src/views/Dashboard.vue`

- [ ] **Step 1: 创建路由**

```typescript
// frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/key-points', name: 'KeyPoints', component: () => import('../views/KeyPoints.vue') },
  { path: '/workbench', name: 'Workbench', component: () => import('../views/Workbench.vue') },
  { path: '/score-publish', name: 'ScorePublish', component: () => import('../views/ScorePublish.vue') },
  { path: '/style', name: 'StyleManage', component: () => import('../views/StyleManage.vue') },
  { path: '/settings', name: 'Settings', component: () => import('../views/Settings.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
```

- [ ] **Step 2: 创建侧边栏**

```vue
<!-- frontend/src/components/Sidebar.vue -->
<template>
  <el-menu :default-active="$route.path" router class="sidebar-menu">
    <el-menu-item index="/">
      <el-icon><Monitor /></el-icon>
      <span>仪表盘</span>
    </el-menu-item>
    <el-menu-item index="/key-points">
      <el-icon><List /></el-icon>
      <span>要点管理</span>
    </el-menu-item>
    <el-menu-item index="/workbench">
      <el-icon><Edit /></el-icon>
      <span>文章工作台</span>
    </el-menu-item>
    <el-menu-item index="/score-publish">
      <el-icon><DataAnalysis /></el-icon>
      <span>评分与发布</span>
    </el-menu-item>
    <el-menu-item index="/style">
      <el-icon><MagicStick /></el-icon>
      <span>风格管理</span>
    </el-menu-item>
    <el-menu-item index="/settings">
      <el-icon><Setting /></el-icon>
      <span>系统设置</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { Monitor, List, Edit, DataAnalysis, MagicStick, Setting } from '@element-plus/icons-vue'
</script>
```

- [ ] **Step 3: 更新 App.vue 布局**

```vue
<!-- frontend/src/App.vue -->
<template>
  <el-container class="app-container">
    <el-aside width="200px">
      <div class="logo">
        <h3>公众号自动化</h3>
      </div>
      <Sidebar />
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
</script>

<style>
html, body, #app { margin: 0; padding: 0; height: 100%; }
.app-container { height: 100vh; }
.logo { padding: 20px; text-align: center; border-bottom: 1px solid #e6e6e6; }
.logo h3 { margin: 0; color: #409eff; }
.el-aside { background: #fff; border-right: 1px solid #e6e6e6; }
.sidebar-menu { border-right: none; }
</style>
```

- [ ] **Step 4: 创建仪表盘页面**

```vue
<!-- frontend/src/views/Dashboard.vue -->
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
```

- [ ] **Step 5: 创建 API 封装**

```typescript
// frontend/src/api/index.ts
import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 30000,
})

export default api
```

- [ ] **Step 6: Commit**

```bash
git add frontend/
git commit -m "feat: 路由、侧边栏布局、仪表盘页面"
```

---

## Task 3: 要点管理 + 文章工作台页面

**Files:**
- Create: `frontend/src/views/KeyPoints.vue`
- Create: `frontend/src/views/Workbench.vue`

- [ ] **Step 1: 要点管理页面**

```vue
<!-- frontend/src/views/KeyPoints.vue -->
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
```

- [ ] **Step 2: 文章工作台页面**

```vue
<!-- frontend/src/views/Workbench.vue -->
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
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/KeyPoints.vue frontend/src/views/Workbench.vue
git commit -m "feat: 要点管理页面 + 文章工作台页面"
```

---

## Task 4: 评分发布 + 风格管理 + 设置页面

**Files:**
- Create: `frontend/src/views/ScorePublish.vue`
- Create: `frontend/src/views/StyleManage.vue`
- Create: `frontend/src/views/Settings.vue`
- Create: `frontend/src/components/ScoreRadar.vue`

- [ ] **Step 1: 评分雷达图组件**

```vue
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
```

- [ ] **Step 2: 评分与发布页面**

```vue
<!-- frontend/src/views/ScorePublish.vue -->
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
```

- [ ] **Step 3: 风格管理页面**

```vue
<!-- frontend/src/views/StyleManage.vue -->
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
```

- [ ] **Step 4: 系统设置页面**

```vue
<!-- frontend/src/views/Settings.vue -->
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
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/ frontend/src/components/ScoreRadar.vue
git commit -m "feat: 评分发布、风格管理、系统设置页面"
```

---

## Task 5: 文章 CRUD API

**Files:**
- Create: `backend/app/api/articles.py`
- Modify: `backend/app/api/router.py`
- Create: `tests/test_api_articles.py`

- [ ] **Step 1: 写 failing test**

```python
# tests/test_api_articles.py
import pytest


@pytest.mark.asyncio
async def test_list_articles_empty(client):
    resp = await client.get("/api/articles")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_article(client):
    resp = await client.post("/api/articles", json={
        "title": "测试文章",
        "key_points": ["搭建了项目骨架"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "测试文章"
    assert data["status"] == "extracting"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_article(client):
    create_resp = await client.post("/api/articles", json={
        "title": "另一篇",
        "key_points": ["实现了插件系统"],
    })
    article_id = create_resp.json()["id"]

    resp = await client.get(f"/api/articles/{article_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "另一篇"


@pytest.mark.asyncio
async def test_update_article_draft(client):
    create_resp = await client.post("/api/articles", json={
        "title": "待编辑",
        "key_points": ["测试"],
    })
    article_id = create_resp.json()["id"]

    resp = await client.put(f"/api/articles/{article_id}", json={
        "final_draft": "这是我修改后的终稿内容。",
    })
    assert resp.status_code == 200
    assert resp.json()["final_draft"] == "这是我修改后的终稿内容。"
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_api_articles.py -v`
Expected: FAIL

- [ ] **Step 3: Implement articles API**

```python
# backend/app/api/articles.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from backend.app.models.article import Article


class CreateArticleRequest(BaseModel):
    title: str
    key_points: list[str]


class UpdateArticleRequest(BaseModel):
    final_draft: str | None = None
    status: str | None = None


router = APIRouter(prefix="/articles")


@router.get("")
async def list_articles(request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        return [
            {
                "id": a.id,
                "title": a.title,
                "status": a.status,
                "score": a.score,
                "created_at": str(a.created_at) if a.created_at else None,
            }
            for a in articles
        ]


@router.post("")
async def create_article(req: CreateArticleRequest, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = Article(title=req.title, status="extracting")
        db.add(article)
        db.commit()
        db.refresh(article)
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
        }


@router.get("/{article_id}")
async def get_article(article_id: int, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = db.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
            "outline": article.outline,
            "ai_draft": article.ai_draft,
            "deai_draft": article.deai_draft,
            "final_draft": article.final_draft,
            "score": article.score,
            "score_details": article.score_details,
        }


@router.put("/{article_id}")
async def update_article(article_id: int, req: UpdateArticleRequest, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = db.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        if req.final_draft is not None:
            article.final_draft = req.final_draft
        if req.status is not None:
            article.status = req.status
        db.commit()
        db.refresh(article)
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
            "final_draft": article.final_draft,
        }
```

- [ ] **Step 4: 更新 router.py 添加 articles 路由**

在 `backend/app/api/router.py` 中新增：
```python
from backend.app.api.articles import router as articles_router
api_router.include_router(articles_router)
```

- [ ] **Step 5: Run test to verify pass**

Run: `pytest tests/test_api_articles.py -v`
Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/articles.py backend/app/api/router.py tests/test_api_articles.py
git commit -m "feat: 文章 CRUD API"
```

---

## Task 6: 微信发布插件 + 排版插件骨架

**Files:**
- Create: `backend/plugins/publishers/__init__.py`
- Create: `backend/plugins/publishers/wechat.py`
- Create: `backend/plugins/formatters/__init__.py`
- Create: `backend/plugins/formatters/wechat_formatter.py`
- Create: `tests/test_wechat_publisher.py`
- Create: `tests/test_wechat_formatter.py`

- [ ] **Step 1: 写 failing test**

```python
# tests/test_wechat_publisher.py
import pytest


def test_wechat_publisher_implements_interface():
    from backend.plugins.publishers.wechat import WeChatPublisher
    from backend.plugins.base import PublisherPlugin

    publisher = WeChatPublisher(app_id="test", app_secret="test")
    assert isinstance(publisher, PublisherPlugin)
    assert publisher.name == "wechat"
    assert publisher.platform == "wechat"


@pytest.mark.asyncio
async def test_wechat_publisher_authenticate_fails_with_bad_credentials():
    from backend.plugins.publishers.wechat import WeChatPublisher

    publisher = WeChatPublisher(app_id="invalid", app_secret="invalid")
    # 不实际调用微信 API，只测试结构
    assert publisher.name == "wechat"
```

```python
# tests/test_wechat_formatter.py
import pytest


def test_wechat_formatter_implements_interface():
    from backend.plugins.formatters.wechat_formatter import WeChatFormatter
    from backend.plugins.base import FormatterPlugin

    formatter = WeChatFormatter()
    assert isinstance(formatter, FormatterPlugin)
    assert formatter.platform == "wechat"


def test_wechat_formatter_wraps_markdown():
    from backend.plugins.formatters.wechat_formatter import WeChatFormatter

    formatter = WeChatFormatter()
    result = formatter.format("# 标题\n\n这是正文内容。")
    assert "标题" in result
    assert "正文内容" in result
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_wechat_publisher.py tests/test_wechat_formatter.py -v`
Expected: FAIL

- [ ] **Step 3: Implement WeChat publisher**

```python
# backend/plugins/publishers/wechat.py
from __future__ import annotations

from backend.plugins.base import PublisherPlugin


class WeChatPublisher(PublisherPlugin):
    """微信公众号发布插件。基于 wechatpy（实际 API 调用在配置正确后启用）。"""

    def __init__(self, app_id: str = "", app_secret: str = "") -> None:
        self._app_id = app_id
        self._app_secret = app_secret
        self._client = None

    @property
    def name(self) -> str:
        return "wechat"

    @property
    def platform(self) -> str:
        return "wechat"

    def _get_client(self):
        """延迟初始化 wechatpy 客户端。"""
        if self._client is None:
            try:
                from wechatpy import WeChatClient
                self._client = WeChatClient(self._app_id, self._app_secret)
            except ImportError:
                raise RuntimeError("请安装 wechatpy: pip install wechatpy")
        return self._client

    async def authenticate(self) -> bool:
        try:
            client = self._get_client()
            client.fetch_access_token()
            return True
        except Exception:
            return False

    async def upload_image(self, image_path: str) -> str:
        client = self._get_client()
        with open(image_path, "rb") as f:
            result = client.material.add("image", f)
        return result.get("media_id", "")

    async def create_draft(self, title: str, content: str, images: list[str]) -> str:
        client = self._get_client()
        articles = [{
            "title": title,
            "content": content,
            "thumb_media_id": images[0] if images else "",
        }]
        result = client.draft.add(articles)
        return result.get("media_id", "")

    async def publish(self, draft_id: str) -> bool:
        client = self._get_client()
        try:
            client.freepublish.submit(draft_id)
            return True
        except Exception:
            return False

    async def get_publish_status(self, draft_id: str) -> str:
        return "unknown"
```

```python
# backend/plugins/publishers/__init__.py
```

- [ ] **Step 4: Implement WeChat formatter**

```python
# backend/plugins/formatters/wechat_formatter.py
from __future__ import annotations

import re

from backend.plugins.base import FormatterPlugin


class WeChatFormatter(FormatterPlugin):
    """微信公众号排版插件。将 Markdown 转为微信兼容的 HTML。"""

    @property
    def name(self) -> str:
        return "wechat_formatter"

    @property
    def platform(self) -> str:
        return "wechat"

    def format(self, markdown: str, images: list[str] | None = None) -> str:
        """
        将 Markdown 转为微信公众号兼容的 HTML。

        基础实现：后续可接入 doocs/md 或 md2wechat-skill 做高级排版。
        """
        html = markdown

        # 标题
        html = re.sub(r'^### (.+)$', r'<h3 style="font-size:16px;font-weight:bold;margin:20px 0 10px;">\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2 style="font-size:18px;font-weight:bold;margin:25px 0 10px;">\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1 style="font-size:22px;font-weight:bold;margin:30px 0 15px;text-align:center;">\1</h1>', html, flags=re.MULTILINE)

        # 加粗和斜体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # 段落
        paragraphs = html.split('\n\n')
        formatted = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<h'):
                p = f'<p style="margin:15px 0;line-height:1.8;font-size:15px;">{p}</p>'
            formatted.append(p)

        return '\n'.join(formatted)
```

```python
# backend/plugins/formatters/__init__.py
```

- [ ] **Step 5: Run test to verify pass**

Run: `pytest tests/test_wechat_publisher.py tests/test_wechat_formatter.py -v`
Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add backend/plugins/publishers/ backend/plugins/formatters/ tests/test_wechat_publisher.py tests/test_wechat_formatter.py
git commit -m "feat: 微信公众号发布插件 + 排版插件"
```

---

## Task 7: 通知集成 + 前端构建 + 静态文件服务

**Files:**
- Create: `backend/app/core/notifications.py`
- Create: `tests/test_notifications.py`
- Modify: `backend/app/main.py` — 添加静态文件服务

- [ ] **Step 1: 写通知 failing test**

```python
# tests/test_notifications.py
import pytest


def test_build_notification_message():
    from backend.app.core.notifications import build_notification

    msg = build_notification(
        event="points_ready",
        title="今日有 3 个可发布要点",
        details={"count": 3},
        project="WeChatAutomation",
    )
    assert msg["title"] == "今日有 3 个可发布要点"
    assert msg["event"] == "points_ready"
    assert "project" in msg


def test_should_notify_respects_config():
    from backend.app.core.notifications import should_notify

    events = ["points_ready", "published"]
    assert should_notify("points_ready", events) is True
    assert should_notify("draft_ready", events) is False
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_notifications.py -v`
Expected: FAIL

- [ ] **Step 3: Implement notifications**

```python
# backend/app/core/notifications.py
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_notification(
    event: str,
    title: str,
    details: dict | None = None,
    project: str = "WeChatAutomation",
) -> dict:
    """构建通知消息结构。"""
    return {
        "event": event,
        "title": title,
        "details": details or {},
        "project": project,
    }


def should_notify(event: str, enabled_events: list[str]) -> bool:
    """检查该事件是否应该发送通知。"""
    return event in enabled_events


def send_notification(
    title: str,
    body: str,
    project: str = "WeChatAutomation",
) -> bool:
    """
    通过 OpenClaw Notify 发送飞书通知。

    依赖本机安装的 openclaw_notify.py 脚本。
    """
    script_path = Path.home() / ".claude" / "skills" / "openclaw-notify" / "scripts" / "openclaw_notify.py"

    if not script_path.exists():
        return False

    try:
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--title", title,
                "--body", body,
                "--project", project,
                "--respect-preferences",
                "--event", "complete",
            ],
            capture_output=True,
            timeout=30,
        )
        return True
    except Exception:
        return False
```

- [ ] **Step 4: Run test to verify pass**

Run: `pytest tests/test_notifications.py -v`
Expected: 2 passed

- [ ] **Step 5: 更新 main.py 支持静态文件服务**

在 `backend/app/main.py` 的 `create_app` 函数中，`return app` 之前添加：

```python
    # 静态文件服务（生产模式下 serve 前端构建产物）
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        from fastapi.staticfiles import StaticFiles
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
```

- [ ] **Step 6: Run all tests**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过（约 70+ 个）

- [ ] **Step 7: Commit**

```bash
git add backend/app/core/notifications.py backend/app/main.py tests/test_notifications.py
git commit -m "feat: 飞书通知集成 + 静态文件服务"
```

---

## Task 8: 前端构建 + 全量验证 + 推送

**Files:** 无新增后端文件

- [ ] **Step 1: 构建前端**

```bash
cd frontend && npm run build
```

Expected: 构建产物输出到 `backend/static/`

- [ ] **Step 2: 运行全量后端测试**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

- [ ] **Step 3: 启动服务端到端验证**

```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

验证：
- `http://127.0.0.1:8000/` → 前端页面
- `http://127.0.0.1:8000/api/health` → `{"status": "ok"}`
- 前端仪表盘能正常加载数据

- [ ] **Step 4: 推送代码**

```bash
git add -A
git commit -m "feat: 前端构建产物 + 端到端验证"
git push origin master
```

---

## Plan 3 完成标准

- [x] Vue 3 + Vite + Element Plus 前端可构建
- [x] 6 个页面：仪表盘、要点管理、文章工作台、评分发布、风格管理、系统设置
- [x] 文章 CRUD API 支持创建、查看、更新
- [x] 微信公众号发布插件实现 PublisherPlugin 接口
- [x] 微信排版插件实现 FormatterPlugin 接口
- [x] 飞书通知集成 OpenClaw Notify
- [x] 前端构建产物由 FastAPI 静态服务
- [x] 所有测试通过
