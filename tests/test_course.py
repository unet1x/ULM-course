import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
COURSE_DOCS = ROOT / "docs"
EXCLUDED_DOCS = COURSE_DOCS / "superpowers"

INLINE_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>(?:\\.|[^\]])*)\]"
    r"\(\s*(?P<target><[^>\n]+>|[^\s)]+)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\n)]*\)))?\s*\)"
)
REFERENCE_LINK = re.compile(
    r"(?P<image>!)?\[(?P<label>(?:\\.|[^\]])*)\]"
    r"\[(?P<reference>[^\]]*)\]"
)
REFERENCE_DEFINITION = re.compile(
    r"(?m)^[ ]{0,3}\[(?P<reference>[^\]]+)\]:\s*"
    r"(?P<target><[^>\n]+>|\S+)"
)
FENCED_CODE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1\s*$")
INLINE_CODE = re.compile(r"(`+)(?:[^`]|`(?!\1))*?\1")


def markdown_files():
    candidates = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    if COURSE_DOCS.is_dir():
        candidates.extend(COURSE_DOCS.rglob("*.md"))
    return sorted(
        path
        for path in candidates
        if path.is_file() and EXCLUDED_DOCS not in path.parents
    )


def strip_code(text):
    return INLINE_CODE.sub("", FENCED_CODE.sub("", text))


def normalise_reference(value):
    return " ".join(value.strip().casefold().split())


def markdown_references(text):
    clean_text = strip_code(text)
    definitions = {
        normalise_reference(match.group("reference")): match.group("target")
        for match in REFERENCE_DEFINITION.finditer(clean_text)
    }
    references = []

    for match in INLINE_LINK.finditer(clean_text):
        references.append(
            (bool(match.group("image")), match.group("label"), match.group("target"))
        )

    for match in REFERENCE_LINK.finditer(clean_text):
        reference = match.group("reference") or match.group("label")
        target = definitions.get(normalise_reference(reference))
        references.append((bool(match.group("image")), match.group("label"), target))

    return references


def local_path(source, target):
    if target is None:
        return None
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        return COURSE_DOCS / decoded_path.lstrip("/")
    return source.parent / decoded_path


class MarkdownParserTests(unittest.TestCase):
    def test_angle_bracket_urls_are_not_local_paths(self):
        text = (
            "Источник: <https://example.org/rules?id=1>\n\n"
            "[Официальный источник](<https://example.org/rules?id=1>)"
        )
        references = markdown_references(text)
        self.assertEqual(1, len(references))
        self.assertIsNone(local_path(ROOT / "sample.md", references[0][2]))

    def test_image_alt_text_and_percent_encoded_local_path_are_preserved(self):
        references = markdown_references(
            "![Схема сил](assets/four%20forces.svg \"Схема\")"
        )
        self.assertEqual(
            [(True, "Схема сил", "assets/four%20forces.svg")], references
        )
        self.assertEqual(
            ROOT / "assets/four forces.svg",
            local_path(ROOT / "sample.md", references[0][2]),
        )


class CourseStructureTests(unittest.TestCase):
    def test_required_entry_points_exist(self):
        for relative_path in ("README.md", "mkdocs.yml", "docs/index.md"):
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_required_source_directory_exists(self):
        self.assertTrue((ROOT / "docs/sources").is_dir(), "docs/sources")

    def test_no_incomplete_markers(self):
        forbidden = re.compile(r"\b(?:TBD|TODO|FIXME)\b")
        for path in markdown_files():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(
                    forbidden.search(path.read_text(encoding="utf-8")), path
                )

    def test_local_markdown_links_and_images_exist(self):
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for is_image, label, target in markdown_references(text):
                with self.subTest(
                    source=path.relative_to(ROOT), target=target, image=is_image
                ):
                    self.assertIsNotNone(target, "unresolved reference-style link")
                    resolved = local_path(path, target)
                    if resolved is not None:
                        self.assertTrue(resolved.exists(), resolved)
                        if COURSE_DOCS in path.parents:
                            self.assertIn(
                                COURSE_DOCS.resolve(),
                                resolved.resolve().parents,
                                "MkDocs links must stay inside docs/",
                            )

    def test_markdown_images_have_alt_text(self):
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for is_image, label, target in markdown_references(text):
                if is_image:
                    with self.subTest(
                        source=path.relative_to(ROOT), target=target
                    ):
                        self.assertTrue(label.strip(), "image alt text is required")


if __name__ == "__main__":
    unittest.main()
