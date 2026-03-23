"""Interactive setup wizard for new projects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import click

from aiopyvuebot.core.template import TemplateManager


class SetupWizard:
    """Walk the user through interactive project creation."""

    def __init__(self) -> None:
        self._mgr = TemplateManager()

    def run(self, project_name: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {}

        # ── project name ──────────────────────────────────────────────────────
        if project_name:
            result["name"] = project_name
        else:
            result["name"] = click.prompt("Project name")

        # ── template ──────────────────────────────────────────────────────────
        templates = self._mgr.list_templates()
        if not templates:
            raise RuntimeError("No templates found in the aiopyvuebot package.")

        click.echo("\nAvailable templates:")
        for i, t in enumerate(templates, 1):
            click.echo(f"  {i}. {t}")

        default_idx = 1
        if len(templates) > 1:
            chosen = click.prompt(
                "Select template",
                type=click.IntRange(1, len(templates)),
                default=default_idx,
            )
            result["template"] = templates[chosen - 1]
        else:
            result["template"] = templates[0]
            click.echo(f"  Using template: {result['template']}")

        # ── description ───────────────────────────────────────────────────────
        result["description"] = click.prompt(
            "Project description",
            default=f"A Telegram Mini App built with aiopyvuebot",
        )

        return result
