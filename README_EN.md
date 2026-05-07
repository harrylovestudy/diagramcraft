# DiagramCraft

> A CLI diagram drawing tool powered by Mermaid.js. Generate flowcharts, architecture diagrams, and more with simple commands.

DiagramCraft is a lightweight command-line tool that wraps the [Mermaid.js](https://mermaid.js.org/) rendering engine, supporting **11 common diagram types** including flowcharts, system architecture diagrams, sequence diagrams, class diagrams, Gantt charts, and more. It works as a standalone tool or integrates into AI document workflows like [QwenPaw](https://github.com/anthropics/claude-code).

## Features

- **11 diagram types** — Flowchart, Architecture, Sequence, Org Chart, Class, Gantt, ER, State, Pie, Mind Map
- **Multiple output formats** — PNG / SVG / PDF
- **4 themes** — default, dark, forest, neutral
- **Built-in templates** — Generate common diagrams without writing Mermaid syntax
- **Pipe-friendly** — Read from stdin for seamless AI workflow integration
- **Batch rendering** — Process an entire directory of .mmd files at once
- **Python API** — Call directly from your code

## Installation

### 1. Install mermaid-cli (rendering engine)

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 2. Install DiagramCraft

```bash
pip install diagramcraft
```

Or install from source:

```bash
git clone https://github.com/harrylovestudy/diagramcraft.git
cd diagramcraft
pip install -e .
```

### Requirements

- Python >= 3.9
- Node.js >= 16 (required by mermaid-cli)
- graphviz (required for some diagram types: `apt install graphviz` or `brew install graphviz`)

## Quick Start

```bash
# Render from a Mermaid file
diagramcraft render-cmd input.mmd -o output.png

# Render from text
diagramcraft render-cmd -t "graph TD; A[Start] --> B[End]" -o output.svg -f svg

# Use a built-in template
diagramcraft new architecture -o system.png --theme dark

# Pipe mode (great for AI-generated diagrams)
echo "graph LR; A-->B; B-->C" | diagramcraft from-text -o out.png
```

## Commands

### `render-cmd` — Render a diagram

Render Mermaid diagrams from a file, text, or stdin.

```bash
# From file
diagramcraft render-cmd input.mmd -o output.png -f png

# From text
diagramcraft render-cmd -t "graph TD; A-->B" -o output.svg

# With theme and dimensions
diagramcraft render-cmd input.mmd -o output.png --theme dark -W 1200

# Custom background
diagramcraft render-cmd input.mmd -o output.svg --background white
```

| Parameter | Description |
|-----------|-------------|
| `input_file` | Input .mmd file path |
| `-t, --text` | Pass Mermaid code as string |
| `-o, --output` | Output file path (required) |
| `-f, --format` | Output format: png / svg / pdf (default: png) |
| `--theme` | Theme: default / dark / forest / neutral |
| `-W, --width` | Output width in pixels |
| `-H, --height` | Output height in pixels |
| `-b, --background` | Background color |
| `--css` | Custom CSS file |
| `--config` | Mermaid config file |
| `--timeout` | Render timeout in seconds (default: 60) |

### `new` — Create from template

Generate diagrams quickly using built-in templates.

```bash
diagramcraft new flowchart -o flow.png
diagramcraft new architecture -o arch.svg -f svg --theme dark
diagramcraft new sequence -e  # Print template to stdout for editing
```

### `templates` — List templates

```bash
diagramcraft templates
```

Output:

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

### `validate-cmd` — Validate syntax

```bash
diagramcraft validate-cmd input.mmd
diagramcraft validate-cmd -t "graph TD; A-->B"
```

### `batch` — Batch render

```bash
diagramcraft batch ./diagrams/ -o ./output/ -f svg --theme dark
```

### `from-text` — Pipe mode

Read Mermaid code from stdin and render it.

```bash
echo "graph TD; A-->B; B-->C" | diagramcraft from-text -o out.png
cat diagram.mmd | diagramcraft from-text -o out.svg -f svg
```

## Python API

```python
from diagramcraft import render, render_string

# Render a string
render_string("graph TD; A-->B", "output.svg", format="svg", theme="dark")

# Render a file
render("input.mmd", "output.png", format="png", width=1200)

# Get templates
from diagramcraft import get_template, list_templates

templates = list_templates()  # Returns list of template info dicts
code = get_template("flowchart")  # Returns template code string
```

## Template List

| ID | Type | Description |
|----|------|-------------|
| `flowchart` | Flowchart | Top-down decision flow |
| `flowchart-lr` | Flowchart (LR) | Left-to-right flow layout |
| `architecture` | System Architecture | Multi-layer microservice architecture |
| `sequence` | Sequence Diagram | Component interaction sequence |
| `orgchart` | Organization Chart | Organizational hierarchy |
| `class` | Class Diagram | UML class relationship diagram |
| `gantt` | Gantt Chart | Project timeline |
| `er` | ER Diagram | Entity-Relationship diagram |
| `state` | State Diagram | State machine |
| `pie` | Pie Chart | Data distribution visualization |
| `mindmap` | Mind Map | Hierarchical mind structure |

## QwenPaw Integration

DiagramCraft serves as the diagram tool for QwenPaw document workflows:

```bash
# AI-generated Mermaid code piped directly to render
qwenpaw generate-diagram "draw a microservice architecture" | diagramcraft from-text -o docs/architecture.svg

# Batch render all diagrams in documentation
diagramcraft batch docs/diagrams/ -o docs/images/ -f png

# Python API integration
from diagramcraft import render_string
render_string(ai_generated_mermaid_code, "output.svg")
```

## Output Examples

Flowcharts, architecture diagrams, sequence diagrams, and more can be generated quickly with `diagramcraft new <template>`.

## Development

```bash
git clone https://github.com/harrylovestudy/diagramcraft.git
cd diagramcraft
pip install -e ".[dev]"
```

## License

[MIT License](LICENSE)
