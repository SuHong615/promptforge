"""Prompt template loading and rendering for LLM applications."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, StrictUndefined, meta


class PromptTemplateError(Exception):
    """Base error for promptforge template operations."""


@dataclass
class PromptTemplate:
    """A single prompt template."""

    name: str
    template: Any
    variables: frozenset[str] = field(default_factory=frozenset)

    @property
    def placeholders(self) -> frozenset[str]:
        """Variable names required by this template."""
        return self.variables

    def render(self, **context: Any) -> str:
        missing = self.variables - set(context)
        if missing:
            raise PromptTemplateError(
                f"template '{self.name}' missing variables: {sorted(missing)}"
            )
        return self.template.render(**context)

    def __str__(self) -> str:
        return self.name


class TemplateRegistry:
    """Loads and renders prompt templates from a directory."""

    def __init__(self, directory: str | os.PathLike[str], extension: str = ".j2") -> None:
        self.directory = Path(directory)
        self.extension = extension
        self._env = Environment(
            loader=FileSystemLoader(str(self.directory)),
            undefined=StrictUndefined,
            autoescape=False,
            keep_trailing_newline=True,
        )
        self._templates: Dict[str, PromptTemplate] = {}

    def load(self) -> "TemplateRegistry":
        """Load every template with the configured extension."""
        self._templates.clear()
        for path in sorted(self.directory.rglob(f"*{self.extension}")):
            name = path.relative_to(self.directory).as_posix()
            name = name[: -len(self.extension)]
            source = path.read_text(encoding="utf-8")
            ast = self._env.parse(source)
            variables = frozenset(meta.find_undeclared_variables(ast))
            self._templates[name] = PromptTemplate(
                name=name,
                template=self._env.from_string(source),
                variables=variables,
            )
        return self

    def names(self) -> list[str]:
        return sorted(self._templates)

    def get(self, name: str) -> PromptTemplate:
        try:
            return self._templates[name]
        except KeyError as exc:
            raise PromptTemplateError(f"unknown template '{name}'") from exc

    def render(self, name: str, **context: Any) -> str:
        return self.get(name).render(**context)