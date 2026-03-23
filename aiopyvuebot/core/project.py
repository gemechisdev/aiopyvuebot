"""Project lifecycle management."""

from __future__ import annotations

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from aiopyvuebot.core.template import TemplateManager


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "-", name.lower()).strip("-")


class Project:
    """Represents an aiopyvuebot project on disk."""

    CONFIG_FILE = "pyvuebot.json"

    def __init__(
        self,
        name: str,
        template: str = "notebot",
        description: str = "",
        target_dir: Path | None = None,
    ) -> None:
        self.name = name
        self.slug = _slugify(name)
        self.template = template
        self.description = description or f"A Telegram Mini App built with aiopyvuebot"
        self.root = target_dir or (Path.cwd() / self.slug)

    # ── factory ───────────────────────────────────────────────────────────────

    @classmethod
    def load(cls) -> "Project":
        """Load project config from the current working directory."""
        cfg_path = Path.cwd() / cls.CONFIG_FILE
        if not cfg_path.exists():
            raise FileNotFoundError(
                f"Not an aiopyvuebot project (missing {cls.CONFIG_FILE}). "
                "Run this command from inside your project directory."
            )
        cfg: dict[str, Any] = json.loads(cfg_path.read_text())
        proj = cls(
            name=cfg["name"],
            template=cfg.get("template", "notebot"),
            description=cfg.get("description", ""),
            target_dir=Path.cwd(),
        )
        return proj

    # ── scaffolding ───────────────────────────────────────────────────────────

    def scaffold(self, force: bool = False) -> None:
        """Create a new project directory from the selected template."""
        if self.root.exists() and not force:
            raise FileExistsError(
                f"Directory '{self.root}' already exists. "
                "Use --force to overwrite."
            )
        if self.root.exists() and force:
            import shutil
            shutil.rmtree(self.root)

        variables = self._variables()
        mgr = TemplateManager()
        mgr.create_project(self.template, self.root, variables)
        self._write_config()

    def _variables(self) -> dict[str, Any]:
        now = datetime.datetime.now()
        return {
            "project_name": self.name,
            "project_slug": self.slug,
            "project_description": self.description,
            "creation_date": now.strftime("%Y-%m-%d"),
            "creation_year": now.year,
            "template_name": self.template,
        }

    def _write_config(self) -> None:
        cfg = {
            "name": self.name,
            "template": self.template,
            "description": self.description,
            "version": "0.1.0",
            "created_at": datetime.datetime.now().isoformat(),
        }
        (self.root / self.CONFIG_FILE).write_text(
            json.dumps(cfg, indent=2), encoding="utf-8"
        )

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def install(self) -> None:
        """Install npm and Python dependencies."""
        self._run(["npm", "install"], "npm install")
        req = self.root / "requirements.txt"
        if req.exists():
            self._run(
                [sys.executable, "-m", "pip", "install", "-r", str(req)],
                "pip install",
            )

    def dev(self) -> None:
        """Start the Vite development server."""
        self._run(["npm", "run", "dev"])

    def build(self) -> None:
        """Build the frontend for production."""
        self._run(["npm", "run", "build"])

    def deploy(self) -> None:
        """Deploy to Vercel."""
        self._run(["vercel", "--prod"])

    # ── helpers ───────────────────────────────────────────────────────────────

    def _run(self, cmd: list[str], label: str | None = None) -> None:
        label = label or " ".join(cmd)
        result = subprocess.run(cmd, cwd=self.root)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {label}")
