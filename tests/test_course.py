import json
import re
import unicodedata
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
COURSE_DOCS = ROOT / "docs"
EXCLUDED_DOCS = COURSE_DOCS / "superpowers"
SOURCE_REGISTRY = COURSE_DOCS / "sources" / "official-sources.json"
SOURCE_REGISTRY_MD = COURSE_DOCS / "sources" / "official-sources.md"
TERMS_REGISTRY = COURSE_DOCS / "reference" / "terms.json"
GLOSSARY = COURSE_DOCS / "reference" / "glossary.md"
ABBREVIATIONS = COURSE_DOCS / "reference" / "abbreviations.md"
AUDIT_FILES = (
    COURSE_DOCS / "sources" / "audit-spain-2026.md",
    COURSE_DOCS / "sources" / "audit-technical.md",
    COURSE_DOCS / "sources" / "audit-lapl-transition.md",
)

TASK4_CHAPTERS = (
    "docs/00-start/01-how-to-study.md",
    "docs/00-start/02-ulm-to-part-fcl-roadmap.md",
    "docs/00-start/03-medical-training-exams.md",
    "docs/01-air-law/01-regulatory-system.md",
    "docs/01-air-law/02-ulm-licence-maf.md",
    "docs/01-air-law/03-rules-of-air.md",
    "docs/01-air-law/04-airspace-spain.md",
    "docs/01-air-law/05-aip-notam-occurrence-reporting.md",
    "docs/01-air-law/06-lapl-ppl-transition.md",
)
TASK4_SVGS = (
    "docs/assets/diagrams/airspace-structure.svg",
    "docs/assets/diagrams/ulm-to-lapl-ppl-roadmap.svg",
)
APPLICABILITY_LABELS = (
    "[ULM — ОСНОВА]",
    "[ULM — ОСОБО ВАЖНО]",
    "[PART-FCL — ОБЩЕЕ]",
    "[LAPL — ПЕРЕХОД]",
    "[PPL — РАСШИРЕНИЕ]",
    "[ИСПАНИЯ]",
    "[БЕЗОПАСНОСТЬ]",
    "[ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ]",
)

OFFICIAL_SOURCE_DOMAINS = {
    "www.easa.europa.eu",
    "eur-lex.europa.eu",
    "www.boe.es",
    "www.seguridadaerea.gob.es",
    "sede.seguridadaerea.gob.es",
    "aip.enaire.es",
    "www.aemet.es",
    "ama.aemet.es",
}
REQUIRED_SOURCE_IDS = {
    "SRC-EASA-AIRCREW-2026",
    "SRC-EASA-SERA-2025",
    "SRC-EURLEX-1178-2011",
    "SRC-EURLEX-2024-2076",
    "SRC-EURLEX-2025-0134",
    "SRC-BOE-RD-123-2015",
    "SRC-BOE-RD-182-2026",
    "SRC-BOE-RD-765-2022",
    "SRC-BOE-RD-141-2025",
    "SRC-AESA-ULM-PROCEDURES",
    "SRC-AESA-LAPL-PPL-PROCEDURES",
    "SRC-ENAIRE-AIP-ESPANA",
    "SRC-AEMET-AVIATION",
}
REQUIRED_CANONICAL_TERMS = {
    "ULM",
    "MAF",
    "LAPL(A)",
    "PPL(A)",
    "Part-FCL",
    "DTO",
    "ATO",
    "SERA",
    "AIP",
    "NOTAM",
    "AFM",
    "POH",
    "PIC",
    "VFR",
    "VMC",
    "IMC",
    "angle of attack",
    "stall",
    "load factor",
    "MTOM",
    "centre of gravity",
    "METAR",
    "TAF",
    "QNH",
    "flight plan",
    "radiofonista (RTC)",
    "AESA",
    "EASA",
    "ICAO",
    "ENAIRE",
    "AIP SUP",
    "AIC",
    "ATC clearance",
    "controlled airspace",
    "recency",
    "occurrence reporting",
    "SEP",
    "skill test",
}

FENCE_OPENER = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(`+)(?:[^`]|`(?!\1))*?\1")
EXPLICIT_HTML_ANCHOR = re.compile(
    r"<a\b[^>]*\bid\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))",
    re.IGNORECASE,
)
ATX_HEADING = re.compile(r"^[ ]{0,3}(#{1,6})[ \t]+(.+?)\s*$")
SETEXT_UNDERLINE = re.compile(r"^[ ]{0,3}(?:=+|-+)[ \t]*$")
ATTRIBUTE_ID = re.compile(r"\s*\{[^}]*#([^\s.}]+)[^}]*\}\s*$")


def markdown_files():
    candidates = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    if COURSE_DOCS.is_dir():
        candidates.extend(COURSE_DOCS.rglob("*.md"))
    return sorted(
        path
        for path in candidates
        if path.is_file() and EXCLUDED_DOCS not in path.parents
    )


def _mask_non_newlines(value):
    return "".join(
        character if character in "\r\n" else " " for character in value
    )


def strip_fenced_code(text):
    output = []
    fence_character = None
    fence_length = 0

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if fence_character is None:
            opener = FENCE_OPENER.match(body)
            if opener is None:
                output.append(line)
                continue
            fence = opener.group(1)
            info = opener.group(2)
            if fence[0] == "`" and "`" in info:
                output.append(line)
                continue
            fence_character = fence[0]
            fence_length = len(fence)
            output.append(_mask_non_newlines(line))
            continue

        output.append(_mask_non_newlines(line))
        closer = re.fullmatch(
            rf" {{0,3}}{re.escape(fence_character)}"
            rf"{{{fence_length},}}[ \t]*",
            body,
        )
        if closer is not None:
            fence_character = None
            fence_length = 0

    return "".join(output)


def strip_code(text):
    without_fences = strip_fenced_code(text)
    return INLINE_CODE.sub(
        lambda match: _mask_non_newlines(match.group(0)), without_fences
    )


def normalise_reference(value):
    return " ".join(value.strip().casefold().split())


def _parse_bracket(text, start):
    if start >= len(text) or text[start] != "[":
        return None
    value = []
    depth = 1
    position = start + 1
    while position < len(text):
        character = text[position]
        if character == "\\" and position + 1 < len(text):
            value.append(text[position + 1])
            position += 2
            continue
        if character == "[":
            depth += 1
            value.append(character)
        elif character == "]":
            depth -= 1
            if depth == 0:
                return "".join(value), position + 1
            value.append(character)
        else:
            value.append(character)
        position += 1
    return None


def _parse_destination(text, start):
    if start >= len(text):
        return None
    if text[start] == "<":
        position = start + 1
        while position < len(text):
            if text[position] == "\n":
                return None
            if text[position] == "\\" and position + 1 < len(text):
                position += 2
                continue
            if text[position] == ">":
                return text[start : position + 1], position + 1
            position += 1
        return None

    value = []
    depth = 0
    position = start
    while position < len(text):
        character = text[position]
        if character == "\\" and position + 1 < len(text):
            value.extend((character, text[position + 1]))
            position += 2
            continue
        if character == "(":
            depth += 1
            value.append(character)
        elif character == ")":
            if depth == 0:
                break
            depth -= 1
            value.append(character)
        elif character.isspace() and depth == 0:
            break
        else:
            value.append(character)
        position += 1
    if depth:
        return None
    return "".join(value), position


def _parse_title(text, start):
    opener = text[start]
    closer = ")" if opener == "(" else opener
    depth = 1
    position = start + 1
    while position < len(text):
        character = text[position]
        if character == "\\" and position + 1 < len(text):
            position += 2
            continue
        if character == "\n" and opener != "(":
            return None
        if opener == "(" and character == "(":
            depth += 1
        elif character == closer:
            depth -= 1
            if depth == 0:
                return position + 1
        position += 1
    return None


def _parse_inline_target(text, start):
    position = start + 1
    while position < len(text) and text[position].isspace():
        position += 1
    parsed = _parse_destination(text, position)
    if parsed is None:
        return None
    target, position = parsed
    if position < len(text) and text[position] == ")":
        return target, position + 1
    if position >= len(text) or not text[position].isspace():
        return None
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] not in "\"'(":
        return None
    position = _parse_title(text, position)
    if position is None:
        return None
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != ")":
        return None
    return target, position + 1


def _reference_definitions(text):
    definitions = {}
    spans = []
    offset = 0
    for line in text.splitlines(keepends=True):
        indent = len(line) - len(line.lstrip(" "))
        if indent <= 3 and indent < len(line) and line[indent] == "[":
            parsed_label = _parse_bracket(line, indent)
            if parsed_label is not None:
                label, position = parsed_label
                if position < len(line) and line[position] == ":":
                    position += 1
                    while position < len(line) and line[position] in " \t":
                        position += 1
                    parsed_target = _parse_destination(line, position)
                    reference = normalise_reference(label)
                    if (
                        parsed_target is not None
                        and parsed_target[0]
                        and not reference.startswith("^")
                    ):
                        definitions[reference] = parsed_target[0]
                        spans.append((offset, offset + len(line)))
        offset += len(line)
    return definitions, spans


def markdown_references(text):
    clean_text = strip_code(text)
    definitions, definition_spans = _reference_definitions(clean_text)
    references = []
    position = 0
    span_index = 0

    while position < len(clean_text):
        while (
            span_index < len(definition_spans)
            and position >= definition_spans[span_index][1]
        ):
            span_index += 1
        if (
            span_index < len(definition_spans)
            and definition_spans[span_index][0]
            <= position
            < definition_spans[span_index][1]
        ):
            position = definition_spans[span_index][1]
            continue
        if clean_text[position] == "\\":
            position += 2
            continue

        is_image = clean_text.startswith("![", position)
        label_start = position + 1 if is_image else position
        if clean_text[label_start] != "[":
            position += 1
            continue
        parsed_label = _parse_bracket(clean_text, label_start)
        if parsed_label is None:
            position += 1
            continue
        label, after_label = parsed_label

        if after_label < len(clean_text) and clean_text[after_label] == "(":
            parsed_inline = _parse_inline_target(clean_text, after_label)
            if parsed_inline is not None:
                target, after_reference = parsed_inline
                references.append((is_image, label, target))
                position = after_reference
                continue
        elif after_label < len(clean_text) and clean_text[after_label] == "[":
            parsed_reference = _parse_bracket(clean_text, after_label)
            if parsed_reference is not None:
                reference, after_reference = parsed_reference
                reference = reference or label
                target = definitions.get(normalise_reference(reference))
                references.append((is_image, label, target))
                position = after_reference
                continue
        else:
            target = definitions.get(normalise_reference(label))
            if target is not None:
                references.append((is_image, label, target))
                position = after_label
                continue

        position = after_label

    return references


def _markdown_link_spans(text):
    definitions, definition_spans = _reference_definitions(text)
    references = []
    position = 0
    span_index = 0

    while position < len(text):
        while (
            span_index < len(definition_spans)
            and position >= definition_spans[span_index][1]
        ):
            span_index += 1
        if (
            span_index < len(definition_spans)
            and definition_spans[span_index][0]
            <= position
            < definition_spans[span_index][1]
        ):
            position = definition_spans[span_index][1]
            continue
        if text[position] == "\\":
            position += 2
            continue

        is_image = text.startswith("![", position)
        label_start = position + 1 if is_image else position
        if text[label_start] != "[":
            position += 1
            continue
        parsed_label = _parse_bracket(text, label_start)
        if parsed_label is None:
            position += 1
            continue
        label, after_label = parsed_label
        target = None
        after_reference = after_label

        if after_label < len(text) and text[after_label] == "(":
            parsed_inline = _parse_inline_target(text, after_label)
            if parsed_inline is not None:
                target, after_reference = parsed_inline
        elif after_label < len(text) and text[after_label] == "[":
            parsed_reference = _parse_bracket(text, after_label)
            if parsed_reference is not None:
                reference, after_reference = parsed_reference
                target = definitions.get(normalise_reference(reference or label))
        else:
            target = definitions.get(normalise_reference(label))

        if target is not None:
            references.append(
                (
                    is_image,
                    label_start + 1,
                    after_label - 1,
                    target,
                    position,
                    after_reference,
                )
            )
            position = after_reference
            continue
        position = after_label

    return references, definition_spans


def _inside_any(position, spans):
    return any(start <= position < end for start, end in spans)


def _term_pattern(canonical):
    parts = [re.escape(part) for part in canonical.split()]
    body = r"\s+".join(parts)
    return re.compile(rf"(?<![\w]){body}(?![\w])", re.IGNORECASE)


def unlinked_term_occurrences(text, term):
    clean_text = strip_code(text)
    links, definition_spans = _markdown_link_spans(clean_text)
    ignored = list(definition_spans)
    linked_labels = []
    anchor = term["anchor"]

    for is_image, label_start, label_end, target, start, end in links:
        ignored.extend(((start, label_start), (label_end, end)))
        if is_image:
            ignored.append((label_start, label_end))
            continue
        fragment = unquote(urlsplit(_clean_target(target)).fragment)
        if fragment == anchor:
            linked_labels.append((label_start, label_end))

    ignored.extend(
        match.span()
        for match in re.finditer(r"<https?://[^>\n]+>", clean_text)
    )
    anchor_pattern = re.compile(
        rf"<a\b[^>]*\bid\s*=\s*(?:"
        rf'"{re.escape(anchor)}"|\'{re.escape(anchor)}\'|'
        rf"{re.escape(anchor)}(?=[\s>]))[^>]*>"
        rf"(?:[ \t]*</a[ \t]*>)?",
        re.IGNORECASE,
    )
    canonical_pattern = _term_pattern(term["canonical"]).pattern
    definition_pattern = re.compile(
        rf"[ \t]*(?:{canonical_pattern}|"
        rf"\*\*{canonical_pattern}\*\*|"
        rf"__{canonical_pattern}__)"
        r"(?=[ \t]*(?:—|–|:))",
        re.IGNORECASE,
    )
    for anchor_match in anchor_pattern.finditer(clean_text):
        ignored.append(anchor_match.span())
        line_end = clean_text.find("\n", anchor_match.end())
        if line_end == -1:
            line_end = len(clean_text)
        definition = definition_pattern.match(
            clean_text, anchor_match.end(), line_end
        )
        if definition is not None:
            ignored.append(definition.span())

    violations = []
    for match in _term_pattern(term["canonical"]).finditer(clean_text):
        if _inside_any(match.start(), ignored):
            continue
        if _inside_any(match.start(), linked_labels):
            continue
        line = clean_text.count("\n", 0, match.start()) + 1
        violations.append(line)
    return violations


def is_learner_chapter(path):
    try:
        relative = path.relative_to(COURSE_DOCS)
    except ValueError:
        return False
    return bool(relative.parts and re.fullmatch(r"\d{2}-.+", relative.parts[0]))


def learner_chapter_files():
    return sorted(
        path
        for path in COURSE_DOCS.rglob("*.md")
        if path.is_file() and is_learner_chapter(path)
    )


def source_rows_from_markdown(text):
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*SRC-[A-Z0-9-]+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            continue
        identifier, authority, title, edition, checked, scope, url = cells
        rows.append(
            {
                "id": identifier,
                "authority": authority,
                "title": title,
                "url": url.removeprefix("<").removesuffix(">"),
                "edition": edition,
                "checked": checked,
                "scope": scope,
            }
        )
    return rows


def abbreviation_links_from_markdown(text):
    links = set()
    row_pattern = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*\[[^]]+\]"
        r"\(glossary\.md#(term-[a-z0-9-]+)\)\s*\|",
        re.MULTILINE,
    )
    for abbreviation, anchor in row_pattern.findall(text):
        links.add((abbreviation.strip(), anchor))
    return links


def glossary_sections(text):
    matches = []
    for match in EXPLICIT_HTML_ANCHOR.finditer(text):
        anchor = next(group for group in match.groups() if group is not None)
        if anchor.startswith("term-"):
            matches.append((anchor, match.start()))
    return {
        anchor: text[start : matches[index + 1][1]]
        if index + 1 < len(matches)
        else text[start:]
        for index, (anchor, start) in enumerate(matches)
    }


def _markdown_unescape(value):
    return re.sub(r"\\([\\`*{}\[\]()#+\-.!_> ])", r"\1", value)


def _clean_target(target):
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    return _markdown_unescape(target)


def local_path(source, target):
    if target is None:
        return None
    target = _clean_target(target)
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    if not parsed.path:
        return source if parsed.fragment else None
    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        return COURSE_DOCS / decoded_path.lstrip("/")
    return source.parent / decoded_path


def _heading_slug(value):
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*~]", "", value)
    value = re.sub(r"(?<!\w)_(?=\S)|(?<=\S)_(?!\w)", "", value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def _unique_anchor(identifier, used_ids):
    while identifier in used_ids or not identifier:
        counted = re.match(r"^(.*)_([0-9]+)$", identifier)
        if counted:
            identifier = f"{counted.group(1)}_{int(counted.group(2)) + 1}"
        else:
            identifier = f"{identifier}_1"
    used_ids.add(identifier)
    return identifier


def markdown_anchors(text):
    anchors = {
        next(group for group in match.groups() if group is not None)
        for match in EXPLICIT_HTML_ANCHOR.finditer(text)
    }
    lines = strip_fenced_code(text).splitlines()
    for index, line in enumerate(lines):
        match = ATX_HEADING.match(line)
        heading = None
        if match:
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2))
        elif (
            index + 1 < len(lines)
            and line.strip()
            and SETEXT_UNDERLINE.match(lines[index + 1])
        ):
            heading = line.strip()
        if heading is None:
            continue

        attribute = ATTRIBUTE_ID.search(heading)
        if attribute:
            anchors.add(attribute.group(1))
            continue
        slug = _heading_slug(heading)
        _unique_anchor(slug, anchors)
    return anchors


def fragment_exists(text, fragment):
    return unquote(fragment.lstrip("#")) in markdown_anchors(text)


def local_target_is_valid(path, is_image):
    return path.is_file() if is_image else path.exists()


def local_reference_error(source, target, is_image=False):
    if target is None:
        return "unresolved reference-style link"
    resolved = local_path(source, target)
    if resolved is None:
        return None
    if not local_target_is_valid(resolved, is_image):
        kind = "image file" if is_image else "link target"
        return f"missing local {kind}: {resolved}"

    resolved_path = resolved.resolve()
    docs_resolved = COURSE_DOCS.resolve()
    if COURSE_DOCS in source.parents and docs_resolved not in resolved_path.parents:
        return f"MkDocs links must stay inside docs/: {resolved}"

    parsed = urlsplit(_clean_target(target))
    if (
        parsed.fragment
        and not is_image
        and resolved_path.suffix.casefold() == ".md"
    ):
        text = resolved_path.read_text(encoding="utf-8")
        if not fragment_exists(text, parsed.fragment):
            return f"missing Markdown anchor #{unquote(parsed.fragment)} in {resolved}"
    return None


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

    def test_full_collapsed_and_shortcut_references_are_resolved(self):
        text = """
[Термин][term], [term][] и [term].
![Полная схема][diagram], ![diagram][] и ![diagram].

[term]: glossary.md#term "Определение"
[diagram]: <assets/diagram (final).svg> 'Схема'
"""
        self.assertEqual(
            [
                (False, "Термин", "glossary.md#term"),
                (False, "term", "glossary.md#term"),
                (False, "term", "glossary.md#term"),
                (True, "Полная схема", "<assets/diagram (final).svg>"),
                (True, "diagram", "<assets/diagram (final).svg>"),
                (True, "diagram", "<assets/diagram (final).svg>"),
            ],
            markdown_references(text),
        )

    def test_nested_labels_titles_and_balanced_destinations_are_scanned(self):
        text = (
            '[Внешний [вложенный] термин](guides/function_(a_(b)).md "Раздел") '
            '![Схема [сил]](<assets/four forces.svg> \'Подпись\')'
        )
        self.assertEqual(
            [
                (
                    False,
                    "Внешний [вложенный] термин",
                    "guides/function_(a_(b)).md",
                ),
                (True, "Схема [сил]", "<assets/four forces.svg>"),
            ],
            markdown_references(text),
        )

    def test_angle_bracket_url_with_parentheses_and_title_stays_external(self):
        references = markdown_references(
            '[Источник](<https://example.org/rules_(current)?q=(a)> "Правило")'
        )
        self.assertEqual(
            [
                (
                    False,
                    "Источник",
                    "<https://example.org/rules_(current)?q=(a)>",
                )
            ],
            references,
        )
        self.assertIsNone(local_path(ROOT / "sample.md", references[0][2]))

    def test_same_page_fragment_resolves_to_source_document(self):
        source = ROOT / "docs/index.md"
        self.assertEqual(source, local_path(source, "#порядок-обучения"))

    def test_markdown_and_explicit_html_anchors_are_discovered(self):
        anchors = globals().get("markdown_anchors", lambda text: set())(
            """# Flight planning

## Повтор
## Повтор

Setext section
--------------

### Heading with explicit ID {#custom-id}

<a id="manual-anchor"></a>
"""
        )
        self.assertTrue(
            {
                "flight-planning",
                "_1",
                "_2",
                "setext-section",
                "custom-id",
                "manual-anchor",
            }.issubset(anchors)
        )

    def test_heading_slug_matches_pinned_python_markdown_default(self):
        self.assertEqual("", _heading_slug("Порядок обучения"))
        self.assertEqual("ulmmaf-maf", _heading_slug("ULM/MAF и MAF"))
        self.assertEqual(
            "ulmmaf-lapla-ppla",
            _heading_slug("ULM/MAF → LAPL(A) или PPL(A)"),
        )

    def test_heading_slug_preserves_literal_intraword_underscore(self):
        self.assertEqual("foo_bar", _heading_slug("foo_bar"))

    def test_heading_slug_removes_actual_underscore_emphasis_delimiters(self):
        self.assertEqual("emphasised", _heading_slug("_emphasised_"))

    def test_present_anchor_is_accepted(self):
        fragment_exists = globals().get(
            "fragment_exists", lambda text, fragment: True
        )
        self.assertTrue(fragment_exists("# Present anchor", "present-anchor"))

    def test_missing_anchor_is_rejected(self):
        fragment_exists = globals().get(
            "fragment_exists", lambda text, fragment: True
        )
        self.assertFalse(fragment_exists("# Present anchor", "missing-anchor"))

    def test_current_index_uses_python_markdown_empty_slug_anchor(self):
        source = ROOT / "docs/index.md"
        reference_error = globals().get(
            "local_reference_error",
            lambda source, target, is_image=False: None,
        )
        self.assertIsNone(reference_error(source, "#_1", is_image=False))
        self.assertIsNotNone(
            reference_error(source, "#порядок-обучения", is_image=False)
        )
        self.assertIsNotNone(
            reference_error(source, "#несуществующий-раздел", is_image=False)
        )

    def test_cross_page_present_and_missing_anchor_targets_are_validated(self):
        source = ROOT / "docs/index.md"
        reference_error = globals().get(
            "local_reference_error",
            lambda source, target, is_image=False: None,
        )
        self.assertIsNone(
            reference_error(
                source,
                "sources/audit-spain-2026.md#_1",
                is_image=False,
            )
        )
        self.assertIsNotNone(
            reference_error(
                source,
                "sources/audit-spain-2026.md#метод-и-иерархия",
                is_image=False,
            )
        )
        self.assertIsNotNone(
            reference_error(
                source,
                "sources/audit-spain-2026.md#несуществующий-раздел",
                is_image=False,
            )
        )

    def test_local_image_target_must_be_a_file(self):
        resolved = local_path(ROOT / "README.md", "docs/sources/")
        target_is_valid = globals().get(
            "local_target_is_valid", lambda path, is_image: path.exists()
        )
        self.assertFalse(target_is_valid(resolved, True))

    def test_repeated_term_links_ignore_code_destinations_and_definitions(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = """[ULM][term-ulm] используется в прозе.
Далее снова используется [ULM][term-ulm].
`ULM ULM` и:
```text
ULM
```
[источник](https://example.test/ULM)
[term-ulm]: ../reference/glossary.md#term-ulm
"""
        self.assertEqual([], unlinked_term_occurrences(text, term))

    def test_every_plain_term_use_after_manifest_definition_is_reported(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = "ULM вводится один раз.\nЗатем ULM повторяется без ссылки.\n"
        self.assertEqual([1, 2], unlinked_term_occurrences(text, term))

    def test_first_and_only_wrong_anchor_term_link_is_reported(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = "[ULM](../reference/glossary.md#term-maf)"
        self.assertEqual([1], unlinked_term_occurrences(text, term))

    def test_inline_term_link_to_own_anchor_is_accepted(self):
        term = {"canonical": "angle of attack", "anchor": "term-angle-of-attack"}
        text = (
            "[angle of attack](../reference/glossary.md#term-angle-of-attack) "
            "вводится ссылкой. Затем "
            "[angle of attack](../reference/glossary.md#term-angle-of-attack)."
        )
        self.assertEqual([], unlinked_term_occurrences(text, term))

    def test_term_link_to_wrong_anchor_is_reported(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = "ULM вводится. Затем [ULM](../reference/glossary.md#term-maf)."
        self.assertEqual([1, 1], unlinked_term_occurrences(text, term))

    def test_term_on_its_explicit_definition_line_is_ignored(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = (
            '<a id="term-ulm"></a> ULM — собственное определение.\n'
            "ULM впервые используется в учебном тексте.\n"
        )
        self.assertEqual([2], unlinked_term_occurrences(text, term))

    def test_only_one_definition_occurrence_on_anchor_line_is_ignored(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = (
            '<a id="term-ulm"></a> ULM — собственное определение; '
            "затем ULM повторяется без ссылки.\n"
        )
        self.assertEqual([1], unlinked_term_occurrences(text, term))

    def test_intraword_hyphen_after_anchor_is_prose_not_a_definition(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = '<a id="term-ulm"></a> This ULM-first course is prose.\n'
        self.assertEqual([1], unlinked_term_occurrences(text, term))

    def test_formatted_canonical_definition_after_anchor_is_ignored(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = '<a id="term-ulm"></a> **ULM** — definition.\n'
        self.assertEqual([], unlinked_term_occurrences(text, term))

    def test_longer_commonmark_closing_fence_is_ignored_and_lines_preserved(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        for character in ("`", "~"):
            with self.subTest(fence=character):
                text = (
                    f"[ULM](#term-ulm)\n{character * 3}text\n"
                    f"ULM\n{character * 4}\nULM\n"
                )
                self.assertEqual([5], unlinked_term_occurrences(text, term))

    def test_only_numbered_course_directories_are_learner_chapters(self):
        self.assertTrue(is_learner_chapter(COURSE_DOCS / "01-air-law" / "intro.md"))
        for path in (
            COURSE_DOCS / "sources" / "audit-spain-2026.md",
            COURSE_DOCS / "sources" / "official-sources.md",
            COURSE_DOCS / "reference" / "glossary.md",
            COURSE_DOCS / "superpowers" / "plans" / "plan.md",
            COURSE_DOCS / "index.md",
            ROOT / "README.md",
            ROOT / "CONTRIBUTING.md",
        ):
            with self.subTest(path=path):
                self.assertFalse(is_learner_chapter(path))


class CourseRegistryTests(unittest.TestCase):
    def load_json(self, path):
        self.assertTrue(path.is_file(), path.relative_to(ROOT))
        return json.loads(path.read_text(encoding="utf-8"))

    def test_registry_files_exist(self):
        for path in (
            SOURCE_REGISTRY,
            SOURCE_REGISTRY_MD,
            TERMS_REGISTRY,
            GLOSSARY,
            ABBREVIATIONS,
        ):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file(), path.relative_to(ROOT))

    def test_official_source_registry_schema_and_required_coverage(self):
        sources = self.load_json(SOURCE_REGISTRY)
        self.assertIsInstance(sources, list)
        required_fields = {
            "id",
            "authority",
            "title",
            "url",
            "edition",
            "checked",
            "scope",
        }
        identifiers = []
        for source in sources:
            with self.subTest(source=source.get("id")):
                self.assertTrue(required_fields.issubset(source))
                self.assertRegex(source["id"], r"^SRC-[A-Z0-9-]+$")
                self.assertEqual("2026-07-13", source["checked"])
                parsed = urlsplit(source["url"])
                self.assertEqual("https", parsed.scheme)
                self.assertIn(parsed.hostname, OFFICIAL_SOURCE_DOMAINS)
                for field in required_fields - {"checked"}:
                    self.assertTrue(str(source[field]).strip(), field)
                identifiers.append(source["id"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertTrue(REQUIRED_SOURCE_IDS.issubset(identifiers))

    def test_human_source_registry_exactly_matches_json(self):
        sources = self.load_json(SOURCE_REGISTRY)
        self.assertTrue(SOURCE_REGISTRY_MD.is_file(), SOURCE_REGISTRY_MD)
        rows = source_rows_from_markdown(
            SOURCE_REGISTRY_MD.read_text(encoding="utf-8")
        )
        self.assertEqual(
            {source["id"]: source for source in sources},
            {row["id"]: row for row in rows},
        )

    def test_human_source_registry_explains_source_controls(self):
        self.assertTrue(SOURCE_REGISTRY_MD.is_file(), SOURCE_REGISTRY_MD)
        text = SOURCE_REGISTRY_MD.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)иерархи")
        self.assertRegex(text, r"(?i)консолид")
        self.assertRegex(text, r"(?i)динамическ")
        self.assertRegex(text, r"(?i)AIP.*NOTAM|NOTAM.*AIP")
        self.assertRegex(text, r"(?i)AEMET")

    def test_regulation_2024_2076_uses_official_publication_date(self):
        sources = {
            source["id"]: source for source in self.load_json(SOURCE_REGISTRY)
        }
        self.assertEqual(
            "OJ от 25.07.2024; применимые положения с 14.08.2024",
            sources["SRC-EURLEX-2024-2076"]["edition"],
        )

    def test_every_registered_source_was_distilled_from_audit_evidence(self):
        sources = self.load_json(SOURCE_REGISTRY)
        evidence = "\n".join(
            path.read_text(encoding="utf-8") for path in AUDIT_FILES
        )
        for source in sources:
            with self.subTest(source=source["id"]):
                self.assertIn(source["url"], evidence)

    def test_term_registry_schema_required_terms_and_unique_stable_ids(self):
        terms = self.load_json(TERMS_REGISTRY)
        self.assertIsInstance(terms, list)
        required_fields = {
            "id",
            "canonical",
            "english",
            "spanish",
            "russian",
            "definition",
            "anchor",
            "defined_in",
        }
        identifiers = []
        anchors = []
        for term in terms:
            with self.subTest(term=term.get("id")):
                self.assertTrue(required_fields.issubset(term))
                self.assertRegex(term["id"], r"^term-[a-z0-9-]+$")
                self.assertEqual(term["id"], term["anchor"])
                for field in required_fields:
                    self.assertTrue(str(term[field]).strip(), field)
                if "abbreviation" in term:
                    self.assertTrue(
                        term["abbreviation"] is None
                        or str(term["abbreviation"]).strip()
                    )
                identifiers.append(term["id"])
                anchors.append(term["anchor"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertEqual(
            REQUIRED_CANONICAL_TERMS,
            {term["canonical"] for term in terms},
        )

    def test_term_definitions_and_abbreviations_match_manifest(self):
        terms = self.load_json(TERMS_REGISTRY)
        self.assertTrue(GLOSSARY.is_file(), GLOSSARY)
        self.assertTrue(ABBREVIATIONS.is_file(), ABBREVIATIONS)
        glossary = GLOSSARY.read_text(encoding="utf-8")
        abbreviations = ABBREVIATIONS.read_text(encoding="utf-8")
        sections = glossary_sections(glossary)
        explicit_term_anchors = {
            next(group for group in match.groups() if group is not None)
            for match in EXPLICIT_HTML_ANCHOR.finditer(glossary)
            if next(group for group in match.groups() if group is not None).startswith(
                "term-"
            )
        }
        self.assertEqual(
            {term["anchor"] for term in terms}, explicit_term_anchors
        )
        for term in terms:
            with self.subTest(term=term["id"]):
                self.assertIn(term["anchor"], sections)
                section = sections[term["anchor"]]
                self.assertIn(f'<a id="{term["anchor"]}"></a>', section)
                for field in (
                    "canonical",
                    "english",
                    "spanish",
                    "russian",
                    "definition",
                ):
                    self.assertIn(str(term[field]), section)
                if term.get("abbreviation"):
                    self.assertIn(str(term["abbreviation"]), abbreviations)
                    self.assertIn(
                        f"glossary.md#{term['anchor']}", abbreviations
                    )
        self.assertEqual(
            {
                (term["abbreviation"], term["anchor"])
                for term in terms
                if term.get("abbreviation")
            },
            abbreviation_links_from_markdown(abbreviations),
        )

    def test_maf_russian_term_uses_multi_axis_wording(self):
        terms = {
            term["canonical"]: term for term in self.load_json(TERMS_REGISTRY)
        }
        self.assertEqual(
            "квалификационная отметка для многоосевого ULM с неподвижным крылом",
            terms["MAF"]["russian"],
        )

    def test_load_factor_definition_states_which_load_is_compared(self):
        terms = {
            term["canonical"]: term for term in self.load_json(TERMS_REGISTRY)
        }
        definition = terms["load factor"]["definition"]
        for required in (
            "аэродинамической нагрузки",
            "тяги",
            "реакции земли",
            "n = L/W",
            "упрощённом установившемся нормальном полёте",
        ):
            with self.subTest(required=required):
                self.assertIn(required, definition)

    def test_defined_in_paths_and_anchors_are_valid(self):
        terms = self.load_json(TERMS_REGISTRY)
        for term in terms:
            with self.subTest(term=term["id"]):
                parsed = urlsplit(term["defined_in"])
                self.assertFalse(parsed.scheme)
                self.assertFalse(parsed.netloc)
                self.assertTrue(parsed.path.startswith("docs/reference/"))
                self.assertEqual(term["anchor"], parsed.fragment)
                path = ROOT / unquote(parsed.path)
                self.assertTrue(path.is_file(), path.relative_to(ROOT))
                self.assertTrue(
                    fragment_exists(
                        path.read_text(encoding="utf-8"), parsed.fragment
                    )
                )

    def test_future_learner_chapters_link_repeated_manifest_terms(self):
        terms = self.load_json(TERMS_REGISTRY)
        violations = []
        for path in learner_chapter_files():
            text = path.read_text(encoding="utf-8")
            for term in terms:
                lines = unlinked_term_occurrences(text, term)
                violations.extend(
                    f"{path.relative_to(ROOT)}:{line}: {term['canonical']}"
                    for line in lines
                )
        self.assertEqual([], violations)


class CourseStructureTests(unittest.TestCase):
    def test_required_entry_points_exist(self):
        for relative_path in ("README.md", "mkdocs.yml", "docs/index.md"):
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_required_source_directory_exists(self):
        self.assertTrue((ROOT / "docs/sources").is_dir(), "docs/sources")

    def test_mkdocs_checks_anchor_fragments(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertRegex(
            config,
            r"(?m)^validation:\s*\n\s+links:\s*\n\s+anchors:\s*warn\s*$",
        )

    def test_mkdocs_excludes_superpowers_documents(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r"(?m)^exclude_docs:\s*\|\s*$")
        self.assertRegex(config, r"(?m)^\s+superpowers/\s*$")

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
                    error = local_reference_error(path, target, is_image)
                    self.assertIsNone(error, error)

    def test_markdown_images_have_alt_text(self):
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for is_image, label, target in markdown_references(text):
                if is_image:
                    with self.subTest(
                        source=path.relative_to(ROOT), target=target
                    ):
                        self.assertTrue(label.strip(), "image alt text is required")


class Task4RoadmapAndAirLawTests(unittest.TestCase):
    def test_task4_chapters_exist_and_are_in_navigation(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for relative_path in TASK4_CHAPTERS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), config)

    def test_every_task4_chapter_has_visible_applicability_table(self):
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path)
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn("## Карта применимости", text)
                self.assertRegex(
                    text,
                    r"(?m)^\|\s*Метка\s*\|\s*Как использовать главу\s*\|$",
                )
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, text)

    def test_normative_subsections_cite_registered_sources(self):
        registered = {
            source["id"] for source in json.loads(SOURCE_REGISTRY.read_text())
        }
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            matches = list(
                re.finditer(r"(?m)^#{2,4}\s+.+\{#norm-[a-z0-9-]+\}\s*$", text)
            )
            self.assertTrue(matches, f"no normative subsection in {relative_path}")
            for index, match in enumerate(matches):
                end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
                section = text[match.end() : end]
                cited = set(re.findall(r"SRC-[A-Z0-9-]+", section))
                with self.subTest(path=relative_path, heading=match.group(0)):
                    self.assertTrue(cited, "normative subsection needs SRC citation")
                    self.assertTrue(cited.issubset(registered), cited - registered)

    def test_course_does_not_claim_automatic_ulm_part_fcl_recognition(self):
        forbidden = re.compile(
            r"(?i)(?:автоматическ(?:ий|ое|ая)\s+"
            r"(?:зачёт|признание|конверсия)|"
            r"ULM\s*(?:=|равен)\s*(?:LAPL|PPL))"
        )
        allowed_negation = re.compile(r"(?i)(?:нет|не|без|отсутствует).{0,35}$")
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            if not path.is_file():
                continue
            text = strip_code(path.read_text(encoding="utf-8"))
            for match in forbidden.finditer(text):
                prefix = text[max(0, match.start() - 40) : match.start()]
                with self.subTest(path=relative_path, phrase=match.group(0)):
                    self.assertRegex(prefix, allowed_negation)

    def test_task4_does_not_teach_cross_border_ulm_procedures(self):
        forbidden_country_procedure = re.compile(
            r"(?i)(?:франц|португал|\bfrance\b|\bportugal\b)"
        )
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            if not path.is_file():
                continue
            with self.subTest(path=relative_path):
                self.assertIsNone(
                    forbidden_country_procedure.search(
                        strip_code(path.read_text(encoding="utf-8"))
                    )
                )

    def test_task4_svgs_are_accessible_original_conceptual_diagrams(self):
        for relative_path in TASK4_SVGS:
            path = ROOT / relative_path
            with self.subTest(path=relative_path):
                self.assertTrue(path.is_file(), relative_path)
                root = ET.parse(path).getroot()
                namespace = "{http://www.w3.org/2000/svg}"
                self.assertEqual(f"{namespace}svg", root.tag)
                self.assertTrue(root.attrib.get("viewBox"))
                self.assertEqual("img", root.attrib.get("role"))
                self.assertIsNotNone(root.find(f"{namespace}title"))
                self.assertIsNotNone(root.find(f"{namespace}desc"))
                self.assertFalse(list(root.iter(f"{namespace}image")))
                words = " ".join(root.itertext()).casefold()
                self.assertIn("концептуальн", words)

    def test_task4_has_at_least_30_unique_explained_questions(self):
        combined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in TASK4_CHAPTERS
            if (ROOT / path).is_file()
        )
        blocks = list(
            re.finditer(
                r"(?ms)^###\s+(Q-(?:START|LAW)-\d{3})\b(.*?)(?=^###\s+Q-(?:START|LAW)-\d{3}\b|\Z)",
                combined,
            )
        )
        identifiers = [match.group(1) for match in blocks]
        self.assertGreaterEqual(len(identifiers), 30)
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for match in blocks:
            with self.subTest(question=match.group(1)):
                body = match.group(2)
                self.assertIn("**Правильный ответ:**", body)
                self.assertIn("**Почему:**", body)
                self.assertIn(
                    "**Почему главный отвлекающий вариант неверен:**",
                    body,
                )


if __name__ == "__main__":
    unittest.main()
