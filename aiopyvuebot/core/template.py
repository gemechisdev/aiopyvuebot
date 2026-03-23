"""Template management – copies a template and substitutes {{ variables }}."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Any


_VAR_RE = re.compile(r"\{\{(.*?)\}\}")

# File extensions that may contain {{ variable }} placeholders
_TEXT_EXTS = {
    ".py", ".js", ".vue", ".html", ".json",
    ".md", ".txt", ".toml", ".yml", ".yaml",
    ".env", ".cfg", ".ini", ".sh",
}


class TemplateManager:
    """Manages built-in project templates."""

    def __init__(self) -> None:
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def list_templates(self) -> list[str]:
        """Return the names of all available templates."""
        if not self.templates_dir.exists():
            return []
        return sorted(
            d.name
            for d in self.templates_dir.iterdir()
            if d.is_dir() and not d.name.startswith("_")
        )

    def create_project(
        self,
        template_name: str,
        project_path: Path,
        variables: dict[str, Any] | None = None,
    ) -> None:
        """Copy *template_name* to *project_path* and substitute variables."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            available = ", ".join(self.list_templates()) or "none"
            raise ValueError(
                f"Template '{template_name}' not found. "
                f"Available templates: {available}"
            )

        shutil.copytree(
            template_path,
            project_path,
            # Preserve .gitignore and dotfiles
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )

        if variables:
            self._substitute(project_path, variables)

    # ── private ───────────────────────────────────────────────────────────────

    def _substitute(self, root: Path, variables: dict[str, Any]) -> None:
        for dirpath, _dirs, files in os.walk(root):
            for filename in files:
                fp = Path(dirpath) / filename
                if fp.suffix in _TEXT_EXTS or filename in {".gitignore", "sample.env"}:
                    self._substitute_file(fp, variables)

    @staticmethod
    def _substitute_file(path: Path, variables: dict[str, Any]) -> None:
        try:
            text = path.read_text(encoding="utf-8")
            modified = False
            for m in _VAR_RE.finditer(text):
                key = m.group(1).strip()
                if key in variables:
                    text = text.replace(m.group(0), str(variables[key]))
                    modified = True
            if modified:
                path.write_text(text, encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            pass  # skip binary files silently
