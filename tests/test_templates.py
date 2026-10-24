from pathlib import Path

import pytest

from promptforge import PromptTemplateError, TemplateRegistry


@pytest.fixture
def registry(tmp_path: Path):
    (tmp_path / "qa").mkdir()
    (tmp_path / "qa" / "extract.j2").write_text(
        "Extract entities from:\n\n{{ text }}\n\nReturn JSON only.",
        encoding="utf-8",
    )
    (tmp_path / "system.j2").write_text("You are {{ role }}.", encoding="utf-8")
    return TemplateRegistry(tmp_path).load()


def test_loads_nested_and_root_templates(registry):
    assert registry.names() == ["qa/extract", "system"]


def test_render_template(registry):
    out = registry.render("system", role="a helpful assistant")
    assert out == "You are a helpful assistant."


def test_missing_variable_raises(registry):
    with pytest.raises(PromptTemplateError):
        registry.render("system")


def test_unknown_template_raises(registry):
    with pytest.raises(PromptTemplateError):
        registry.render("does-not-exist")


def test_placeholders_are_declared(registry):
    assert registry.get("qa/extract").placeholders == {"text"}