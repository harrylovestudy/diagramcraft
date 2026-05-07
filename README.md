# DiagramCraft

> 基于 Mermaid.js 的 CLI 画图工具，让文档中的图表生成变得简单高效。

DiagramCraft 是一个轻量级命令行工具，封装 [Mermaid.js](https://mermaid.js.org/) 渲染引擎，支持流程图、系统架构图、时序图、类图、甘特图等 **11 种** 常见图表类型。可作为独立工具使用，也可集成到 [QwenPaw](https://github.com/anthropics/claude-code) 等 AI 文档工作流中。

## 特性

- **11 种图表类型** — 流程图、架构图、时序图、组织架构图、类图、甘特图、ER 图、状态图、饼图、思维导图
- **多格式输出** — PNG / SVG / PDF
- **4 种主题** — default、dark、forest、neutral
- **内置模板** — 快速生成常用图表，无需手写 Mermaid 语法
- **管道友好** — 支持 stdin 输入，轻松集成到 AI 工作流
- **批量渲染** — 一次处理整个目录的 .mmd 文件
- **Python API** — 可在代码中直接调用

## 安装

### 1. 安装 mermaid-cli（渲染引擎）

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 2. 安装 DiagramCraft

```bash
pip install diagramcraft
```

或从源码安装：

```bash
git clone https://github.com/harrylovestudy/diagramcraft.git
cd diagramcraft
pip install -e .
```

### 依赖

- Python >= 3.9
- Node.js >= 16（mermaid-cli 需要）
- graphviz（部分图表类型需要，`apt install graphviz` 或 `brew install graphviz`）

## 快速开始

```bash
# 从 Mermaid 文件渲染
diagramcraft render-cmd input.mmd -o output.png

# 从文本直接渲染
diagramcraft render-cmd -t "graph TD; A[开始] --> B[结束]" -o output.svg -f svg

# 使用内置模板
diagramcraft new architecture -o system.png --theme dark

# 管道模式（适合 AI 生成）
echo "graph LR; A-->B; B-->C" | diagramcraft from-text -o out.png
```

## 命令说明

### `render-cmd` — 渲染图表

从文件、文本或 stdin 渲染 Mermaid 图表。

```bash
# 从文件
diagramcraft render-cmd input.mmd -o output.png -f png

# 从文本
diagramcraft render-cmd -t "graph TD; A-->B" -o output.svg

# 指定主题和尺寸
diagramcraft render-cmd input.mmd -o output.png --theme dark -W 1200

# 自定义背景色
diagramcraft render-cmd input.mmd -o output.svg --background white
```

| 参数 | 说明 |
|------|------|
| `input_file` | 输入 .mmd 文件路径 |
| `-t, --text` | 直接传入 Mermaid 代码 |
| `-o, --output` | 输出文件路径（必填） |
| `-f, --format` | 输出格式：png / svg / pdf（默认 png） |
| `--theme` | 主题：default / dark / forest / neutral |
| `-W, --width` | 输出宽度（像素） |
| `-H, --height` | 输出高度（像素） |
| `-b, --background` | 背景色 |
| `--css` | 自定义 CSS 文件 |
| `--config` | Mermaid 配置文件 |
| `--timeout` | 渲染超时（秒，默认 60） |

### `new` — 从模板创建

使用内置模板快速生成图表。

```bash
diagramcraft new flowchart -o flow.png
diagramcraft new architecture -o arch.svg -f svg --theme dark
diagramcraft new sequence -e  # 打印模板到 stdout（可编辑后管道渲染）
```

### `templates` — 列出模板

```bash
diagramcraft templates
```

输出：

```
                              Available Templates
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID           ┃ Name                      ┃ Description                       ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ flowchart    │ Flowchart                 │ Basic flowchart with decision     │
│ architecture │ System Architecture       │ Multi-layer system architecture   │
│ sequence     │ Sequence Diagram          │ Interaction sequence              │
│ orgchart     │ Organization Chart        │ Organizational hierarchy          │
│ class        │ Class Diagram             │ UML class diagram                 │
│ gantt        │ Gantt Chart               │ Project timeline chart            │
│ er           │ ER Diagram                │ Entity-Relationship diagram       │
│ state        │ State Diagram             │ State machine diagram             │
│ pie          │ Pie Chart                 │ Pie chart for data visualization  │
│ mindmap      │ Mind Map                  │ Hierarchical mind map             │
└──────────────┴───────────────────────────┴───────────────────────────────────┘
```

### `validate-cmd` — 语法校验

```bash
diagramcraft validate-cmd input.mmd
diagramcraft validate-cmd -t "graph TD; A-->B"
```

### `batch` — 批量渲染

```bash
diagramcraft batch ./diagrams/ -o ./output/ -f svg --theme dark
```

### `from-text` — 管道模式

从 stdin 读取 Mermaid 代码并渲染。

```bash
echo "graph TD; A-->B; B-->C" | diagramcraft from-text -o out.png
cat diagram.mmd | diagramcraft from-text -o out.svg -f svg
```

## Python API

```python
from diagramcraft import render, render_string

# 渲染字符串
render_string("graph TD; A-->B", "output.svg", format="svg", theme="dark")

# 渲染文件
render("input.mmd", "output.png", format="png", width=1200)

# 获取模板
from diagramcraft import get_template, list_templates

templates = list_templates()  # 返回模板列表
code = get_template("flowchart")  # 获取模板代码
```

## 模板列表

| ID | 类型 | 说明 |
|----|------|------|
| `flowchart` | 流程图 | 自上而下的决策流程 |
| `flowchart-lr` | 流程图（横向） | 从左到右的流程布局 |
| `architecture` | 系统架构图 | 多层微服务架构 |
| `sequence` | 时序图 | 组件间交互序列 |
| `orgchart` | 组织架构图 | 组织层级结构 |
| `class` | 类图 | UML 类关系图 |
| `gantt` | 甘特图 | 项目时间线 |
| `er` | ER 图 | 实体关系图 |
| `state` | 状态图 | 状态机 |
| `pie` | 饼图 | 数据分布可视化 |
| `mindmap` | 思维导图 | 层级思维结构 |

## 配合 QwenPaw 使用

DiagramCraft 可以作为 QwenPaw 文档工作流的画图工具：

```bash
# AI 生成 Mermaid 代码后直接管道渲染
qwenpaw generate-diagram "画一个微服务架构图" | diagramcraft from-text -o docs/architecture.svg

# 批量渲染文档中的所有图表
diagramcraft batch docs/diagrams/ -o docs/images/ -f png

# Python API 集成
from diagramcraft import render_string
render_string(ai_generated_mermaid_code, "output.svg")
```

## 输出示例

流程图、架构图、时序图等均可通过 `diagramcraft new <template>` 快速生成。

## 开发

```bash
git clone https://github.com/harrylovestudy/diagramcraft.git
cd diagramcraft
pip install -e ".[dev]"
```

## 许可证

[MIT License](LICENSE)
