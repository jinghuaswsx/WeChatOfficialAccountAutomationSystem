# 微信公众号自动化系统 - 设计文档

> 日期: 2026-04-04
> 状态: 待审核

## 1. 项目概述

### 1.1 目标

构建一个基于多模型协作的内容自动化系统，将每日 Claude Code 的使用记录转化为高质量的个人风格文章，自动排版并发布到微信公众号，同时预留多平台扩展能力。

### 1.2 核心原则

- **人机协作**：AI 出初稿，用户修改终稿，系统持续学习用户风格
- **严格去 AI 化**：多维度评分门控，通过主流 AI 检测工具 + 主观体验双重标准
- **插件式架构**：AI 模型、发布平台、排版引擎、图片生成器均可插拔替换
- **本地优先**：本地 Web 服务运行，数据不离开本机

### 1.3 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 后端框架 | FastAPI | 异步、轻量、API 友好 |
| 数据库 | SQLite | 本地单用户，零运维 |
| 微信发布 | wechatpy (4.2k stars) | 活跃维护，完整支持草稿箱+发布 API |
| 前端 | Vue 3 + Vite | 轻量，适合中小型 UI |
| 包管理 | uv / poetry | 现代 Python 依赖管理 |

## 2. 系统架构

### 2.1 架构风格：插件式单体

单体应用为基座，核心功能模块内聚，AI 模型、发布平台、排版引擎、图片生成器通过插件注册中心按需加载。

```
┌─────────────────────────────────────────────────┐
│                   Web UI (前端)                   │
│         审核面板 / 要点筛选 / 一键发布              │
└──────────────────────┬──────────────────────────┘
                       │ REST API + WebSocket
┌──────────────────────▼──────────────────────────┐
│              FastAPI 应用核心                      │
│                                                   │
│  ┌───────────┐ ┌───────────┐ ┌────────────────┐ │
│  │ 采集模块   │ │ 写作流水线 │ │  质量评分系统   │ │
│  │ Collector  │ │ Pipeline  │ │  Scorer        │ │
│  └───────────┘ └───────────┘ └────────────────┘ │
│                                                   │
│  ┌──────────────────────────────────────────────┐│
│  │           插件注册中心 (Plugin Registry)       ││
│  │                                              ││
│  │  ┌─────────┐ ┌─────────┐ ┌──────────────┐  ││
│  │  │ AI 模型  │ │ 发布平台 │ │  图片生成器   │  ││
│  │  │ 插件     │ │ 插件     │ │  插件         │  ││
│  │  └─────────┘ └─────────┘ └──────────────┘  ││
│  │  ┌──────────────────────────────────────┐   ││
│  │  │           排版引擎插件                │   ││
│  │  └──────────────────────────────────────┘   ││
│  └──────────────────────────────────────────────┘│
│                                                   │
│  ┌──────────────────────────────────────────────┐│
│  │           风格学习引擎 (Style Engine)          ││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │   SQLite 数据库   │
              │   本地文件存储     │
              └─────────────────┘
```

### 2.2 项目结构

```
WeChatOfficialAccountAutomationSystem/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── api/                 # REST API 路由
│   │   ├── core/                # 配置、依赖注入、定时任务
│   │   ├── collector/           # Claude Code 记录采集
│   │   ├── pipeline/            # 写作流水线编排
│   │   ├── scorer/              # 质量评分系统
│   │   ├── style_engine/        # 风格学习引擎
│   │   └── models/              # 数据模型 (SQLAlchemy)
│   ├── plugins/
│   │   ├── registry.py          # 插件注册中心
│   │   ├── base.py              # 插件基类定义
│   │   ├── ai_models/           # AI 模型插件
│   │   │   ├── claude.py
│   │   │   ├── deepseek.py
│   │   │   └── qwen.py
│   │   ├── publishers/          # 发布平台插件
│   │   │   ├── wechat.py        # 基于 wechatpy
│   │   │   ├── xiaohongshu.py   # 预留
│   │   │   └── twitter.py       # 预留
│   │   ├── formatters/          # 排版引擎插件
│   │   │   ├── wechat_formatter.py
│   │   │   ├── xiaohongshu_formatter.py  # 预留
│   │   │   └── twitter_formatter.py      # 预留
│   │   └── image_generators/    # 图片生成插件
│   │       └── gemini.py
│   └── data/
│       ├── style_samples/       # 文风样本
│       └── db/                  # SQLite 数据库
├── frontend/                    # Vue 3 Web UI
├── tests/
├── docs/
└── pyproject.toml
```

## 3. 核心模块设计

### 3.1 内容采集模块 (Collector)

**数据源**：`~/.claude/` 下的当日会话记录。

**采集流程**：
1. 扫描当天会话文件
2. 调用 Claude API 提取要点：解决了什么问题、用了什么方法、关键决策
3. 发布判定：检查是否有使用 Superpowers skill 完成「需求分析 → 规划 → 实现」的完整流程
4. 无实质内容 → 标记"当天无可发布内容"，不水文章
5. 有内容 → 生成要点列表推送到 Web UI，等待用户筛选和脱敏

**发布判定标准**：
- 至少有一个具体需求被解决（修小 bug 不算）
- 以使用 Superpowers 完成需求分析、任务规划及实现规划的完整过程为判定基准

### 3.2 多模型写作流水线 (Pipeline)

用户完成要点筛选和脱敏后，进入四阶段流水线：

**Stage 1: 内容提炼** (Claude)
- 输入：脱敏后的要点
- 输出：结构化大纲 + 素材整理
- 同步触发配图生成

**Stage 2: 文章创作** (DeepSeek / 通义千问)
- 输入：大纲 + 风格画像
- 输出：符合用户文风的初稿

**Stage 3: 去 AI 化** (交叉模型)
- 输入：初稿
- 输出：消除 AI 套话/句式，替换为自然表达
- 目标：通过 GPTZero 等主流 AI 检测工具 + 主观上读不出 AI 味

**Stage 4: 审稿** (再换一个模型)
- 输入：去 AI 化后的稿件
- 输出：逻辑通顺性检查、事实准确性校验、残留 AI 痕迹扫描

每个 Stage 的模型均为插件化，可通过配置替换。流水线编排器只负责串联各阶段、传递上下文。

### 3.3 配图生成

- 时机：Stage 1 完成后，根据大纲中的关键场景描述触发
- 模型：Google Gemini（后续可调整）
- 流程：提取 2-3 个适合配图的场景 → 生成英文 prompt → 调用 Gemini API → 图片进入审核流程
- 用户可在文章工作台替换、删除或重新生成配图

### 3.4 质量评分系统 (Scorer)

用户修改终稿后，提交评分。

**评分维度**：

| 维度 | 权重 | 说明 |
|------|------|------|
| 内容质量 | 30% | 逻辑清晰度、信息密度、技术准确性 |
| AI 痕迹 | 30% | AI 套话检测、句式重复度、模拟 AI 检测工具 |
| 文风匹配 | 20% | 与用户风格画像的吻合度 |
| 可读性 | 10% | 段落节奏、句子长度分布、阅读流畅度 |
| 排版规范 | 10% | 标题层级、图文搭配、平台排版适配 |

**评分引擎组成**：
- AI 模型评分：独立模型对各维度打分 (0-100)
- 规则引擎评分：正则/关键词检测 AI 套话黑名单词库
- 风格相似度：与风格画像做向量相似度计算

**门控逻辑**：
- 综合分 >= 80：可发布（Web UI 亮绿灯）
- 综合分 < 80：不可发布，显示各维度得分和具体扣分点
- AI 痕迹单项 < 70：无论总分多少，强制打回（硬性底线）
- 阈值可在系统设置中调整

**打回处理**：
- 系统给出具体修改建议（哪些句子有 AI 味、哪里逻辑断裂）
- 用户可手动修改后重新评分，或让去 AI 化阶段重跑一次

### 3.5 风格学习引擎 (Style Engine)

**阶段 1: 冷启动**
- 导入用户的历史文章样本（大学时期文章）
- 提取风格特征，生成初始风格画像

**阶段 2: 持续进化**
- 每次用户修改终稿，系统自动 diff AI 原稿与用户修改版
- 提取用户的修改模式（常删什么、常改什么、常加什么）
- 积累 10-20 篇后，风格画像趋于稳定

**风格画像结构**：
```json
{
  "vocabulary": {
    "preferred_words": ["搞定", "踩坑"],
    "avoided_words": ["赋能", "抓手"],
    "tone": "偏口语、直接"
  },
  "sentence_patterns": {
    "avg_length": 18,
    "short_sentence_ratio": 0.4,
    "rhetorical_habits": ["喜欢用反问", "段落结尾常用短句收束"]
  },
  "structure": {
    "paragraph_style": "短段落为主",
    "transition_style": "少用过渡词，直接切换话题"
  },
  "revision_patterns": {
    "commonly_deleted": ["值得注意的是", "总而言之"],
    "commonly_rewritten": [
      {"from": "进行了深入的探讨", "to": "聊了聊"}
    ]
  }
}
```

风格画像存储在 SQLite 中，可在 Web UI 上查看和手动微调。画像直接注入写作流水线 Stage 2（创作）和 Stage 3（去 AI 化）的 prompt 中。

## 4. 发布系统与多平台适配

### 4.1 插件接口

所有发布平台插件实现统一基类：

```python
class PublisherPlugin(ABC):
    def authenticate(self) -> bool: ...
    def upload_image(self, image_path: str) -> str: ...
    def create_draft(self, article: Article) -> str: ...
    def publish(self, draft_id: str) -> bool: ...
    def get_publish_status(self, draft_id: str) -> str: ...
```

所有排版引擎插件实现统一基类：

```python
class FormatterPlugin(ABC):
    def format(self, markdown: str, images: list[str]) -> str: ...
    def get_platform(self) -> str: ...
```

### 4.2 微信公众号发布流程

1. 排版引擎将 Markdown 终稿转为微信兼容富文本（参考 doocs/md 或 md2wechat-skill 方案）
2. 通过 wechatpy 上传配图素材
3. 通过 wechatpy 创建草稿
4. 用户在 Web UI 点击一键发布 → 调用 wechatpy 的 freepublish API 完成发布

### 4.3 多平台适配

| 平台 | 内容适配 | 排版方案 | 状态 |
|------|---------|---------|------|
| 微信公众号 | 长文 + 富文本排版 + 配图 | doocs/md 或 md2wechat-skill | 首期实现 |
| 小红书 | 截短为图文笔记，配图为主 | Auto-Redbook-Skills / RedInk | 预留 |
| Twitter/X | 提炼为推文 + 线程 | 自定义格式化 | 预留 |

每个平台的内容适配和排版是发布插件 + 排版插件共同职责，核心流水线不感知平台差异。

### 4.4 新平台接入流程

1. 在 `plugins/publishers/` 下新建插件文件，实现 `PublisherPlugin` 基类
2. 在 `plugins/formatters/` 下新建排版插件，实现 `FormatterPlugin` 基类
3. 在 `config.yaml` 中启用新平台
4. 完成

## 5. Web UI 设计

### 5.1 页面结构

- **仪表盘**：今日发布判定状态、流水线进度、最近发布记录
- **要点管理**：Claude Code 使用要点列表、勾选/脱敏编辑、确认提交
- **文章工作台**：左侧 AI 原稿（只读）、右侧编辑区（Markdown 编辑器）、底部配图预览
- **评分与发布**：雷达图展示各维度得分、扣分详情、一键发布按钮
- **风格管理**：风格画像查看/微调、样本文章管理、修改模式统计
- **系统设置**：AI 模型 API Key 配置、发布平台配置、评分阈值、插件管理

### 5.2 技术方案

- 前端框架：Vue 3 + Vite
- 组件库：Element Plus 或 Naive UI
- Markdown 编辑器：md-editor-v3（实时预览）
- 通信：REST API + WebSocket（流水线进度实时推送）

## 6. 通知集成

通过本机已有的 OpenClaw Notify 技能发送飞书通知。

**通知触发点**：

| 事件 | 通知内容 |
|------|---------|
| 每日定时检测发现可发布内容 | "今日有 N 个可发布要点，请审核" |
| 写作流水线完成初稿 | "初稿已生成，请进入工作台修改"（可选） |
| 文章发布成功 | "文章《xxx》已发布到微信公众号" |
| 文章发布失败 | "发布失败：具体错误信息" |

**实现方式**：调用本机 OpenClaw Notify Python 脚本，不需要额外集成飞书 API。

## 7. 数据模型

### 核心实体

- **Session**: Claude Code 会话记录（日期、原始数据引用、提取状态）
- **KeyPoint**: 提取的要点（内容、是否选中、脱敏内容、所属 Session）
- **Article**: 文章（各阶段内容、状态、评分、发布记录）
- **StyleProfile**: 风格画像（特征 JSON、版本号、更新时间）
- **RevisionHistory**: 修改历史（AI 原稿、用户终稿、diff）

### 文章状态流转

```
extracting → points_ready → writing → draft_ready → reviewing → scored → published
                                                         ↓
                                                    rejected (打回修改)
```

## 8. 配置管理

```yaml
# config.yaml
app:
  host: "127.0.0.1"
  port: 8000
  daily_check_time: "20:00"  # 每日定时检测时间

collector:
  claude_data_path: "~/.claude/"
  min_complexity: "superpowers"  # 发布判定标准

pipeline:
  stages:
    - name: "content_extraction"
      plugin: "claude"
    - name: "article_writing"
      plugin: "deepseek"
    - name: "deai_processing"
      plugin: "qwen"
    - name: "review"
      plugin: "claude"

scorer:
  pass_threshold: 80
  ai_trace_hard_limit: 70
  weights:
    content_quality: 0.3
    ai_trace: 0.3
    style_match: 0.2
    readability: 0.1
    formatting: 0.1

publishers:
  wechat:
    enabled: true
    app_id: ""
    app_secret: ""
  xiaohongshu:
    enabled: false
  twitter:
    enabled: false

image_generator:
  plugin: "gemini"
  api_key: ""

notifications:
  enabled: true
  engine: "openclaw_notify"
  events:
    - "points_ready"
    - "draft_ready"
    - "published"
    - "failed"
```

## 9. 开源依赖

| 用途 | 项目 | Stars | 说明 |
|------|------|-------|------|
| 微信 API | wechatpy | 4.2k | Python 微信 SDK，完整公众号 API |
| 微信排版 | doocs/md | 12.2k | Markdown→微信富文本，CLI 可调用 |
| 微信排版备选 | md2wechat-skill | 1.1k | 排版+上传草稿箱一条龙 |
| 小红书排版 | Auto-Redbook-Skills | 1.6k | Python 调用，Playwright 渲染 |
| 小红书排版备选 | RedInk | 5.1k | Flask REST API，图文生成 |
