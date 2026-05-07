"""DiagramCraft - A CLI diagram drawing tool powered by Mermaid.js."""

__version__ = "0.1.0"

from diagramcraft.core.renderer import render, render_string
from diagramcraft.core.templates import get_template, list_templates

__all__ = ["render", "render_string", "get_template", "list_templates"]
