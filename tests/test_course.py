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
    "ICAO-compliant licence",
    "training credit",
    "pre-entry flight assessment",
    "syllabus",
    "supervised solo flight",
    "dual flight instruction",
    "cross-country flight",
    "Head of Training",
    "TMG",
    "AMC",
    "LAPL medical certificate",
    "Class 2 medical certificate",
}

HYBRID_TERMS_REQUIRING_EXPLANATION = (
    "credit",
    "pre-entry",
    "syllabus",
    "supervised solo",
    "dual",
    "cross-country",
    "Head of Training",
    "scope",
    "gate",
    "prior",
    "direct",
    "initial issue",
    "full stop",
    "flight instruction",
    "total aeroplane",
    "rolling",
    "checkout",
    "assessment",
    "TMG",
    "AMC",
    "LAPL medical",
    "Class 2",
)

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
    ignored.extend(
        match.span()
        for match in re.finditer(r"\{[^}\n]*#[^}\n]+\}", clean_text)
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


def mkdocs_nav_paths(text):
    """Return real Markdown nav targets, excluding full-line/inline comments."""
    paths = set()
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        match = re.match(
            r"^\s*-\s+(?:(?:[^:\n]+):\s+)?['\"]?([^'\"\s#][^#]*?\.md)['\"]?\s*$",
            line,
        )
        if match:
            paths.add(match.group(1).strip())
    return paths


def applicability_table_labels(text):
    section = re.search(
        r"(?ms)^##\s+Карта применимости(?:\s+\{#[^}]+\})?\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text,
    )
    if section is None:
        return []
    labels = []
    for line in section.group(1).splitlines():
        match = re.match(r"^\|\s*(.+?)\s*\|", line)
        if match is None:
            continue
        cell = match.group(1).strip()
        linked = re.fullmatch(r"(\[[^]]+\])(?:\[[^]]+\]|\([^)]*\))", cell)
        labels.append(linked.group(1) if linked else cell)
    return labels


def normative_claim_errors(text, registered_sources):
    """Find source-free normative claims without relying on opt-in #norm IDs."""
    # Keep inline-code source IDs (the course deliberately renders SRC-* that way),
    # while excluding fenced examples that are not learner prose.
    clean = strip_fenced_code(text)
    clean = re.split(r"(?m)^##\s+Контрольные вопросы\b", clean, maxsplit=1)[0]
    sections = re.split(r"(?m)(?=^##\s+)", clean)
    cue = re.compile(
        r"(?i)(?:\b(?:обязан(?:а|ы)?|требу(?:ет|ется|ются)|допускается|"
        r"запрещ[её]н(?:а|о|ы)?|долж(?:ен|на|но|ны)|"
        r"действител(?:ен|ьна|ьно|ьны)|разрешает|"
        r"выда[её]тся|призна[её]тся|не\s+превышает|не\s+менее|минимум|"
        r"максимум)\b|\b(?:FCL|SERA)\.\d)"
    )
    errors = []
    for section in sections:
        heading = re.search(r"(?m)^##\s+(.+)$", section)
        if heading is None or not cue.search(section):
            continue
        cited = set(re.findall(r"SRC-[A-Z0-9-]+", section))
        if not cited:
            errors.append(f"{heading.group(1)}: normative claim has no SRC citation")
        elif not cited.issubset(registered_sources):
            errors.append(
                f"{heading.group(1)}: unknown sources {sorted(cited - registered_sources)}"
            )
    return errors


def _sentences(text):
    clean = strip_code(text)
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])(?:\s+|\n+)|\n{2,}", clean)
        if sentence.strip()
    ]


def _tight_negation_before(value, position):
    prefix = value[max(0, position - 28) : position]
    return re.search(r"(?i)\bне(?:\s+[а-яa-z-]+){0,2}\s+$", prefix) is not None


def automatic_recognition_claims(text):
    errors = []
    learner_text = re.sub(
        r"(?ms)^###\s+Красные флаги\b.*?(?=^##\s+|\Z)", "", text
    )
    for sentence in _sentences(learner_text):
        entity = re.search(r"(?i)\b(?:ULM|MAF)\b", sentence)
        target = re.search(r"(?i)\b(?:LAPL|PPL|Part-FCL)\b", sentence)
        marker = re.search(
            r"(?i)(?:автоматическ\w*|полностью|"
            r"без\s+(?:оценк\w*|обучен\w*|экзамен\w*|проверк\w*))",
            sentence,
        )
        predicate = re.search(
            r"(?i)\b(?:засчитыва\w*|призна\w*|конверт\w*|конверси\w*|"
            r"станов\w*|превраща\w*)\b",
            sentence,
        )
        if not all((entity, target, marker, predicate)):
            continue
        prefix = sentence[max(0, predicate.start() - 48) : predicate.start()]
        nominal_conversion = re.match(
            r"(?i)конверси", predicate.group(0)
        ) is not None
        explicitly_negated = _tight_negation_before(
            sentence, predicate.start()
        ) or (
            nominal_conversion
            and re.search(
                r"(?i)\b(?:нет|без)(?:\s+[а-яa-z-]+){0,2}\s+$", prefix
            )
        )
        if not explicitly_negated:
            errors.append(sentence)
    return errors


FOREIGN_COUNTRY = re.compile(
    r"(?i)\b(?:France|Portugal|Italy|Germany|Austria|Switzerland|Belgium|"
    r"Netherlands|Ireland|Poland|Czechia|Croatia|Greece|Morocco|Andorra|"
    r"Франц\w*|Португал\w*|Итал\w*|Герман\w*|Австр\w*|Швейцар\w*|"
    r"Бельг\w*|Нидерланд\w*|Ирланд\w*|Польш\w*|Чех\w*|Хорват\w*|"
    r"Грец\w*|Марокк\w*|Андорр\w*)\b"
)
FOREIGN_OPERATION = re.compile(
    r"(?i)(?:процедур|правил|разрешен|разрешён|permit|permission|authori[sz]ation|"
    r"маршрут|пересеч|вл[её]т|пол[её]т|airspace|AIP|NOTAM|радио|план\s+пол[её]та)"
)

GENERIC_FOREIGN_SCOPE = re.compile(
    r"(?i)(?:вне\s+(?:Испани\w*|испанск\w+\s+воздушн\w+\s+пространств\w*)|"
    r"иностранн\w+|друг\w+\s+государств\w+|международн\w+|"
    r"пересеч\w+\s+границ\w+)"
)
SPAIN_ONLY_DISCLAIMER = re.compile(
    r"(?i)(?:только\s+в\s+Испани\w*|огранич\w+\s+Испани\w*|"
    r"не\s+(?:учит|обучает|описывает|рассматривает|выда[её]т|препода|явля)|"
    r"запрещ\w*)"
)


def cross_border_procedure_errors(text):
    errors = []
    learner_text = re.split(
        r"(?m)^##\s+Контрольные вопросы\b", text, maxsplit=1
    )[0]
    for sentence in _sentences(learner_text):
        if SPAIN_ONLY_DISCLAIMER.search(sentence):
            continue
        destination = FOREIGN_COUNTRY.search(sentence)
        from_spain = re.search(r"(?i)\bиз\s+Испани\w*\b", sentence)
        if FOREIGN_OPERATION.search(sentence) and (
            destination
            or GENERIC_FOREIGN_SCOPE.search(sentence)
            or (from_spain and destination)
        ):
            errors.append(sentence)
    return errors


def _plain_markdown(value):
    value = re.sub(r"\[([^]]+)\](?:\[[^]]+\]|\([^)]*\))", r"\1", value)
    value = re.sub(r"[`*_{}<>]", " ", value)
    return " ".join(value.split())


def _substantive(value, minimum_words=3, minimum_length=12):
    plain = _plain_markdown(value)
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", plain)
    return len(plain) >= minimum_length and len(words) >= minimum_words


def parsed_question_blocks(text):
    headings = list(
        re.finditer(
            r"(?m)^###\s+(Q-(?:START|LAW)-\d{3})\s+—\s+(.+?)"
            r"(?:\s+\{#([a-z][a-z0-9-]*)\})?\s*$",
            text,
        )
    )
    blocks = []
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        next_h2 = re.search(r"(?m)^##\s+", text[match.end() : end])
        if next_h2:
            end = match.end() + next_h2.start()
        blocks.append(
            {
                "id": match.group(1),
                "prompt": match.group(2).strip(),
                "anchor": match.group(3),
                "body": text[match.end() : end],
            }
        )
    return blocks


ABSURD_DISTRACTOR = re.compile(
    r"(?i)(?:купить.{0,20}книж|рекламн(?:ый|ая|ое)\s+сайт|"
    r"автор\s+этого\s+курса|количеств[оа]\s+букв|цвет\s+приложения|"
    r"если\s+нет\s+ветра|подбросить\s+монет|выбрать\s+наугад|"
    r"(?:брос|кинут|подброс|тянут|вытян)\w*.{0,30}(?:кубик|кост\w*|монет|жреб)|"
    r"(?:наугад|случайн\w*|по\s+жребию)|"
    r"цвет.{0,24}назван.{0,24}(?:размер\s+шрифт|шрифт))"
)

TAUTOLOGICAL_EXPLANATION = re.compile(
    r"(?is)(?:ответ[^.!?\n]{0,20}(?:правильн\w*|верн\w*)|"
    r"вариант[^.!?\n]{0,20}невер\w*)[^.!?\n]{0,30}"
    r"потому\s+что[^.!?\n]{0,55}(?:правильн\w*|верн\w*|невер\w*)"
)


def explanation_is_tautological(value):
    plain = _plain_markdown(value)
    if TAUTOLOGICAL_EXPLANATION.search(plain):
        return True
    filler = re.compile(
        r"(?i)^(?:этот|эта|это|ответ|вариант|правильн\w*|верн\w*|"
        r"невер\w*|потому|поскольку|явля\w*|поэтому|услови\w*|вопрос\w*|"
        r"подход\w*|выб\w*|след\w*|именно|лучш\w*|хуж\w*|остальн\w*|"
        r"отверг\w*)$"
    )
    concepts = {
        token.casefold()
        for token in re.findall(r"[A-Za-zА-Яа-яЁё0-9.-]+", plain)
        if len(token) >= 4 and not filler.match(token)
    }
    return len(concepts) < 2


EXPLANATION_SOURCE_OR_RULE = re.compile(
    r"(?i)(?:SRC-[A-Z0-9-]+|\b(?:AESA|EASA|ICAO|AIP|NOTAM|AIS|AIRAC|SERA|VMC)\b|"
    r"\b(?:FCL|SERA|MED)\.[A-Z0-9.()]+|\bRD\s*\d+|"
    r"официальн\w*\s+(?:источник|разъяснен)\w*|\bнорм\w*\b)"
)
EXPLANATION_DOMAIN_CONCEPT = re.compile(
    r"(?i)\b(?:правов\w*|контекст\w*|универсальн\w*|предел\w*|"
    r"знан\w*|модел\w*|математ\w*|максим\w*|индивидуальн\w*|"
    r"решен\w*|зач[её]т\w*|последств\w*|сходств\w*|перекрыт\w*|"
    r"международн\w*|национальн\w*|администр\w*|исключен\w*|"
    r"правил\w*|документ\w*|статус\w*|публикац\w*|компетенц\w*|"
    r"юридическ\w*|актуальн\w*|обязательн\w*|услов\w*|трениров\w*|"
    r"инструктор\w*|требован\w*|полномоч\w*|неконтрол\w*|"
    r"нерегулир\w*|форм\w*|высот\w*|актив\w*|маршрут\w*|"
    r"механизм\w*|восстанов\w*|нал[её]т\w*|обучен\w*|"
    r"срок\w*|дат\w*|полн\w*)\b"
)


def _question_concepts(value):
    stop = re.compile(
        r"(?i)^(?:како\w*|котор\w*|след\w*|нуж\w*|мож\w*|эт\w*|"
        r"ответ\w*|вариант\w*|правильн\w*|невер\w*|почему|потому|"
        r"поскольку|именно|подход\w*|выб\w*|лучш\w*|хуж\w*|"
        r"остальн\w*|перед|после|только|один|одна|одно|одни|"
        r"для|при|или|без|всег\w*|тако\w*)$"
    )
    concepts = set()
    for token in re.findall(r"[A-Za-zА-Яа-яЁё0-9.-]+", _plain_markdown(value)):
        folded = token.casefold().strip(".-")
        if len(folded) < 4 or stop.match(folded):
            continue
        concepts.add(folded if any(character.isdigit() for character in folded) else folded[:4])
    return concepts


def explanation_is_grounded(explanation, context):
    plain = _plain_markdown(explanation)
    if EXPLANATION_SOURCE_OR_RULE.search(plain):
        return True
    if _question_concepts(explanation) & _question_concepts(context):
        return True
    return bool(EXPLANATION_DOMAIN_CONCEPT.search(plain))


def question_block_errors(text):
    errors = []
    prompts = {}
    for block in parsed_question_blocks(text):
        identifier = block["id"]
        prompt = block["prompt"]
        body = block["body"]
        if not _substantive(prompt, minimum_words=4, minimum_length=18):
            errors.append(f"{identifier}: prompt is not substantive")
        normal_prompt = re.sub(r"\W+", " ", _plain_markdown(prompt).casefold()).strip()
        if normal_prompt in prompts:
            errors.append(f"{identifier}: duplicate prompt with {prompts[normal_prompt]}")
        prompts[normal_prompt] = identifier

        options = re.findall(r"(?m)^([A-D])\.\s+(.+?)(?:<br>)?\s*$", body)
        if [letter for letter, _ in options] != list("ABCD"):
            errors.append(f"{identifier}: expected exactly options A-D")
        option_values = [
            re.sub(r"\W+", " ", _plain_markdown(value).casefold()).strip()
            for _, value in options
        ]
        if len(option_values) != len(set(option_values)):
            errors.append(f"{identifier}: duplicate answer options")
        for letter, value in options:
            if not _substantive(value, minimum_words=2, minimum_length=8):
                errors.append(f"{identifier}: option {letter} is not substantive")
            if ABSURD_DISTRACTOR.search(_plain_markdown(value)):
                errors.append(f"{identifier}: option {letter} is an absurd distractor")

        answer = re.search(r"\*\*Правильный ответ:\*\*\s*([A-D])\.", body)
        if answer is None:
            errors.append(f"{identifier}: answer must be A-D")
        why = re.search(
            r"(?ms)\*\*Почему:\*\*\s*(.+?)(?=\n\n\*\*Почему главный отвлекающий)",
            body,
        )
        distractor = re.search(
            r"(?ms)\*\*Почему главный отвлекающий вариант неверен:\*\*\s*(.+?)(?=\n\n|\Z)",
            body,
        )
        if why is None or not _substantive(why.group(1), 5, 28):
            errors.append(f"{identifier}: explanation is not substantive")
        elif explanation_is_tautological(why.group(1)):
            errors.append(f"{identifier}: explanation is tautological")
        if why is not None and answer is not None:
            option_by_letter = dict(options)
            correct_context = f"{prompt} {option_by_letter.get(answer.group(1), '')}"
            if not explanation_is_grounded(why.group(1), correct_context):
                errors.append(f"{identifier}: explanation lacks question-specific concepts")
        if distractor is None or not _substantive(distractor.group(1), 5, 28):
            errors.append(f"{identifier}: distractor explanation is not substantive")
        elif explanation_is_tautological(distractor.group(1)):
            errors.append(f"{identifier}: distractor explanation is tautological")
        if distractor is not None:
            option_by_letter = dict(options)
            distractor_letter = re.match(
                r"\s*([A-D])\b", _plain_markdown(distractor.group(1))
            )
            if distractor_letter:
                distractor_options = option_by_letter.get(distractor_letter.group(1), "")
            elif answer is not None:
                distractor_options = " ".join(
                    value for letter, value in options if letter != answer.group(1)
                )
            else:
                distractor_options = " ".join(value for _, value in options)
            distractor_context = f"{prompt} {distractor_options}"
            if not explanation_is_grounded(distractor.group(1), distractor_context):
                errors.append(
                    f"{identifier}: distractor explanation lacks question-specific concepts"
                )
    return errors


def explicit_atx_heading_errors(text):
    errors = []
    identifiers = []
    for line_number, line in enumerate(strip_fenced_code(text).splitlines(), 1):
        match = ATX_HEADING.match(line)
        if match is None:
            continue
        attribute = ATTRIBUTE_ID.search(match.group(2))
        if attribute is None:
            errors.append(f"line {line_number}: missing explicit English anchor")
            continue
        identifier = attribute.group(1)
        if not re.fullmatch(r"[a-z][a-z0-9-]*", identifier):
            errors.append(f"line {line_number}: invalid explicit English anchor {identifier}")
        identifiers.append(identifier)
    for duplicate in sorted({item for item in identifiers if identifiers.count(item) > 1}):
        errors.append(f"duplicate explicit anchor {duplicate}")
    return errors


def unexplained_hybrid_occurrences(text):
    clean = strip_code(text)
    links, definition_spans = _markdown_link_spans(clean)
    explained_spans = []
    ignored = list(definition_spans)
    for is_image, label_start, label_end, target, start, end in links:
        ignored.extend(((start, label_start), (label_end, end)))
        fragment = unquote(urlsplit(_clean_target(target)).fragment)
        if not is_image and fragment.startswith("term-"):
            explained_spans.append((label_start, label_end))
    errors = []
    for hybrid in HYBRID_TERMS_REQUIRING_EXPLANATION:
        pattern = re.compile(rf"(?i)(?<![\w-]){re.escape(hybrid)}(?![\w-])")
        for match in pattern.finditer(clean):
            if _inside_any(match.start(), ignored + explained_spans):
                continue
            errors.append((clean.count("\n", 0, match.start()) + 1, hybrid))
    return errors


def _bbox_union(boxes):
    boxes = [box for box in boxes if box is not None]
    if not boxes:
        return None
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[0] + box[2] for box in boxes)
    bottom = max(box[1] + box[3] for box in boxes)
    return (left, top, right - left, bottom - top)


def element_bbox(element):
    """Derive a conservative box from real SVG geometry, never data-bbox."""
    tag = element.tag.rsplit("}", 1)[-1]
    if tag == "rect":
        return tuple(
            float(element.attrib.get(name, 0))
            for name in ("x", "y", "width", "height")
        )
    if tag == "line":
        x1, y1, x2, y2 = (
            float(element.attrib.get(name, 0))
            for name in ("x1", "y1", "x2", "y2")
        )
        return (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    if tag == "path":
        numbers = [
            float(item)
            for item in re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", element.attrib.get("d", ""))
        ]
        if len(numbers) < 2 or len(numbers) % 2:
            return None
        points = list(zip(numbers[0::2], numbers[1::2]))
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
    if tag == "text":
        font_size = element.attrib.get("font-size")
        if font_size is None:
            return None
        font_size = float(font_size.removesuffix("px"))
        lines = list(element) or [element]
        boxes = []
        for line in lines:
            content = " ".join("".join(line.itertext()).split())
            if not content:
                continue
            x = float(line.attrib.get("x", element.attrib.get("x", 0)))
            y = float(line.attrib.get("y", element.attrib.get("y", 0)))
            width = len(content) * font_size * 0.56
            anchor = line.attrib.get(
                "text-anchor", element.attrib.get("text-anchor", "start")
            )
            if anchor == "middle":
                x -= width / 2
            elif anchor == "end":
                x -= width
            boxes.append((x, y - font_size, width, font_size * 1.15))
        return _bbox_union(boxes)
    return _bbox_union(element_bbox(child) for child in element)


def bboxes_overlap(first, second):
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


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

    def test_explicit_heading_anchor_metadata_is_not_learner_prose(self):
        term = {"canonical": "ULM", "anchor": "term-ulm"}
        text = "# [ULM](#term-ulm) roadmap {#ulm-roadmap}\n"
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


class Task4ValidatorRegressionTests(unittest.TestCase):
    def test_nav_parser_rejects_commented_fake_entry(self):
        config = """nav:
  # - Fake: 00-start/commented.md
  - Real: 00-start/real.md # visible row
"""
        self.assertEqual({"00-start/real.md"}, mkdocs_nav_paths(config))

    def test_applicability_labels_must_be_actual_table_rows(self):
        text = """## Карта применимости {#applicability}

<!-- [ULM — ОСНОВА] -->
| Метка | Как использовать главу |
|---|---|
| [ИСПАНИЯ] | Только Испания. |

## Далее {#next}
"""
        self.assertEqual(
            ["Метка", "---", "[ИСПАНИЯ]"], applicability_table_labels(text)
        )
        self.assertNotIn("[ULM — ОСНОВА]", applicability_table_labels(text))

    def test_normative_claim_scanner_does_not_depend_on_norm_anchor(self):
        registered = {"SRC-TEST"}
        without_source = """## Правило без специального ID {#rule}

Пилот обязан иметь документ и не менее трёх часов опыта.
"""
        with_source = without_source + "\nИсточник: `SRC-TEST`.\n"
        self.assertTrue(normative_claim_errors(without_source, registered))
        self.assertEqual([], normative_claim_errors(with_source, registered))
        common_obligation = """## Обычная обязанность {#ordinary-duty}

Пилот должен иметь действующую лицензию.
"""
        self.assertTrue(normative_claim_errors(common_obligation, registered))

    def test_automatic_recognition_is_sentence_local_and_requires_tight_negation(self):
        positives = (
            "Часы ULM полностью засчитываются при выдаче PPL.",
            "ULM автоматически превращается в LAPL.",
            "ULM автоматически становится PPL.",
            "ULM автоматически признаётся как LAPL.",
            "ULM признаётся автоматически как LAPL.",
            "ULM конвертируется в PPL без оценки.",
            "ULM конвертируется в LAPL без оценки.",
            "ULM без оценки конвертируется в LAPL.",
            "MAF без обучения конвертируется в Part-FCL.",
            "Это не относится к погоде. Часы ULM полностью засчитываются при выдаче PPL.",
            "Это не очевидно: ULM автоматически становится PPL.",
            "Это не очевидно: ULM признаётся автоматически как LAPL.",
        )
        for value in positives:
            with self.subTest(value=value):
                self.assertTrue(automatic_recognition_claims(value))
        allowed = (
            "Часы ULM не полностью засчитываются при выдаче PPL.",
            "ULM автоматически не превращается в LAPL.",
            "ULM автоматически не становится PPL.",
            "ULM автоматически не признаётся как LAPL.",
            "ULM не признаётся автоматически как LAPL.",
            "ULM не конвертируется в PPL без оценки.",
            "ULM не конвертируется в LAPL без оценки.",
            "ULM без оценки не конвертируется в LAPL.",
            "ULM не является автоматической конверсией в LAPL.",
            "Нет автоматической конверсии ULM в LAPL.",
        )
        for value in allowed:
            with self.subTest(value=value):
                self.assertEqual([], automatic_recognition_claims(value))

    def test_cross_border_guard_covers_multiple_foreign_states(self):
        for value in (
            "Для полёта в Italy запросите местное разрешение.",
            "Перед пересечением границы Германии изучите её AIP.",
            "Маршрут во Францию требует отдельной процедуры.",
            "Для полёта в Марокко запросите местное разрешение.",
            "Перед вылетом в Андорру изучите процедуру пересечения границы.",
        ):
            with self.subTest(value=value):
                self.assertTrue(cross_border_procedure_errors(value))
        self.assertEqual(
            [],
            cross_border_procedure_errors(
                "Курс рассматривает ULM только в Испании и не обучает иностранным процедурам."
            ),
        )
        self.assertEqual(
            [],
            cross_border_procedure_errors(
                "Для полёта в Мадрид запросите диспетчерское разрешение."
            ),
        )
        self.assertTrue(
            cross_border_procedure_errors(
                "Перед полётом из Испании по опубликованному маршруту в Марокко "
                "запросите местное разрешение."
            )
        )

    def test_question_parser_rejects_whimsical_and_tautological_content(self):
        invalid = """### Q-LAW-903 — Как определить применимые границы зоны перед вылетом? {#q-law-903}

A. Подбросить монету перед полётом.<br>
B. Проверить горизонтальные, вертикальные и временные пределы.<br>
C. Цвет, название и размер шрифта.<br>
D. Сверить только координату геометрического центра зоны.

**Правильный ответ:** B.

**Почему:** Этот ответ правильный, потому что он является правильным ответом на вопрос.

**Почему главный отвлекающий вариант неверен:** Этот вариант неверен, потому что он является неверным вариантом ответа.
"""
        errors = "\n".join(question_block_errors(invalid))
        self.assertIn("option A is an absurd distractor", errors)
        self.assertIn("option C is an absurd distractor", errors)
        self.assertIn("explanation is tautological", errors)
        self.assertIn("distractor explanation is tautological", errors)

    def test_question_explanations_must_use_question_specific_concepts(self):
        invalid = """### Q-LAW-904 — Как проверить активность ограниченной зоны перед вылетом? {#q-law-904}

A. Бросить игральный кубик перед выбором маршрута.<br>
B. Проверить текущие AIP и NOTAM для времени маршрута.<br>
C. Спросить пассажира после запуска двигателя.<br>
D. Использовать старый снимок экрана без даты.

**Правильный ответ:** B.

**Почему:** Следует выбрать этот ответ, поскольку именно он подходит лучше остальных.

**Почему главный отвлекающий вариант неверен:** Следует отвергнуть этот вариант, поскольку он хуже остальных.
"""
        errors = "\n".join(question_block_errors(invalid))
        self.assertIn("option A is an absurd distractor", errors)
        self.assertIn("explanation is tautological", errors)
        self.assertIn("explanation lacks question-specific concepts", errors)
        self.assertIn("distractor explanation lacks question-specific concepts", errors)

    def test_svg_geometry_ignores_stale_hand_authored_metadata(self):
        root = ET.fromstring(
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<rect id="terrain" x="0" y="80" width="100" height="20" '
            'data-bbox="0 80 100 20"/>'
            '<rect id="zone" x="10" y="85" width="20" height="10" '
            'data-bbox="10 10 20 10"/>'
            '</svg>'
        )
        elements = {item.attrib["id"]: item for item in root if "id" in item.attrib}
        terrain = element_bbox(elements["terrain"])
        zone = element_bbox(elements["zone"])
        self.assertEqual((10.0, 85.0, 20.0, 10.0), zone)
        self.assertTrue(bboxes_overlap(terrain, zone))

    def test_question_parser_rejects_empty_duplicate_and_absurd_content(self):
        invalid = """### Q-LAW-901 — Пусто {#q-law-901}

A. Одинаковый вариант.<br>
B. Одинаковый вариант.<br>
C. Купить новую книжку.<br>
D. Нет.

**Правильный ответ:** E.

**Почему:** Так.

**Почему главный отвлекающий вариант неверен:** Нет.

### Q-LAW-902 — Пусто {#q-law-902}

A. Первый содержательный вариант.<br>
B. Второй содержательный вариант.<br>
C. Третий содержательный вариант.<br>
D. Четвёртый содержательный вариант.

**Правильный ответ:** A.

**Почему:** Это достаточно полное объяснение правильного ответа на вопрос.

**Почему главный отвлекающий вариант неверен:** Этот вариант противоречит условию и поэтому не подходит.
"""
        errors = "\n".join(question_block_errors(invalid))
        for expected in (
            "prompt is not substantive",
            "duplicate prompt",
            "duplicate answer options",
            "absurd distractor",
            "answer must be A-D",
            "explanation is not substantive",
            "distractor explanation is not substantive",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, errors)

    def test_heading_guard_requires_stable_ascii_identifier(self):
        self.assertTrue(explicit_atx_heading_errors("## Русский заголовок"))
        self.assertTrue(
            explicit_atx_heading_errors("## Русский заголовок {#русский-якорь}")
        )
        self.assertEqual(
            [], explicit_atx_heading_errors("## Русский заголовок {#russian-heading}")
        )


class Task4RoadmapAndAirLawTests(unittest.TestCase):
    def test_task4_chapters_exist_and_are_in_navigation(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        nav_paths = mkdocs_nav_paths(config)
        for relative_path in TASK4_CHAPTERS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), nav_paths)

    def test_every_task4_chapter_has_visible_applicability_table(self):
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path)
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                labels = applicability_table_labels(text)
                self.assertIn("Метка", labels)
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, labels)

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

    def test_normative_claims_are_source_cited_even_without_norm_anchor(self):
        registered = {
            source["id"] for source in json.loads(SOURCE_REGISTRY.read_text())
        }
        violations = []
        for relative_path in TASK4_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            violations.extend(
                f"{relative_path}: {error}"
                for error in normative_claim_errors(text, registered)
            )
        self.assertEqual([], violations)

    def test_course_does_not_claim_automatic_ulm_part_fcl_recognition(self):
        violations = []
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            if not path.is_file():
                continue
            violations.extend(
                f"{relative_path}: {sentence}"
                for sentence in automatic_recognition_claims(
                    path.read_text(encoding="utf-8")
                )
            )
        self.assertEqual([], violations)

    def test_task4_does_not_teach_cross_border_ulm_procedures(self):
        violations = []
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            if not path.is_file():
                continue
            violations.extend(
                f"{relative_path}: {sentence}"
                for sentence in cross_border_procedure_errors(
                    path.read_text(encoding="utf-8")
                )
            )
        self.assertEqual([], violations)

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

    def test_airspace_svg_layering_contrast_and_geometry(self):
        path = ROOT / "docs/assets/diagrams/airspace-structure.svg"
        root = ET.parse(path).getroot()
        by_id = {
            element.attrib["id"]: element
            for element in root.iter()
            if "id" in element.attrib
        }
        for identifier in (
            "terrain-layer",
            "special-use-zone",
            "aerodrome-symbol",
            "warning-panel",
            "warning-text",
        ):
            self.assertIn(identifier, by_id)
        serialised = ET.tostring(root, encoding="unicode")
        self.assertLess(serialised.index('id="terrain-layer"'), serialised.index('id="special-use-zone"'))
        self.assertLess(serialised.index('id="terrain-layer"'), serialised.index('id="aerodrome-symbol"'))
        self.assertEqual("#102a43", by_id["warning-panel"].attrib.get("fill"))
        self.assertEqual("#ffffff", by_id["warning-text"].attrib.get("fill"))
        terrain = element_bbox(by_id["terrain-layer"])
        zone = element_bbox(by_id["special-use-zone"])
        aerodrome = element_bbox(by_id["aerodrome-symbol"])
        self.assertIsNotNone(terrain)
        self.assertIsNotNone(zone)
        self.assertIsNotNone(aerodrome)
        self.assertFalse(bboxes_overlap(terrain, zone))
        self.assertFalse(bboxes_overlap(terrain, aerodrome))

    def test_roadmap_svg_warning_is_wrapped_inside_panel(self):
        path = ROOT / "docs/assets/diagrams/ulm-to-lapl-ppl-roadmap.svg"
        root = ET.parse(path).getroot()
        namespace = "{http://www.w3.org/2000/svg}"
        by_id = {
            element.attrib["id"]: element
            for element in root.iter()
            if "id" in element.attrib
        }
        panel = by_id["roadmap-warning-panel"]
        text = by_id["roadmap-warning-text"]
        tspans = list(text.findall(f"{namespace}tspan"))
        self.assertGreaterEqual(len(tspans), 2)
        self.assertTrue(all((item.text or "").strip() for item in tspans))
        self.assertTrue(all(len((item.text or "").strip()) <= 60 for item in tspans))
        panel_box = element_bbox(panel)
        text_box = element_bbox(text)
        self.assertIsNotNone(panel_box)
        self.assertIsNotNone(text_box)
        px, py, pw, ph = panel_box
        tx, ty, tw, th = text_box
        self.assertGreaterEqual(tx, px)
        self.assertGreaterEqual(ty, py)
        self.assertLessEqual(tx + tw, px + pw)
        self.assertLessEqual(ty + th, py + ph)

    def test_task4_has_four_substantive_unique_questions_per_chapter(self):
        blocks = []
        violations = []
        for relative_path in TASK4_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            chapter_blocks = parsed_question_blocks(text)
            self.assertEqual(4, len(chapter_blocks), relative_path)
            blocks.extend(chapter_blocks)
            violations.extend(
                f"{relative_path}: {error}"
                for error in question_block_errors(text)
            )
        identifiers = [block["id"] for block in blocks]
        self.assertGreaterEqual(len(identifiers), 30)
        self.assertEqual(len(identifiers), len(set(identifiers)))
        prompts = [
            re.sub(r"\W+", " ", _plain_markdown(block["prompt"]).casefold()).strip()
            for block in blocks
        ]
        self.assertEqual(len(prompts), len(set(prompts)))
        self.assertEqual([], violations)

    def test_q_start_006_is_not_duplicate_of_direct_ppl_credit_question(self):
        text = (ROOT / TASK4_CHAPTERS[1]).read_text(encoding="utf-8")
        block = next(
            item for item in parsed_question_blocks(text) if item["id"] == "Q-START-006"
        )
        self.assertNotRegex(_plain_markdown(block["prompt"]), r"(?i)PPL|прям")

    def test_all_task4_headings_have_stable_explicit_english_anchors(self):
        violations = []
        for relative_path in TASK4_CHAPTERS:
            violations.extend(
                f"{relative_path}: {error}"
                for error in explicit_atx_heading_errors(
                    (ROOT / relative_path).read_text(encoding="utf-8")
                )
            )
        self.assertEqual([], violations)

    def test_hybrid_english_is_linked_to_an_explanation(self):
        violations = []
        for relative_path in TASK4_CHAPTERS:
            path = ROOT / relative_path
            violations.extend(
                f"{relative_path}:{line}: {term}"
                for line, term in unexplained_hybrid_occurrences(
                    path.read_text(encoding="utf-8")
                )
            )
        self.assertEqual([], violations)

    def test_beginner_transition_terms_are_explained_in_russian_at_first_use(self):
        roadmap = (ROOT / TASK4_CHAPTERS[1]).read_text(encoding="utf-8")
        transition = (ROOT / TASK4_CHAPTERS[8]).read_text(encoding="utf-8")
        expected = {
            "roadmap TMG": (roadmap, "туристических мотопланёрах ([TMG][tmg])"),
            "roadmap AMC": (
                roadmap,
                "приемлемые способы подтверждения соответствия ([AMC][amc])",
            ),
            "roadmap LAPL medical": (
                roadmap,
                "медицинское свидетельство LAPL ([LAPL medical certificate][lapl-medical])",
            ),
            "roadmap Class 2": (
                roadmap,
                "медицинским свидетельством класса 2 ([Class 2 medical certificate][class-2-medical])",
            ),
            "transition TMG": (transition, "туристическом мотопланёре ([TMG][tmg])"),
            "transition LAPL medical": (
                transition,
                "медицинское свидетельство LAPL ([LAPL medical certificate][lapl-medical])",
            ),
            "transition Class 2": (
                transition,
                "медицинское свидетельство класса 2 ([Class 2 medical certificate][class-2-medical])",
            ),
        }
        for label, (text, phrase) in expected.items():
            with self.subTest(term=label):
                self.assertIn(phrase, text)

    def test_index_prominently_links_to_first_lesson(self):
        text = (ROOT / "docs/index.md").read_text(encoding="utf-8")
        before_order = text.split("## Порядок обучения", 1)[0]
        self.assertRegex(
            before_order,
            r"(?i)\[[^]]*(?:начать|перв|урок)[^]]*\]\(00-start/01-how-to-study\.md\)",
        )

    def test_legal_pinpoints_and_scope_match_reviewed_sources(self):
        audit = (ROOT / "docs/sources/audit-spain-2026.md").read_text(
            encoding="utf-8"
        )
        expected_rows = {
            "ES-ULM-TRN-001": "Art. 5.3;",
            "ES-ULM-TRN-002": "Art. 5.4;",
            "ES-ULM-OPS-003": "Art. 4.1(a)–(b);",
            "ES-ULM-OPS-004": "Art. 4.1(c);",
            "ES-ULM-OPS-005": "Art. 4.1(e);",
            "ES-ULM-OPS-006": "Art. 4.1(d);",
        }
        for row_id, pinpoint in expected_rows.items():
            row = next(line for line in audit.splitlines() if f"| {row_id} |" in line)
            with self.subTest(row=row_id):
                self.assertIn(pinpoint, row)
        duplicate_row = next(
            line for line in audit.splitlines() if "| ES-FCL-ULM-003 |" in line
        )
        self.assertRegex(duplicate_row, r"(?i)обладател.*Part-FCL|Part-FCL.*обладател")

        medical = (ROOT / TASK4_CHAPTERS[2]).read_text(encoding="utf-8")
        self.assertIn("art. 6.3(c)", medical)
        airspace = (ROOT / TASK4_CHAPTERS[6]).read_text(encoding="utf-8")
        self.assertIn("art. 4.1(d)", airspace)
        condition = "когда это требуется классом, характером операции и текущим AIP"
        self.assertIn(condition, _plain_markdown(airspace))
        self.assertIn(condition, audit)

        occurrence = (ROOT / TASK4_CHAPTERS[7]).read_text(encoding="utf-8")
        self.assertRegex(
            occurrence,
            r"(?is)рекомендаци[яи]\s+курса.{0,220}не\s+устанавливает.{0,80}"
            r"персональн(?:ую|ой)\s+(?:обязанность|норму)\s+(?:для\s+)?ученика",
        )

    def test_supervised_solo_means_the_student_is_the_only_person_on_board(self):
        glossary = GLOSSARY.read_text(encoding="utf-8")
        glossary_section = glossary.split(
            '<a id="term-supervised-solo-flight"></a>', 1
        )[1].split('<a id="term-dual-flight-instruction"></a>', 1)[0]
        terms = json.loads(TERMS_REGISTRY.read_text(encoding="utf-8"))
        registry_definition = next(
            term["definition"]
            for term in terms
            if term["canonical"] == "supervised solo flight"
        )
        for definition in (glossary_section, registry_definition):
            with self.subTest(definition=definition):
                self.assertRegex(
                    definition,
                    r"(?i)единственн\w+\s+(?:лиц\w+|человек\w+).{0,30}на\s+борту",
                )
                self.assertRegex(definition, r"(?i)без\s+пассажир|наблюдател")

    def test_duplicate_logbook_faq_scope_names_the_direct_access_holder(self):
        lesson = (ROOT / TASK4_CHAPTERS[0]).read_text(encoding="utf-8")
        question = next(
            item for item in parsed_question_blocks(lesson) if item["id"] == "Q-START-003"
        )
        prompt = _plain_markdown(question["prompt"])
        self.assertRegex(prompt, r"(?is)обладател.*Part-FCL.*прям.*испан.*ULM")

        audit = (ROOT / "docs/sources/audit-lapl-transition.md").read_text(
            encoding="utf-8"
        )
        row = next(line for line in audit.splitlines() if "| LTR-ULM-006 |" in line)
        self.assertRegex(row, r"(?is)обладател.*Part-FCL.*прям.*испан.*ULM")


if __name__ == "__main__":
    unittest.main()
