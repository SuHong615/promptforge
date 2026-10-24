# promptforge

A tiny Jinja2-based prompt template manager for LLM applications. Keep your
prompts in version-controlled files, validate placeholders up front, and render
them without scattering string concatenation through your code.

## Features

- Load templates from a directory tree (`.j2` by default).
- Strict placeholder detection: every template exposes its required variables.
- Clear errors when a variable is missing or a template is unknown.
- Nested templates with namespaced names (`qa/extract`).

## Install

```bash
pip install -e .
```

## Quick start

```python
from promptforge import TemplateRegistry

registry = TemplateRegistry("examples").load()
print(registry.render("system", role="a helpful assistant"))
# You are a helpful assistant. Answer concisely and in the user's language.
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT