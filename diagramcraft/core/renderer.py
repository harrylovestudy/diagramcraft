"""Rendering engine - wraps mermaid-cli (mmdc) to render Mermaid diagrams."""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


VALID_FORMATS = ("png", "svg", "pdf")
VALID_THEMES = ("default", "dark", "forest", "neutral", "base")

# Auto-create puppeteer config when running as root (Linux containers)
_PUPPETEER_CONFIG_PATH: Optional[str] = None


def _ensure_puppeteer_config() -> Optional[str]:
    """Create a puppeteer config with --no-sandbox if running as root."""
    global _PUPPETEER_CONFIG_PATH
    if _PUPPETEER_CONFIG_PATH is not None:
        return _PUPPETEER_CONFIG_PATH

    if os.getuid() == 0:
        config = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(config, tmp)
        tmp.close()
        _PUPPETEER_CONFIG_PATH = tmp.name
        return _PUPPETEER_CONFIG_PATH

    return None


class RenderError(Exception):
    """Raised when rendering fails."""


def _find_mmdc() -> str:
    """Locate the mmdc binary."""
    result = subprocess.run(
        ["which", "mmdc"], capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    # Try npx as fallback
    result = subprocess.run(
        ["which", "npx"], capture_output=True, text=True
    )
    if result.returncode == 0:
        return "npx"
    raise RenderError("mermaid-cli (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli")


def render(
    input_file: str | Path,
    output_file: str | Path,
    format: str = "png",
    theme: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    background: Optional[str] = None,
    css_file: Optional[str] = None,
    config_file: Optional[str] = None,
    puppeteer_config: Optional[str] = None,
    timeout: int = 60,
) -> Path:
    """Render a Mermaid file to an image.

    Args:
        input_file: Path to .mmd file
        output_file: Output file path
        format: Output format (png, svg, pdf)
        theme: Mermaid theme (default, dark, forest, neutral, base)
        width: Output width in pixels
        height: Output height in pixels
        background: Background color (e.g. 'white', 'transparent')
        css_file: Custom CSS file path
        config_file: Mermaid config file path
        puppeteer_config: Puppeteer config file path
        timeout: Rendering timeout in seconds

    Returns:
        Path to the output file
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise RenderError(f"Input file not found: {input_path}")

    if format not in VALID_FORMATS:
        raise RenderError(f"Invalid format '{format}'. Must be one of: {VALID_FORMATS}")

    if theme and theme not in VALID_THEMES:
        raise RenderError(f"Invalid theme '{theme}'. Must be one of: {VALID_THEMES}")

    mmdc = _find_mmdc()

    # Build command
    if mmdc == "npx":
        cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "mmdc"]
    else:
        cmd = [mmdc]

    cmd.extend(["-i", str(input_path), "-o", str(output_path), "-e", format])

    if theme:
        cmd.extend(["-t", theme])
    if width:
        cmd.extend(["-w", str(width)])
    if height:
        cmd.extend(["-H", str(height)])
    if background:
        cmd.extend(["-b", background])
    if css_file:
        cmd.extend(["-c", css_file])
    if config_file:
        cmd.extend(["-C", config_file])
    if puppeteer_config:
        cmd.extend(["-p", puppeteer_config])
    else:
        auto_config = _ensure_puppeteer_config()
        if auto_config:
            cmd.extend(["-p", auto_config])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise RenderError(f"Rendering timed out after {timeout}s")

    if result.returncode != 0:
        raise RenderError(f"mmdc failed:\n{result.stderr}")

    if not output_path.exists():
        raise RenderError(f"Output file was not created: {output_path}")

    return output_path


def render_string(
    mermaid_code: str,
    output_file: str | Path,
    format: str = "png",
    theme: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    background: Optional[str] = None,
    timeout: int = 60,
) -> Path:
    """Render a Mermaid code string directly to an image.

    Args:
        mermaid_code: Mermaid diagram code string
        output_file: Output file path
        format: Output format (png, svg, pdf)
        theme: Mermaid theme
        width: Output width
        height: Output height
        background: Background color
        timeout: Rendering timeout in seconds

    Returns:
        Path to the output file
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as f:
        f.write(mermaid_code)
        tmp_path = f.name

    try:
        return render(
            input_file=tmp_path,
            output_file=output_file,
            format=format,
            theme=theme,
            width=width,
            height=height,
            background=background,
            timeout=timeout,
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def validate(mermaid_code: str) -> tuple[bool, Optional[str]]:
    """Validate Mermaid syntax by attempting a dry render.

    Returns:
        (is_valid, error_message)
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as f:
        f.write(mermaid_code)
        tmp_input = f.name

    tmp_output = tmp_input.replace(".mmd", ".svg")

    try:
        render(input_file=tmp_input, output_file=tmp_output, format="svg", timeout=30)
        return True, None
    except RenderError as e:
        return False, str(e)
    finally:
        Path(tmp_input).unlink(missing_ok=True)
        Path(tmp_output).unlink(missing_ok=True)
