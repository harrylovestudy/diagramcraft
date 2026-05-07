"""DiagramCraft CLI - command-line interface for diagram rendering."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from diagramcraft.core.renderer import (
    render,
    render_string,
    validate,
    RenderError,
    VALID_FORMATS,
    VALID_THEMES,
)
from diagramcraft.core.templates import list_templates, get_template

app = typer.Typer(
    name="diagramcraft",
    help="A CLI diagram drawing tool powered by Mermaid.js.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def render_cmd(
    input_file: Optional[Path] = typer.Argument(None, help="Input .mmd file path"),
    text: Optional[str] = typer.Option(None, "-t", "--text", help="Mermaid code string"),
    output: Path = typer.Option(..., "-o", "--output", help="Output file path"),
    format: str = typer.Option("png", "-f", "--format", help="Output format: png, svg, pdf"),
    theme: Optional[str] = typer.Option(None, "--theme", help="Theme: default, dark, forest, neutral"),
    width: Optional[int] = typer.Option(None, "-W", "--width", help="Output width in pixels"),
    height: Optional[int] = typer.Option(None, "-H", "--height", help="Output height in pixels"),
    background: Optional[str] = typer.Option(None, "-b", "--background", help="Background color"),
    css: Optional[Path] = typer.Option(None, "--css", help="Custom CSS file"),
    config: Optional[Path] = typer.Option(None, "--config", help="Mermaid config file"),
    timeout: int = typer.Option(60, "--timeout", help="Render timeout in seconds"),
):
    """Render a Mermaid diagram to an image file.

    Accepts input from a file, -t/--text flag, or stdin.
    """
    mermaid_code = _get_input(input_file, text)

    if mermaid_code is None:
        console.print("[red]Error:[/red] Provide input via file, -t/--text, or stdin.")
        raise typer.Exit(1)

    try:
        result = render_string(
            mermaid_code=mermaid_code,
            output_file=output,
            format=format,
            theme=theme,
            width=width,
            height=height,
            background=background,
            timeout=timeout,
        )
        console.print(f"[green]Rendered:[/green] {result}")
    except RenderError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def new(
    template_id: str = typer.Argument(..., help="Template ID (e.g. flowchart, architecture)"),
    output: Path = typer.Option(..., "-o", "--output", help="Output file path"),
    format: str = typer.Option("png", "-f", "--format", help="Output format: png, svg, pdf"),
    theme: Optional[str] = typer.Option(None, "--theme", help="Theme name"),
    edit: bool = typer.Option(False, "-e", "--edit", help="Print template to stdout for editing"),
):
    """Create a diagram from a built-in template."""
    template_code = get_template(template_id)
    if template_code is None:
        console.print(f"[red]Error:[/red] Template '{template_id}' not found.")
        console.print("Run [bold]diagramcraft templates[/bold] to see available templates.")
        raise typer.Exit(1)

    if edit:
        # Print template to stdout for the user to edit and pipe back
        sys.stdout.write(template_code)
        raise typer.Exit(0)

    try:
        result = render_string(
            mermaid_code=template_code,
            output_file=output,
            format=format,
            theme=theme,
        )
        console.print(f"[green]Rendered:[/green] {result}")
    except RenderError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="templates")
def list_cmd():
    """List all available diagram templates."""
    templates = list_templates()

    table = Table(title="Available Templates")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description")

    for t in templates:
        table.add_row(t["id"], t["name"], t["description"])

    console.print(table)


@app.command()
def validate_cmd(
    input_file: Optional[Path] = typer.Argument(None, help="Input .mmd file"),
    text: Optional[str] = typer.Option(None, "-t", "--text", help="Mermaid code string"),
):
    """Validate Mermaid syntax."""
    mermaid_code = _get_input(input_file, text)

    if mermaid_code is None:
        console.print("[red]Error:[/red] Provide input via file or -t/--text.")
        raise typer.Exit(1)

    is_valid, error = validate(mermaid_code)
    if is_valid:
        console.print("[green]Valid Mermaid syntax.[/green]")
    else:
        console.print(f"[red]Invalid:[/red] {error}")
        raise typer.Exit(1)


@app.command()
def batch(
    input_dir: Path = typer.Argument(..., help="Directory containing .mmd files"),
    output_dir: Path = typer.Option(..., "-o", "--output", help="Output directory"),
    format: str = typer.Option("png", "-f", "--format", help="Output format"),
    theme: Optional[str] = typer.Option(None, "--theme", help="Theme name"),
):
    """Batch render all .mmd files in a directory."""
    if not input_dir.is_dir():
        console.print(f"[red]Error:[/red] '{input_dir}' is not a directory.")
        raise typer.Exit(1)

    mmd_files = sorted(input_dir.glob("*.mmd"))
    if not mmd_files:
        console.print(f"[yellow]No .mmd files found in '{input_dir}'[/yellow]")
        raise typer.Exit(0)

    output_dir.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0

    for mmd_file in mmd_files:
        out_file = output_dir / f"{mmd_file.stem}.{format}"
        try:
            render(
                input_file=mmd_file,
                output_file=out_file,
                format=format,
                theme=theme,
            )
            console.print(f"  [green]OK[/green] {mmd_file.name} -> {out_file.name}")
            success += 1
        except RenderError as e:
            console.print(f"  [red]FAIL[/red] {mmd_file.name}: {e}")
            failed += 1

    console.print(f"\nDone: {success} succeeded, {failed} failed.")


@app.command()
def from_text(
    output: Path = typer.Option(..., "-o", "--output", help="Output file path"),
    format: str = typer.Option("png", "-f", "--format", help="Output format"),
    theme: Optional[str] = typer.Option(None, "--theme", help="Theme name"),
    timeout: int = typer.Option(60, "--timeout", help="Render timeout in seconds"),
):
    """Read Mermaid code from stdin and render it.

    Usage: echo 'graph TD; A-->B' | diagramcraft from-text -o out.png
    """
    if sys.stdin.isatty():
        console.print("[yellow]Reading from stdin (Ctrl+D to end)...[/yellow]")

    mermaid_code = sys.stdin.read().strip()
    if not mermaid_code:
        console.print("[red]Error:[/red] No input received from stdin.")
        raise typer.Exit(1)

    try:
        result = render_string(
            mermaid_code=mermaid_code,
            output_file=output,
            format=format,
            theme=theme,
            timeout=timeout,
        )
        console.print(f"[green]Rendered:[/green] {result}")
    except RenderError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


def _get_input(input_file: Optional[Path], text: Optional[str]) -> Optional[str]:
    """Resolve input from file, text flag, or stdin."""
    if text:
        return text
    if input_file:
        return input_file.read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def main():
    app()


if __name__ == "__main__":
    main()
