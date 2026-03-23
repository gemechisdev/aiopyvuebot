"""Project lifecycle CLI commands."""

from __future__ import annotations

from pathlib import Path

import click

from aiopyvuebot import __version__
from aiopyvuebot.core.project import Project
from aiopyvuebot.core.template import TemplateManager
from aiopyvuebot.core.wizard import SetupWizard


# ── init ──────────────────────────────────────────────────────────────────────

@click.command()
@click.argument("name", required=False)
@click.option("--template", "-t", default="notebot", show_default=True,
              help="Template to use (see `aiopyvuebot templates`).")
@click.option("--description", "-d", default="", help="Short project description.")
@click.option("--yes", "-y", is_flag=True, help="Skip interactive prompts and use defaults.")
@click.option("--force", "-f", is_flag=True, help="Overwrite an existing directory.")
def init(name, template, description, yes, force):
    """Scaffold a new Telegram Mini App project."""
    if yes or name:
        proj = Project(
            name=name or "my-miniapp",
            template=template,
            description=description,
            target_dir=Path.cwd() / (name or "my-miniapp"),
        )
    else:
        wizard = SetupWizard()
        answers = wizard.run(name)
        proj = Project(
            name=answers["name"],
            template=answers["template"],
            description=answers["description"],
        )

    click.echo(f"\n🚀 Creating '{proj.name}' from template '{proj.template}'…")
    try:
        proj.scaffold(force=force)
    except FileExistsError as e:
        raise click.ClickException(str(e))
    except ValueError as e:
        raise click.ClickException(str(e))

    click.echo(f"\n✅ Project created at  ./{proj.slug}/\n")
    click.echo("Next steps:")
    click.echo(f"  cd {proj.slug}")
    click.echo("  cp sample.env .env   # fill in BOT_TOKEN, MONGO_URI, WEB_APP_URL")
    click.echo("  aiopyvuebot install  # installs npm + pip deps")
    click.echo("  aiopyvuebot dev      # starts Vite dev server")
    click.echo()


# ── install ───────────────────────────────────────────────────────────────────

@click.command()
def install():
    """Install npm and Python dependencies in the current project."""
    try:
        proj = Project.load()
    except FileNotFoundError as e:
        raise click.ClickException(str(e))

    click.echo("📦 Installing dependencies…")
    try:
        proj.install()
        click.echo("✅ Dependencies installed.")
    except RuntimeError as e:
        raise click.ClickException(str(e))


# ── dev ───────────────────────────────────────────────────────────────────────

@click.command()
def dev():
    """Start the Vite development server (port 3000)."""
    try:
        proj = Project.load()
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo("🔥 Starting development server on http://localhost:3000 …")
    proj.dev()


# ── build ─────────────────────────────────────────────────────────────────────

@click.command()
def build():
    """Build the Vue frontend for production (outputs to dist/)."""
    try:
        proj = Project.load()
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo("🔨 Building for production…")
    try:
        proj.build()
        click.echo("✅ Build complete → dist/")
    except RuntimeError as e:
        raise click.ClickException(str(e))


# ── deploy ────────────────────────────────────────────────────────────────────

@click.command()
def deploy():
    """Deploy to Vercel (requires `vercel` CLI)."""
    try:
        proj = Project.load()
    except FileNotFoundError as e:
        raise click.ClickException(str(e))
    click.echo("🚢 Deploying to Vercel…")
    try:
        proj.deploy()
    except RuntimeError as e:
        raise click.ClickException(str(e))


# ── templates ─────────────────────────────────────────────────────────────────

@click.command("templates")
def list_templates():
    """List all available project templates."""
    mgr = TemplateManager()
    templates = mgr.list_templates()
    if not templates:
        click.echo("No templates found.")
        return
    click.echo(f"Available templates ({len(templates)}):")
    for t in templates:
        marker = " ← default" if t == "notebot" else ""
        click.echo(f"  • {t}{marker}")
