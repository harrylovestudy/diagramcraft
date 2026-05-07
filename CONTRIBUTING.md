# Contributing to DiagramCraft

感谢你对 DiagramCraft 的关注！欢迎贡献代码、报告问题或提出建议。

Thank you for your interest in DiagramCraft! Contributions are welcome.

## 如何贡献 / How to Contribute

### 报告问题 / Report Issues

- 使用 [GitHub Issues](https://github.com/harrylovestudy/diagramcraft/issues) 提交 Bug 报告或功能建议
- 请包含：操作系统、Python 版本、Node.js 版本、复现步骤

### 提交代码 / Submit Code

1. Fork 本仓库
2. 创建你的功能分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -m "Add my feature"`
4. 推送到分支：`git push origin feature/my-feature`
5. 创建 Pull Request

### 开发环境 / Development Setup

```bash
# 克隆仓库
git clone https://github.com/harrylovestudy/diagramcraft.git
cd diagramcraft

# 安装开发依赖
pip install -e ".[dev]"

# 安装 mermaid-cli
npm install -g @mermaid-js/mermaid-cli
```

### 代码规范 / Code Style

- Python 代码遵循 PEP 8
- 使用 type hints
- 函数和类需要 docstring
- 提交前请确保代码能正常运行

### 添加新模板 / Adding New Templates

1. 在 `diagramcraft/core/templates.py` 中添加模板定义
2. 在 `diagramcraft/templates/` 目录添加对应的 `.mmd` 文件
3. 更新 README 中的模板列表

### 测试 / Testing

```bash
# 运行测试
pytest

# 测试 CLI
diagramcraft templates
diagramcraft new flowchart -o test.png
```

## 许可证 / License

贡献的代码将使用 MIT License。
