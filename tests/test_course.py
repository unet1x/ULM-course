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
TASK5_CHAPTERS = (
    "docs/02-human-performance/01-physiology.md",
    "docs/02-human-performance/02-vision-hearing-orientation.md",
    "docs/02-human-performance/03-stress-fatigue-medication.md",
    "docs/02-human-performance/04-adm-tem-communication.md",
)
TASK5_SVGS = (
    "docs/assets/diagrams/hypoxia-response.svg",
    "docs/assets/diagrams/decision-loop.svg",
)
TASK6_CHAPTERS = (
    "docs/03-meteorology/01-atmosphere-pressure-temperature.md",
    "docs/03-meteorology/02-wind-turbulence-mountain-coast.md",
    "docs/03-meteorology/03-water-clouds-visibility.md",
    "docs/03-meteorology/04-air-masses-fronts-systems.md",
    "docs/03-meteorology/05-hazards-thunderstorm-icing.md",
    "docs/03-meteorology/06-metar-taf-sigmet-charts.md",
    "docs/03-meteorology/07-spain-go-no-go.md",
)
TASK6_SVGS = (
    "docs/assets/diagrams/fronts-and-pressure.svg",
    "docs/assets/diagrams/thunderstorm-hazards.svg",
    "docs/assets/diagrams/metar-taf-decoder.svg",
)
TASK7_CHAPTERS = (
    "docs/04-communications/01-radio-basics-rtc.md",
    "docs/04-communications/02-message-structure.md",
    "docs/04-communications/03-departure-en-es.md",
    "docs/04-communications/04-enroute-arrival-en-es.md",
    "docs/04-communications/05-uncontrolled-aerodrome.md",
    "docs/04-communications/06-urgency-distress-radio-failure.md",
)
TASK7_REFERENCE = "docs/reference/checklists-radio.md"
TASK7_SVG = "docs/assets/diagrams/radio-message-flow.svg"
TASK8_CHAPTERS = (
    "docs/05-navigation/01-earth-time-directions.md",
    "docs/05-navigation/02-charts-airspace.md",
    "docs/05-navigation/03-heading-track-wind.md",
    "docs/05-navigation/04-dead-reckoning-flight-log.md",
    "docs/05-navigation/05-vor-dme-adf-ppl.md",
    "docs/05-navigation/06-gnss-and-cross-check.md",
    "docs/05-navigation/07-lost-diversion-border.md",
)
TASK8_REFERENCE = "docs/reference/templates-flight-log.md"
TASK8_SVGS = (
    "docs/assets/diagrams/wind-triangle.svg",
    "docs/assets/diagrams/vor-geometry.svg",
    "docs/assets/diagrams/sample-route.svg",
    "docs/assets/diagrams/chart-symbols-gen23.svg",
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
    "ad.easa.europa.eu",
    "eur-lex.europa.eu",
    "www.boe.es",
    "www.seguridadaerea.gob.es",
    "sede.seguridadaerea.gob.es",
    "aip.enaire.es",
    "www.aemet.es",
    "www.faa.gov",
    "www.aviation.govt.nz",
    "egnos.gsc-europa.eu",
    "www.cdc.gov",
    "ama.aemet.es",
    "cloudatlas.wmo.int",
    "store.icao.int",
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
    "SRC-AESA-MAF-SYLLABUS-ED01",
    "SRC-AESA-ULM-LEARNING-OBJECTIVES-GU09-ED01",
    "SRC-AESA-ULM-QUESTION-BANKS",
    "SRC-AESA-LAPL-PPL-PROCEDURES",
    "SRC-ENAIRE-AIP-ESPANA",
    "SRC-AEMET-AVIATION",
    "SRC-EASA-HYPOXIA-2016",
    "SRC-EASA-SIB-2020-01R1",
    "SRC-EASA-EGAST-GA2",
    "SRC-FAA-PHAK-25C-CH17",
    "SRC-FAA-RISK-MANAGEMENT-2A",
    "SRC-FAA-MEDICATIONS-2017",
    "SRC-FAA-HEARING-NOISE-98-3",
    "SRC-FAA-FATIGUE-2020",
    "SRC-CDC-CO-CLINICAL",
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
    "hypoxia",
    "hyperventilation",
    "carbon monoxide (CO)",
    "spatial disorientation",
    "situational awareness",
    "threat and error management (TEM)",
    "aeronautical decision-making (ADM)",
    "IMSAFE",
    "PAVE",
    "personal minima",
    "external pressure",
    "Part-MED",
    "aeromedical examiner (AME)",
    "over-the-counter medication (OTC)",
    "crew resource management (CRM)",
    "non-technical skills (NTS)",
    "Human performance",
    "go/no-go",
    "continue/divert",
    "AVIATE–NAVIGATE–COMMUNICATE",
    "general aviation (GA)",
    "International Standard Atmosphere (ISA)",
    "flight level (FL)",
    "QFE",
    "CAVOK",
    "SPECI",
    "TREND",
    "SIGMET",
    "AIRMET",
    "GAMET",
    "Aeronautical Meteorological Self-service (AMA)",
    "density altitude",
    "wind shear",
    "VFR into IMC (VFR2IMC)",
    "pressure altitude",
    "transition altitude",
    "transition level",
    "anabatic flow",
    "katabatic flow",
    "mountain wave",
    "rotor",
    "lee downdraft",
    "headwind component",
    "crosswind component",
    "surface wind",
    "significant weather chart for low-level flights (SWL)",
    "radiotelephony (R/T)",
    "air traffic control (ATC)",
    "aerodrome flight information service (AFIS)",
    "air-to-air (A/A)",
    "readback",
    "acknowledgement",
    "callsign",
    "plain language",
    "listening watch",
    "distress",
    "urgency",
    "communication failure",
    "secondary surveillance radar (SSR)",
    "language proficiency endorsement",
    "dead reckoning (DR)",
    "true course (TC)",
    "magnetic course (MC)",
    "true heading (TH)",
    "magnetic heading (MH)",
    "true airspeed (TAS)",
    "compass deviation (DEV)",
    "compass heading (CH)",
    "wind correction angle (WCA)",
    "groundspeed (GS)",
    "estimated time of arrival (ETA)",
    "global navigation satellite system (GNSS)",
    "receiver autonomous integrity monitoring (RAIM)",
    "satellite-based augmentation system (SBAS)",
    "VHF omnidirectional range (VOR)",
    "distance measuring equipment (DME)",
    "automatic direction finder (ADF)",
    "non-directional beacon (NDB)",
    "European Geostationary Navigation Overlay Service (EGNOS)",
    "Coordinated Universal Time (UTC)",
    "air traffic services (ATS)",
    "Aeronautical Information Regulation and Control (AIRAC)",
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
    "go/no-go",
    "continue/divert",
    "Human performance",
    "AVIATE",
    "NAVIGATE",
    "COMMUNICATE",
    "intercom",
    "the leans",
    "somatogravic illusion",
    "graveyard spiral",
    "black-hole approach",
    "instrument rating",
    "instrument recovery",
    "Part-MED",
    "medical",
    "AME",
    "OTC",
    "scope",
    "non-technical skills",
    "error management",
    "safety promotion",
    "TEM",
    "CRM",
    "GA",
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
            r"(?m)^###\s+(Q-(?:START|LAW|HP|MET|RTC|NAV)-\d{3})\s+—\s+(.+?)"
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
    r"групп\w*\s+G.{0,30}только\s+(?:к\s+)?температур|"
    r"G\s+публику\w*.{0,30}после\s+(?:завершения\s+)?пол[её]т|"
    r"морск\w+\s+бриз.{0,30}только\s+на\s+морск\w+\s+суд|"
    r"длин\w+\s+строк\w*.{0,20}(?:без\s+пробел|сообщен)|"
    r"SPECI.{0,35}(?:семь|7)\s+дн|"
    r"средн\w+\s+арифметическ\w*.{0,35}(?:предел|значен)|"
    r"предел.{0,35}выбира\w+\s+пассажир|"
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
    r"знан\w*|математ\w*|максим\w*|индивидуальн\w*|"
    r"решен\w*|зач[её]т\w*|последств\w*|сходств\w*|перекрыт\w*|"
    r"международн\w*|национальн\w*|администр\w*|исключен\w*|"
    r"правил\w*|документ\w*|статус\w*|публикац\w*|компетенц\w*|"
    r"юридическ\w*|актуальн\w*|обязательн\w*|услов\w*|трениров\w*|"
    r"инструктор\w*|требован\w*|полномоч\w*|неконтрол\w*|"
    r"нерегулир\w*|форм\w*|высот\w*|актив\w*|маршрут\w*|"
    r"восстанов\w*|нал[её]т\w*|обучен\w*|"
    r"срок\w*|дат\w*|полн\w*)\b"
)


def _question_concepts(value):
    stop = re.compile(
        r"(?i)^(?:како\w*|котор\w*|след\w*|нуж\w*|мож\w*|эт\w*|"
        r"ответ\w*|вариант\w*|правильн\w*|невер\w*|почему|потому|"
        r"поскольку|именно|подход\w*|выб\w*|лучш\w*|хуж\w*|"
        r"остальн\w*|перед|после|только|один|одна|одно|одни|"
        r"механизм\w*|модел\w*|основан\w*|"
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


def human_performance_safety_errors(text):
    """Reject unsafe claims using sentence-local features and predicate negation."""
    errors = []
    for sentence in _sentences(text):
        plain = _plain_markdown(sentence)

        coordinator = re.compile(r"(?i)(?:;\s*|,\s*(?:а|но|зато|и)\s+)")

        def predicate_is_positive(match):
            """Negation belongs to this predicate, not another coordinated one."""
            starts = [boundary.end() for boundary in coordinator.finditer(plain, 0, match.start())]
            clause_start = starts[-1] if starts else 0
            next_boundary = coordinator.search(plain, match.end())
            clause_end = next_boundary.start() if next_boundary else len(plain)
            prefix = plain[clause_start:match.start()]
            suffix = plain[match.end():clause_end]
            direct_negation = re.search(
                r"(?i)(?:\bникогда\s+не|\bне(?:\s+(?:всегда|обязательно|может))?)"
                r"(?:\s+[а-яёa-z-]+){0,3}\s*$",
                prefix,
            )
            negated_governing_predicate = re.search(
                r"(?i)\bне\s+означа\w*(?:\s+автоматическ\w*)?\s*,?\s*"
                r"(?:что\s+)?(?:\s*[а-яёa-z-]+){0,6}\s*$",
                prefix,
            )
            quoted_refutation = (
                re.search(r"(?i)\bмиф\s*:", plain[clause_start:match.start()])
                and (
                    re.search(r"(?i)(?:неверн|ошибочн)", suffix)
                    or re.search(
                        r"(?i)индивидуал\w*\s+восприимчив\w*\s+различ",
                        plain[match.end():],
                    )
                )
            )
            return not (direct_negation or negated_governing_predicate or quoted_refutation)

        feature_claims = (
            (r"гипокси", r"ниже\s+\d[\d\s]*\s*(?:ft|фут)", r"невозмож"),
            (r"действующ\w+\s+(?:medical|медицинск\w+\s+свидетельств)", r"сегодня", r"(?:гарантиру|означа).{0,20}год"),
            (r"(?:OTC|безрецептурн\w+).{0,15}(?:препарат|лекарств)?", r"", r"безопас"),
            (r"(?:детектор|пульсоксиметр)", r"", r"гарантиру\w+\s+безопас"),
            (r"личн\w+\s+минимум", r"(?:AFM|POH|предел|огранич)", r"заменя"),
            (r"(?:законн\w+|легальн\w+)\s+VMC", r"(?:пилот|тип|самол[её]т)", r"(?:подход|пригод)"),
            (r"гипокси", r"гипервентиляц", r"легко\s+отлич"),
            (r"кофеин", r"усталост", r"(?:лечит|устраняет|вылечивает)"),
            (r"(?:CO|угарн\w+\s+газ)", r"предупреждающ\w+\s+запах", r"(?:имеет|обладает|есть)"),
            (r"ULM", r"всегда\s+летает\s+низко", r"гипокси\w+\s+не\s+важн"),
        )
        unsafe_predicate_found = False
        for first, second, predicate in feature_claims:
            if re.search(first, plain, re.IGNORECASE) and (
                not second or re.search(second, plain, re.IGNORECASE)
            ):
                for match in re.finditer(predicate, plain, re.IGNORECASE):
                    if predicate_is_positive(match):
                        errors.append(sentence)
                        unsafe_predicate_found = True
                        break
            if unsafe_predicate_found:
                break
        universal_limits = (
            r"(?i)(?:всегда|каждый\s+пилот).{0,30}(?:спать|сон).{0,12}\d+\s*час",
            r"(?i)(?:после\s+алкоголя|алкогол\w+).{0,30}(?:ждать|достаточно).{0,12}\d+\s*час",
            r"(?i)(?:люб\w+|все)\s+(?:ULM|самол[её]т).{0,30}(?:шум|вибрац|холод|низк\w+\s+инерц)",
        )
        if any(re.search(pattern, plain) for pattern in universal_limits):
            universal_refutation = re.search(
                r"(?i)(?:нельзя\s+утверждать|^\s*(?:считать|приписывать)|"
                r"\bне\s+(?:каждый|любой|все)\b)",
                plain,
            )
            if not universal_refutation:
                errors.append(sentence)
        if re.search(r"(?i)\b(?:диагностируйте|назначьте\s+лечение|примите\s+дозу)\b", plain):
            errors.append(sentence)
    return errors


def human_evidence_adjacency_errors(text, registered_sources):
    """Require claim-specific registered evidence in the same paragraph/table row."""
    rules = (
        (
            re.compile(r"(?i)(?:дополнительн\w+\s+кислород|высот\w+\s+кабин).{0,100}(?:треб|\d[\d\s]*\s*ft)"),
            {"SRC-BOE-RD-765-2022"},
        ),
        (
            re.compile(r"(?i)гипервентиляц.{0,160}(?:углекисл|признак|дыхани|покалыван|головокруж)"),
            {"SRC-FAA-PHAK-25C-CH17"},
        ),
        (
            re.compile(r"(?i)(?:MED\.A\.020|снижени\w+\s+медицинск\w+\s+годност)"),
            {"SRC-EASA-AIRCREW-2026"},
        ),
        (
            re.compile(r"(?i)(?:IMSAFE|PAVE).{0,120}(?:Illness|Pilot|мнемоник|группир)"),
            {"SRC-FAA-RISK-MANAGEMENT-2A"},
        ),
        (
            re.compile(r"(?i)(?:CO|угарн\w+\s+газ).{0,150}(?:детектор|без\s+запах|выхлоп|признак)"),
            {"SRC-EASA-SIB-2020-01R1"},
        ),
        (
            re.compile(r"(?i)пульсоксиметр.{0,180}(?:CO|угарн|карбоксигемоглобин)"),
            {"SRC-CDC-CO-CLINICAL"},
        ),
        (
            re.compile(r"(?i)(?:центральн\w+\s+област\w+\s+сетчатк|перифер\w+\s+зрен|сканирован\w+\s+взгляд)"),
            {"SRC-FAA-PHAK-25C-CH17"},
        ),
        (
            re.compile(r"(?i)(?:полукружн\w+\s+канал|отолитов\w+\s+орган|вестибуляр\w+\s+иллюз)"),
            {"SRC-FAA-PHAK-25C-CH17"},
        ),
        (
            re.compile(r"(?i)(?:шум.{0,100}(?:маскир|реч|усталост|ошибк)|защит\w+слуха)"),
            {"SRC-FAA-HEARING-NOISE-98-3"},
        ),
        (
            re.compile(r"(?i)усталост\w*\s*(?:—|:|может|способн\w*)?\s*"
                       r"(?:сниж|ухудш|вед|вызыв|сопровожд|деград).{0,100}"
                       r"(?:вниман|работоспособ|концентр|ошибк|сужден|физическ|умствен)"),
            {"SRC-FAA-PHAK-25C-CH17", "SRC-FAA-FATIGUE-2020"},
        ),
        (
            re.compile(r"(?i)стресс.{0,150}(?:вниман|реакц|действ|ошиб|нагруз)"),
            {"SRC-FAA-PHAK-25C-CH17", "SRC-FAA-FATIGUE-2020"},
        ),
        (
            re.compile(r"(?i)алкогол.{0,150}(?:сужден|координац|вниман|сон|реакц)"),
            {"SRC-FAA-PHAK-25C-CH17"},
        ),
        (
            re.compile(r"(?i)ситуационн\w+\s+осведомл.{0,180}(?:восприн|понят|прогноз|решен)"),
            {"SRC-EASA-AIRCREW-2026", "SRC-EASA-EGAST-GA2"},
        ),
        (
            re.compile(r"(?i)(?:CRM|управлен\w+ресурс\w+экипаж).{0,180}(?:ресурс|коммуникац|ошиб|однопилот)"),
            {"SRC-EASA-AIRCREW-2026"},
        ),
        (
            re.compile(r"(?i)личн\w+\s+минимум.{0,180}(?:строж|границ|замен|огранич)"),
            {"SRC-FAA-RISK-MANAGEMENT-2A"},
        ),
        (
            re.compile(r"(?i)PART-FCL.{0,180}LAPL.{0,180}PPL.{0,180}(?:одинаков\w+\s+теоретическ\w+\s+глубин|программ\w+\s+PPL)"),
            {"SRC-EASA-AIRCREW-2026"},
        ),
    )
    clean = strip_fenced_code(text)
    clean = re.sub(
        r"(?ms)^##\s+(?:Результаты\s+обучения|Краткий\s+конспект|"
        r"Контрольные\s+вопросы|Источники)\b.*?(?=^##\s|\Z)",
        "",
        clean,
    )
    blocks = [
        block.strip()
        for block in re.split(r"\n\s*\n|(?=^\|)", clean, flags=re.MULTILINE)
        if block.strip()
    ]
    errors = []
    for block in blocks:
        plain = _plain_markdown(block)
        if re.fullmatch(r"#{1,6}\s+.*", plain.strip()):
            continue
        cited = set(re.findall(r"SRC-[A-Z0-9-]+", block))
        for cue, required in rules:
            if cue.search(plain) and not cited.intersection(required):
                errors.append(f"claim needs one of {sorted(required)}: {plain[:100]}")
        unknown = cited - registered_sources
        if unknown:
            errors.append(f"unknown sources {sorted(unknown)}")
    return errors


def unexplained_hybrid_occurrences(text):
    # Inline code formatting does not explain an English/Spanish aviation term.
    clean = strip_fenced_code(text)
    links, definition_spans = _markdown_link_spans(clean)
    explained_spans = []
    ignored = list(definition_spans)
    ignored.extend(
        match.span()
        for match in re.finditer(r"\{[^}\n]*#[^}\n]+\}", clean)
    )
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


def unexplained_english_phrase_occurrences(text):
    """Find English learner prose, including short fragments and code spans."""
    clean = strip_fenced_code(text)
    product_table_lines = {
        line_number
        for line_number, line in enumerate(clean.splitlines(), 1)
        if re.match(
            r"^\|\s*(?:\[(?:METAR|TAF|SPECI|AIRMET|GAMET|SWL)\]"
            r"(?:\[[^\]]+\]|\([^)]*\))|(?:METAR|TAF|SPECI|AIRMET|GAMET|SWL))\s*\|",
            line,
        )
    }
    errors = []
    for line_number, line in enumerate(clean.splitlines(), 1):
        if re.match(r"^\s*\[[^\]]+\]:", line):
            continue
        for match in re.finditer(
            r"\[([^\]\n]+)\](?:\[[^\]\n]*\]|\([^\n)]+\))",
            line,
        ):
            label = match.group(1)
            if re.search(r"(?<![A-Za-z])[a-z][a-z'-]{3,}(?![A-Za-z])", label) and not re.search(
                r"[А-Яа-яЁё]", label
            ):
                errors.append((line_number, " ".join(label.split())))
    clean = re.sub(
        r"\((?:English|EN):[^)\n]+(?:español|ES):[^)\n]+\)",
        " ",
        clean,
        flags=re.IGNORECASE,
    )
    clean = re.sub(
        r"\((?:español|ES):[^)\n]+\)",
        " ",
        clean,
        flags=re.IGNORECASE,
    )
    def keep_only_prose_code(match):
        value = match.group(1)
        lower_words = {
            word.casefold()
            for word in re.findall(r"(?<![A-Za-z])([A-Za-z]+)(?![A-Za-z])", value)
            if word.islower()
        }
        if not lower_words or lower_words.issubset({"cos", "sin", "ft"}):
            return " "
        return value

    clean = re.sub(r"`([^`\n]+)`", keep_only_prose_code, clean)
    clean = re.sub(
        r"!?\[[^\]\n]+\](?:\[[^\]\n]*\]|\([^\n)]+\))",
        " ",
        clean,
    )
    clean = re.sub(r"https?://\S+|SRC-[A-Z0-9-]+", " ", clean)
    clean = re.sub(r"<[^>\n]+>", " ", clean)
    pattern = re.compile(
        r"(?<![A-Za-z])(?:(?:[A-Za-z][A-Za-z'-]*\s+){2,}"
        r"[A-Za-z][A-Za-z'-]*|(?:[a-z][a-z'-]{1,}\s+)*[a-z][a-z'-]{3,})"
        r"(?![A-Za-z])"
    )
    for line_number, line in enumerate(clean.splitlines(), 1):
        if line_number in product_table_lines:
            continue
        if re.match(r"^\s*#{1,6}\s+", line):
            continue
        if re.match(r"^\s*\[[^\]]+\]:", line):
            continue
        if re.match(r"^\s*-\s+\*\*(?:Canonical|English|Español|Русский|Сокращение):\*\*", line):
            continue
        for match in pattern.finditer(line):
            errors.append((line_number, " ".join(match.group(0).split())))
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

    def test_lapl_holder_and_exam_only_theory_credit_are_distinguished(self):
        lesson = (ROOT / TASK4_CHAPTERS[8]).read_text(encoding="utf-8")
        theory = lesson.split("## Теория и экзамены", 1)[1].split(
            "## [LAPL(A)][lapl] → [PPL(A)][ppl]", 1
        )[0]
        self.assertRegex(
            theory,
            r"(?is)обладател\w*\s+уже\s+выданн\w+\s+.*LAPL.*той\s+же\s+"
            r"категори.*полн\w+\s+зач[её]т.*не\s+ограничен.*24-месяч",
        )
        self.assertRegex(
            theory,
            r"(?is)без\s+выданн\w+\s+.*LAPL.*только\s+сдал.*теоретическ\w+\s+"
            r"экзамен.*FCL\.025\(c\).*24\s+месяц",
        )

        question = next(
            item for item in parsed_question_blocks(lesson) if item["id"] == "Q-LAW-023"
        )
        options = re.findall(
            r"(?m)^([A-D])\.\s+(.+?)(?:<br>)?\s*$", question["body"]
        )
        self.assertEqual(list("ABCD"), [letter for letter, _ in options])
        question_text = _plain_markdown(question["prompt"] + question["body"])
        self.assertRegex(question_text, r"(?is)выданн\w+\s+LAPL.*только\s+сдал")
        self.assertRegex(question_text, r"(?is)FCL\.025\(c\).*24\s+месяц")

        audit = (ROOT / "docs/sources/audit-lapl-transition.md").read_text(
            encoding="utf-8"
        )
        row = next(line for line in audit.splitlines() if "| LTR-PPL-009 |" in line)
        self.assertRegex(row, r"(?i)обладател\w*\s+выданн\w+\s+LAPL")
        self.assertRegex(row, r"(?i)без\s+выданн\w+\s+LAPL.*FCL\.025\(c\)")

        sources = {
            source["id"]: source
            for source in json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
        }
        scope = sources["SRC-EURLEX-2024-2076"]["scope"]
        self.assertRegex(scope, r"(?i)обладател\w*\s+выданн\w+\s+LAPL")
        self.assertRegex(scope, r"(?i)без\s+выданн\w+\s+LAPL.*FCL\.025\(c\)")

        false_holder_expiry = re.compile(
            r"(?is)(?:обладател\w*\s+(?:уже\s+)?выданн\w+\s+LAPL|"
            r"(?<!без\s)выданн\w+\s+LAPL).{0,140}(?:только|лишь)\s+"
            r"(?:пока|до).{0,100}"
            r"(?:FCL\.025\(c\)|24[- ]месяч)"
        )
        for label, text in (
            ("learner lesson", theory),
            ("source audit", audit),
            ("source scope", scope),
        ):
            with self.subTest(document=label):
                self.assertNotRegex(text, false_holder_expiry)

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


class Task5HumanPerformanceTests(unittest.TestCase):
    def test_lapl_and_ppl_use_the_same_human_performance_theory_depth(self):
        for relative_path in TASK5_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            applicability = text.split("## Карта применимости", 1)[1].split("## Теория", 1)[0]
            self.assertRegex(
                _plain_markdown(applicability),
                r"(?is)LAPL.*PPL.*одинаков\w+\s+теоретическ\w+\s+глубин|"
                r"LAPL.*использует\s+программу\s+PPL",
                relative_path,
            )
            self.assertNotRegex(applicability, r"(?i)PPL.{0,35}(?:углуб|добавляется)")

    def test_task5_hybrid_terms_are_explained_across_all_learner_chapters(self):
        violations = []
        for path in learner_chapter_files():
            violations.extend(
                f"{path.relative_to(ROOT)}:{line}: {term}"
                for line, term in unexplained_hybrid_occurrences(
                    path.read_text(encoding="utf-8")
                )
            )
        self.assertEqual([], violations)
        probe = "Решение go/no-go; затем continue/divert, CRM, GA и TEM."
        self.assertGreaterEqual(len(unexplained_hybrid_occurrences(probe)), 5)
        self.assertEqual(
            [],
            unexplained_hybrid_occurrences("### Управление угрозами {#tem}"),
        )

    def test_co_definition_requires_response_to_one_signal_and_distinguishes_detector(self):
        terms = {term["canonical"]: term for term in json.loads(TERMS_REGISTRY.read_text())}
        definition = terms["carbon monoxide (CO)"]["definition"]
        self.assertRegex(definition, r"(?is)активн\w+\s+CO-детектор")
        self.assertRegex(definition, r"(?is)запах\w*\s+продукт\w+\s+выхлоп")
        self.assertRegex(definition, r"(?is)люб\w+\s+одиночн\w+\s+подозрительн\w+\s+признак")
        self.assertRegex(definition, r"(?is)не\s+жд")
        physiology = (ROOT / TASK5_CHAPTERS[0]).read_text(encoding="utf-8")
        self.assertRegex(physiology, r"(?is)пульсоксиметр.{0,180}не\s+является\s+CO-детектор")
        self.assertRegex(physiology, r"(?is)пульсоксиметр.{0,220}не\s+(?:исключает|опровергает).{0,60}CO")
        self.assertIn("SRC-CDC-CO-CLINICAL", physiology)

    def test_imsafe_has_exactly_six_factors_and_never_eating(self):
        combined = "\n".join(
            [
                (ROOT / TASK5_CHAPTERS[2]).read_text(encoding="utf-8"),
                (ROOT / TASK5_CHAPTERS[3]).read_text(encoding="utf-8"),
                GLOSSARY.read_text(encoding="utf-8"),
                TERMS_REGISTRY.read_text(encoding="utf-8"),
                (ROOT / TASK5_SVGS[1]).read_text(encoding="utf-8"),
            ]
        )
        self.assertNotRegex(combined, r"(?i)Emotion\s*/\s*Eating|emotion/eating|E\s*=\s*Eating")
        term = next(
            item for item in json.loads(TERMS_REGISTRY.read_text()) if item["canonical"] == "IMSAFE"
        )
        for factor in ("Illness", "Medication", "Stress", "Alcohol", "Fatigue", "Emotion"):
            self.assertIn(factor, term["english"])

    def test_human_evidence_is_claim_adjacent_and_source_specific(self):
        registered = {source["id"] for source in json.loads(SOURCE_REGISTRY.read_text())}
        violations = []
        for relative_path in TASK5_CHAPTERS:
            violations.extend(
                f"{relative_path}: {error}"
                for error in human_evidence_adjacency_errors(
                    (ROOT / relative_path).read_text(encoding="utf-8"), registered
                )
            )
        self.assertEqual([], violations)
        false_oxygen = (
            "Дополнительный кислород требуется выше 1 000 ft. "
            "Источник: `SRC-EASA-EGAST-GA2`."
        )
        self.assertTrue(human_evidence_adjacency_errors(false_oxygen, registered))
        correct_oxygen = false_oxygen.replace(
            "SRC-EASA-EGAST-GA2", "SRC-BOE-RD-765-2022"
        )
        self.assertEqual([], human_evidence_adjacency_errors(correct_oxygen, registered))
        whitespace_sensitive_claims = (
            "Центральная область сетчатки обеспечивает детальное зрение.",
            "Полукружные каналы участвуют в возникновении вестибулярных иллюзий.",
            "Ситуационная осведомлённость включает восприятие, понимание и прогноз.",
            "Личные минимумы могут быть только строже обязательных ограничений.",
            "Part-FCL: LAPL и PPL имеют одинаковую теоретическую глубину.",
            "Part-FCL: LAPL и PPL используют программу PPL.",
        )
        for claim in whitespace_sensitive_claims:
            with self.subTest(claim=claim):
                self.assertTrue(human_evidence_adjacency_errors(claim, registered))

    def test_human_sources_record_exact_documents_pages_and_limits(self):
        sources = {
            source["id"]: source
            for source in json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
        }
        expected = {
            "SRC-FAA-PHAK-25C-CH17": (
                "FAA-H-8083-25C", "hyperventilation 17-4",
                "spatial disorientation 17-6–17-10", "stress and fatigue 17-12–17-13",
                "alcohol and drugs 17-15–17-16", "vision and scanning 17-19–17-23",
            ),
            "SRC-FAA-RISK-MANAGEMENT-2A": ("FAA-H-8083-2A", "IMSAFE"),
            "SRC-FAA-MEDICATIONS-2017": ("OK-17-2022", "pages 1–2"),
            "SRC-FAA-HEARING-NOISE-98-3": (
                "AM-400-98/3",
                "substantive PDF pages 1–3; colophon page 4",
            ),
            "SRC-FAA-FATIGUE-2020": ("OK-20-0925", "PDF pages 1–2", "circadian"),
            "SRC-CDC-CO-CLINICAL": (
                "Confirmation of Diagnosis", "two-wavelength pulse oximeter", "COHgb",
            ),
        }
        for source_id, needles in expected.items():
            with self.subTest(source=source_id):
                record = sources[source_id]
                joined = f'{record["edition"]} {record["scope"]}'
                for needle in needles:
                    self.assertIn(needle, joined)
                self.assertRegex(record["scope"], r"(?i)не\s+(?:норма|источник).*(?:ЕС|Испани)")

    def test_med_a020_consultation_applies_to_lapl_and_class2_holders(self):
        chapter = (ROOT / TASK5_CHAPTERS[2]).read_text(encoding="utf-8")
        plain = _plain_markdown(chapter)
        self.assertRegex(
            plain,
            r"(?is)MED\.A\.020.{0,500}обладател.{0,120}LAPL.{0,120}Class\s*2",
        )
        self.assertRegex(
            plain,
            r"(?is)без\s+неоправданной\s+задержки.{0,500}"
            r"операц.{0,100}регулярн.{0,80}лекарств.{0,120}"
            r"травм.{0,100}болезн.{0,100}беремен.{0,100}"
            r"стационар.{0,120}корректирующ",
        )
        self.assertRegex(plain, r"(?is)при\s+сомнени.{0,80}консультац")
        self.assertRegex(plain, r"(?is)ULM.{0,100}отдельн\w+\s+национальн\w+\s+режим")

    def test_postflight_guidance_distinguishes_suspected_co(self):
        chapter = (ROOT / TASK5_CHAPTERS[0]).read_text(encoding="utf-8")
        plain = _plain_markdown(chapter)
        self.assertRegex(
            plain,
            r"(?is)подозрен.{0,30}CO.{0,180}медицинск.{0,100}"
            r"техническ.{0,50}проверк.{0,100}SRC-EASA-SIB-2020-01R1",
        )
        self.assertRegex(
            plain,
            r"(?is)друг\w+\s+симптом.{0,180}применим\w+\s+медицинск\w+\s+рекомендац|"
            r"профессиональн\w+\s+оценк",
        )

    def test_question_grounding_rejects_generic_model_language(self):
        self.assertFalse(
            explanation_is_grounded(
                "Этот механизм основан на модели и поэтому подходит.",
                "Как CO влияет на перенос кислорода?",
            )
        )

    def test_task5_files_exist_and_are_in_navigation(self):
        nav_paths = mkdocs_nav_paths((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        for relative_path in TASK5_CHAPTERS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), nav_paths)
        for relative_path in TASK5_SVGS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_task5_chapter_template_applicability_and_stable_headings(self):
        required_anchors = {
            "purpose", "outcomes", "applicability", "theory", "ulm-application",
            "part-fcl-extension", "safety", "common-errors", "summary",
            "review-questions", "sources",
        }
        for relative_path in TASK5_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertEqual([], explicit_atx_heading_errors(text))
                self.assertTrue(required_anchors.issubset(markdown_anchors(text)))
                labels = applicability_table_labels(text)
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, labels)

    def test_task5_required_topics_are_explicitly_anchored(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK5_CHAPTERS
        )
        required = {
            "hypoxia", "hyperventilation", "carbon-monoxide", "spatial-disorientation",
            "fatigue", "medication", "alcohol", "stress", "imsafe",
            "situational-awareness", "tem", "external-pressure",
        }
        self.assertTrue(required.issubset(markdown_anchors(text)), required - markdown_anchors(text))

    def test_task5_has_twenty_four_substantive_unique_questions(self):
        blocks = []
        violations = []
        for relative_path in TASK5_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            chapter = parsed_question_blocks(text)
            self.assertEqual(6, len(chapter), relative_path)
            blocks.extend(chapter)
            violations.extend(f"{relative_path}: {item}" for item in question_block_errors(text))
        self.assertEqual(24, len(blocks))
        self.assertEqual(24, len({block["id"] for block in blocks}))
        prompts = {
            re.sub(r"\W+", " ", _plain_markdown(block["prompt"]).casefold()).strip()
            for block in blocks
        }
        self.assertEqual(24, len(prompts))
        self.assertEqual([], violations)

    def test_task5_has_at_least_eight_labelled_decision_scenarios(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK5_CHAPTERS
        )
        scenarios = re.findall(
            r"(?m)^###\s+Сценарий\s+HP-\d{2}\s+—\s+.+?\{#scenario-hp-\d{2}\}\s*$",
            text,
        )
        self.assertGreaterEqual(len(scenarios), 8)
        self.assertRegex(text, r"(?i)go/no-go")
        self.assertRegex(text, r"(?i)continue/divert")

    def test_task5_normative_and_medical_safety_claims_are_cited(self):
        registered = {
            source["id"] for source in json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
        }
        violations = []
        for relative_path in TASK5_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            violations.extend(
                f"{relative_path}: {error}" for error in normative_claim_errors(text, registered)
            )
            citations = set(re.findall(r"SRC-[A-Z0-9-]+", text))
            self.assertTrue(citations.issubset(registered), citations - registered)
            self.assertGreaterEqual(len(citations), 2, relative_path)
        self.assertEqual([], violations)

    def test_task5_refutes_myths_without_unsafe_medical_advice(self):
        violations = []
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK5_CHAPTERS
        )
        for relative_path in TASK5_CHAPTERS:
            chapter = (ROOT / relative_path).read_text(encoding="utf-8")
            violations.extend(
                f"{relative_path}: {error}" for error in human_performance_safety_errors(chapter)
            )
        self.assertEqual([], violations)
        for phrase in (
            "ULM летает низко", "ниже 10 000 ft", "легко отличить от гипервентиляции",
            "предупреждающего запаха", "не гарантирует безопасность", "кофеин не лечит",
            "medical не означает", "OTC не означает", "IMSAFE не является нормой EASA",
            "личные минимумы не заменяют", "законные VMC не означают",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), _plain_markdown(text).casefold())

    def test_human_performance_guard_rejects_unsafe_synthetic_probes(self):
        probes = (
            "ULM всегда летает низко, поэтому гипоксия не важна.",
            "Ниже 10 000 ft гипоксия невозможна.",
            "Гипоксию легко отличить от гипервентиляции.",
            "Угарный газ имеет полезный предупреждающий запах.",
            "Пульсоксиметр гарантирует безопасность.",
            "Каждый пилот должен всегда спать 8 часов.",
            "После алкоголя достаточно ждать 8 часов.",
            "Диагностируйте гипоксию и назначьте лечение.",
            "Гипоксия невозможна ниже 9 000 ft.",
            "Действующий medical гарантирует годность сегодня.",
            "OTC-препарат безопасен.",
            "Личные минимумы заменяют AFM.",
            "Законные VMC всегда пригодны для этого пилота.",
            "Гипоксия невозможна ниже 9 000 ft, а её признаки неспецифичны.",
            "Действующий medical гарантирует годность сегодня, но симптомы стоит отслеживать.",
            "OTC-препарат безопасен, если он продаётся без рецепта.",
            "Личные минимумы заменяют AFM, а законные VMC пригодны этому пилоту.",
            "OTC-препарат не обязательно безопасен для пассажира, а для пилота безопасен.",
            "Личные минимумы не заменяют пожелания пассажира, зато заменяют AFM.",
            "Законные VMC не всегда пригодны пассажиру, но пригодны этому пилоту.",
            "Гипоксия не невозможна ниже 9 000 ft, но невозможна ниже 8 000 ft.",
        )
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertTrue(human_performance_safety_errors(probe))
        self.assertEqual(
            [],
            human_performance_safety_errors(
                "Миф: ниже 10 000 ft гипоксия невозможна; индивидуальная восприимчивость различается."
            ),
        )
        for safe in (
            "Детектор не всегда гарантирует безопасность.",
            "OTC-препарат не обязательно безопасен.",
            "Личные минимумы никогда не заменяют ограничения AFM.",
            "Законные VMC не всегда пригодны для этого пилота.",
            "Законные VMC не означают, что условия пригодны этому пилоту.",
        ):
            with self.subTest(safe=safe):
                self.assertEqual([], human_performance_safety_errors(safe))

    def test_task5_sources_and_terms_are_registered(self):
        sources = {source["id"] for source in json.loads(SOURCE_REGISTRY.read_text())}
        self.assertTrue(
            {
                "SRC-EASA-HYPOXIA-2016", "SRC-EASA-SIB-2020-01R1",
                "SRC-EASA-EGAST-GA2",
                "SRC-FAA-PHAK-25C-CH17", "SRC-FAA-RISK-MANAGEMENT-2A",
                "SRC-FAA-MEDICATIONS-2017", "SRC-FAA-HEARING-NOISE-98-3",
                "SRC-FAA-FATIGUE-2020", "SRC-CDC-CO-CLINICAL",
            }.issubset(sources)
        )
        canonical = {term["canonical"] for term in json.loads(TERMS_REGISTRY.read_text())}
        for term in (
            "hypoxia", "hyperventilation", "carbon monoxide (CO)",
            "spatial disorientation", "situational awareness",
            "threat and error management (TEM)", "aeronautical decision-making (ADM)",
            "IMSAFE", "PAVE", "personal minima", "external pressure",
            "Part-MED", "aeromedical examiner (AME)",
            "over-the-counter medication (OTC)", "crew resource management (CRM)",
            "non-technical skills (NTS)",
            "Human performance", "go/no-go", "continue/divert",
            "AVIATE–NAVIGATE–COMMUNICATE",
        ):
            self.assertIn(term, canonical)

    def test_task5_svgs_are_accessible_and_use_real_geometry(self):
        namespace = "{http://www.w3.org/2000/svg}"
        for relative_path in TASK5_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            with self.subTest(path=relative_path):
                self.assertEqual(f"{namespace}svg", root.tag)
                self.assertEqual("img", root.attrib.get("role"))
                self.assertTrue(root.attrib.get("aria-labelledby"))
                self.assertIsNotNone(root.find(f"{namespace}title"))
                self.assertIsNotNone(root.find(f"{namespace}desc"))
                self.assertFalse(list(root.iter(f"{namespace}image")))
                viewbox = tuple(float(value) for value in root.attrib["viewBox"].split())
                self.assertEqual(4, len(viewbox))
                vx, vy, vw, vh = viewbox
                self.assertLessEqual(vw, 700, "mobile-readable SVG width")
                text_sizes = [
                    float(element.attrib["font-size"].removesuffix("px"))
                    for element in root.iter(f"{namespace}text")
                    if "font-size" in element.attrib
                ]
                self.assertTrue(text_sizes)
                self.assertGreaterEqual(min(text_sizes) * 340 / vw, 14.0)
                for element in root.iter():
                    bbox = element_bbox(element)
                    if bbox is None:
                        continue
                    x, y, width, height = bbox
                    self.assertGreaterEqual(x, vx)
                    self.assertGreaterEqual(y, vy)
                    self.assertLessEqual(x + width, vx + vw)
                    self.assertLessEqual(y + height, vy + vh)
                for group in root.iter(f"{namespace}g"):
                    panel = next(
                        (child for child in group if child.tag == f"{namespace}rect"),
                        None,
                    )
                    if panel is None:
                        continue
                    panel_box = element_bbox(panel)
                    px, py, pw, ph = panel_box
                    for label in (
                        child for child in group if child.tag == f"{namespace}text"
                    ):
                        label_box = element_bbox(label)
                        if label_box is None:
                            continue
                        tx, ty, tw, th = label_box
                        self.assertGreaterEqual(tx, px, group.attrib.get("id"))
                        self.assertGreaterEqual(ty, py, group.attrib.get("id"))
                        self.assertLessEqual(tx + tw, px + pw, group.attrib.get("id"))
                        self.assertLessEqual(ty + th, py + ph, group.attrib.get("id"))

    def test_hypoxia_diagram_separates_hypoxia_and_co_and_disclaims_treatment(self):
        root = ET.parse(ROOT / TASK5_SVGS[0]).getroot()
        by_id = {element.attrib["id"]: element for element in root.iter() if "id" in element.attrib}
        for identifier in (
            "hypoxia-path", "co-path", "branch-or", "aviate-control", "oxygen-checklist",
            "descend-land", "postflight-co", "postflight-other", "safety-disclaimer",
        ):
            self.assertIn(identifier, by_id)
        words = " ".join(root.itertext()).casefold()
        self.assertIn("не медицинское лечение", words)
        self.assertIn("не чек-лист воздушного судна", words)
        self.assertIn("или", words)
        self.assertIn("при co", words)
        self.assertIn("при других симптомах", words)
        self.assertFalse(bboxes_overlap(element_bbox(by_id["hypoxia-path"]), element_bbox(by_id["co-path"])))

        hypoxia_panel = element_bbox(by_id["hypoxia-panel"])
        co_panel = element_bbox(by_id["co-panel"])
        branch_a = by_id["hypoxia-to-merge"]
        branch_b = by_id["co-to-merge"]
        merge_to_aviate = by_id["merge-to-aviate"]
        endpoint_a = (float(branch_a.attrib["x2"]), float(branch_a.attrib["y2"]))
        endpoint_b = (float(branch_b.attrib["x2"]), float(branch_b.attrib["y2"]))
        self.assertEqual(endpoint_a, endpoint_b, "A and B must converge at one merge")
        self.assertEqual(
            endpoint_a,
            (float(merge_to_aviate.attrib["x1"]), float(merge_to_aviate.attrib["y1"])),
        )

        def inside(point, box):
            x, y = point
            bx, by, bw, bh = box
            return bx <= x <= bx + bw and by <= y <= by + bh

        self.assertFalse(inside(endpoint_a, hypoxia_panel))
        self.assertFalse(inside(endpoint_a, co_panel))
        self.assertNotEqual(
            (float(branch_a.attrib["x1"]), float(branch_a.attrib["y1"])),
            (float(branch_b.attrib["x1"]), float(branch_b.attrib["y1"])),
        )
        co_follow = by_id["landing-to-co"]
        other_follow = by_id["landing-to-other"]
        self.assertEqual(
            (float(co_follow.attrib["x1"]), float(co_follow.attrib["y1"])),
            (float(other_follow.attrib["x1"]), float(other_follow.attrib["y1"])),
        )
        self.assertNotEqual(
            (float(co_follow.attrib["x2"]), float(co_follow.attrib["y2"])),
            (float(other_follow.attrib["x2"]), float(other_follow.attrib["y2"])),
        )

    def test_decision_loop_has_complete_loop_and_preflight_inputs(self):
        root = ET.parse(ROOT / TASK5_SVGS[1]).getroot()
        ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
        self.assertTrue(
            {
                "facts-threats", "understand-risk", "options-escape", "decision",
                "action", "monitor-repeat", "preflight-inputs", "tem-boundary",
            }.issubset(ids)
        )
        words = " ".join(root.itertext())
        self.assertIn("IMSAFE", words)
        self.assertIn("личные минимумы", words.casefold())
        self.assertIn("TEM", words)
        markers = list(root.iter("{http://www.w3.org/2000/svg}marker"))
        self.assertTrue(markers, "decision flow requires arrow markers")
        self.assertGreaterEqual(
            len([
                element for element in root.iter()
                if element.attrib.get("marker-end", "").startswith("url(#")
            ]),
            6,
        )
        return_path = next(
            element for element in root.iter()
            if element.attrib.get("id") == "return-path"
        )
        self.assertTrue(return_path.attrib.get("marker-end", "").startswith("url(#"))

    def test_task5_diagram_panels_do_not_overlap_and_colours_have_contrast(self):
        def luminance(hex_colour):
            channels = [int(hex_colour[index:index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        def contrast(first, second):
            bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
            return (bright + 0.05) / (dark + 0.05)

        for relative_path in TASK5_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            by_id = {element.attrib.get("id"): element for element in root.iter()}
            panels = [
                element_bbox(element)
                for identifier, element in by_id.items()
                if identifier and identifier.endswith("-panel")
            ]
            for index, first in enumerate(panels):
                for second in panels[index + 1:]:
                    self.assertFalse(bboxes_overlap(first, second), relative_path)
            self.assertGreaterEqual(contrast("#F8FAFC", "#0F172A"), 7.0)
            self.assertGreaterEqual(contrast("#FFFFFF", "#1E3A5F"), 7.0)

    def test_task5_distractors_avoid_reviewed_strawmen(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK5_CHAPTERS
        )
        for strawman in (
            r"кислород\s+полностью\s+исчезает",
            r"сердце\s+переста[её]т\s+перекачивать",
            r"уменьшение\s+контраста.{0,30}блик",
            r"PAVE.{0,80}квалификационн\w+\s+отметк",
            r"одн\w+\s+приемлем\w+\s+сектор.{0,50}четыр",
            r"зрени\w+\s+автоматическ\w+\s+восстанавлива\w+\s+горизонт",
            r"дела\w+\s+стандартн\w+\s+структур\w+\s+сообщен\w+\s+ненужн",
            r"испанск\w+\s+лицензи\w+.{0,40}медицинск\w+\s+осмотр",
        ):
            self.assertNotRegex(_plain_markdown(text), re.compile(strawman, re.IGNORECASE))


def weather_safety_errors(text):
    """Return unsafe meteorology shortcuts from learner prose, sentence by sentence."""
    learner_text = re.split(
        r"(?m)^##\s+(?:Контрольные вопросы|Источники)\b", text, maxsplit=1
    )[0]
    learner_text = re.sub(
        r"(?ms)^##\s+Типичные ошибки\b.*?(?=^##\s+|\Z)", "", learner_text
    )
    dangerous = (
        r"\bCAVOK\b.{0,55}\b(?:всегда\s+)?(?:безопасн|ясн\w+\s+неб)",
        r"\bMETAR\b.{0,45}(?:описыва\w+|явля\w+)\s+(?:весь\s+)?маршрут",
        r"\bTAF\b.{0,55}(?:гарантир\w+|обеща\w+)",
        r"\bTEMPO\b.{0,45}(?:можно\s+)?игнорир\w+",
        r"\bPROB30\b.{0,45}(?:ничтожн|незнач|можно\s+игнорир)",
        r"без\s+группы\s+G.{0,55}(?:порыв|турбулент).{0,35}(?:нет|не\s+будет)",
        r"\bSPECI\b.{0,55}(?:исправлен\w+|коррекц\w+).{0,30}\bTAF\b",
        r"без\s+SIGMET.{0,55}(?:опасност|угроз).{0,35}(?:нет|отсутств\w+)",
        r"стандартн\w+\s+градиент.{0,60}(?:точно|фактическ).{0,35}(?:облач|замерзан|нулев)",
        r"\bQNH\b.{0,55}(?:показыва\w+|равн\w+).{0,25}высот\w+\s+над\s+(?:ВПП|порог)",
        r"\bQFE\b.{0,45}(?:всегда|универсальн).{0,25}(?:обязател|требу)",
        r"(?:волн\w*|ротор).{0,55}(?:обязательн|всегда).{0,25}линзовидн",
        r"морск\w+\s+бриз.{0,45}(?:всегда|обязательно).{0,20}слаб",
        r"архивн\w+\s+(?:скриншот|снимок).{0,45}(?:явля\w+|это).{0,20}текущ\w+\s+погод",
        r"климатолог\w+.{0,45}(?:явля\w+|это).{0,20}прогноз",
    )
    errors = []
    for sentence in _sentences(learner_text):
        for pattern in dangerous:
            match = re.search(pattern, sentence, re.IGNORECASE)
            safe_subject_negation = re.search(
                r"(?i)(?:\bCAVOK\b|\bMETAR\b|\bTAF\b|\bTEMPO\b|\bPROB30\b|"
                r"\bSPECI\b|\bQNH\b|\bQFE\b|климатолог\w+|морск\w+\s+бриз|"
                r"линзовидн\w+\s+облак\w+|стандартн\w+\s+градиент|"
                r"архивн\w+\s+(?:скриншот|снимок))"
                r".{0,28}\b(?:не|нельзя)\b",
                sentence,
            ) or re.search(
                r"(?i)(?:отсутствие|без)\s+(?:группы\s+G|SIGMET).{0,25}\bне\s+означает\b",
                sentence,
            )
            if match and not safe_subject_negation:
                errors.append(sentence)
                break

        universal_limit = re.search(
            r"(?i)\bULM\b.{0,90}(?:универсальн\w+|всегда|обязан\w*|нельзя\s+ближе).{0,90}"
            r"(?:ветр\w*|порыв\w*|боков\w+\s+ветр\w*|видимост\w*|облачност\w*|турбулент\w*|обледен\w*|гроз\w*).{0,40}"
            r"\b\d+(?:[.,]\d+)?\s*(?:kt|km/h|км/ч|m|м|km|км|ft|фут)",
            sentence,
        )
        universal_distance = re.search(
            r"(?i)\bULM\b.{0,50}нельзя\s+ближе.{0,30}\b\d+(?:[.,]\d+)?\s*"
            r"(?:km|км|m|м).{0,25}гроз\w*",
            sentence,
        )
        denies_universal_limit = re.search(
            r"(?i)\b(?:нет|не\s+существует)\s+универсальн\w+.{0,80}(?:лимит|предел|дистанц)",
            sentence,
        )
        if (universal_limit or universal_distance) and not denies_universal_limit:
            errors.append(sentence)
    return errors


class Task6MeteorologyTests(unittest.TestCase):
    def test_language_guard_rejects_unlabelled_english_prose(self):
        probe = "Пилот проверяет данные. This entire operational sentence is English."
        self.assertEqual(
            [(1, "This entire operational sentence is English")],
            unexplained_english_phrase_occurrences(probe),
        )
        self.assertEqual(
            [],
            unexplained_english_phrase_occurrences(
                "Пилот проверяет [высоту по плотности][density-altitude] и QNH."
            ),
        )
        self.assertEqual(
            [(1, "dew point"), (1, "approximate cloud base")],
            unexplained_english_phrase_occurrences(
                "Проверьте dew point и `approximate cloud base`."
            ),
        )
        self.assertEqual(
            [(1, "wind shear")],
            unexplained_english_phrase_occurrences(
                "Риск [wind shear][wind-shear] вырос."
            ),
        )
        self.assertEqual(
            [],
            unexplained_english_phrase_occurrences(
                "METAR: `T = Td + 2`; источник `SRC-AEMET-GUIA-MET-2025`."
            ),
        )

    def test_task6_ru_first_language_contract_and_first_use_terms(self):
        violations = []
        for relative_path in TASK6_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            violations.extend(
                f"{relative_path}:{line}: {phrase}"
                for line, phrase in unexplained_english_phrase_occurrences(text)
            )
        glossary = GLOSSARY.read_text(encoding="utf-8")
        sections = glossary_sections(glossary)
        for anchor in (
            "term-international-standard-atmosphere-isa", "term-flight-level-fl",
            "term-qfe", "term-cavok", "term-speci", "term-trend", "term-sigmet",
            "term-airmet", "term-gamet", "term-aeronautical-meteorological-self-service-ama",
            "term-density-altitude", "term-wind-shear", "term-vfr-into-imc-vfr2imc",
            "term-pressure-altitude",
            "term-transition-altitude", "term-transition-level", "term-anabatic-flow",
            "term-katabatic-flow", "term-mountain-wave", "term-rotor",
            "term-lee-downdraft", "term-headwind-component",
            "term-crosswind-component", "term-surface-wind",
            "term-significant-weather-chart-low-level-swl",
        ):
            violations.extend(
                f"glossary:{anchor}:{line}: {phrase}"
                for line, phrase in unexplained_english_phrase_occurrences(sections[anchor])
            )
        self.assertEqual([], violations)

        products = (ROOT / TASK6_CHAPTERS[5]).read_text(encoding="utf-8")
        for abbreviation in ("METAR", "TAF", "SPECI", "AIRMET", "GAMET"):
            with self.subTest(abbreviation=abbreviation):
                self.assertRegex(
                    products,
                    re.compile(
                        rf"(?m)^\|\s*(?:\[{abbreviation}\]\[[^\]]+\]|{abbreviation})\s*\|"
                        r"[^|]*[А-Яа-яЁё][^|]*\|"
                        r"[^|]*[A-Za-z][^|]*\|[^|]*[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][^|]*\|\s*$"
                    ),
                )

        atmosphere = (ROOT / TASK6_CHAPTERS[0]).read_text(encoding="utf-8")
        wind = (ROOT / TASK6_CHAPTERS[1]).read_text(encoding="utf-8")
        products_intro = (ROOT / TASK6_CHAPTERS[5]).read_text(
            encoding="utf-8"
        ).split("## Результаты обучения", 1)[0]
        for text, russian, english, spanish, link in (
            (atmosphere, "барометрическая высота", "pressure altitude", "altitud de presión", "pressure-altitude"),
            (atmosphere, "абсолютная высота перехода", "transition altitude", "altitud de transición", "transition-altitude"),
            (atmosphere, "эшелон перехода", "transition level", "nivel de transición", "transition-level"),
            (wind, "анабатический склоновый поток", "anabatic flow", "flujo anabático", "anabatic-flow"),
            (wind, "катабатический склоновый поток", "katabatic flow", "flujo catabático", "katabatic-flow"),
            (wind, "горная волна", "mountain wave", "onda de montaña", "mountain-wave"),
            (wind, "подветренный нисходящий поток", "lee downdraft", "corriente descendente a sotavento", "lee-downdraft"),
            (wind, "боковая составляющая ветра", "crosswind component", "componente de viento cruzado", "crosswind-component"),
            (wind, "приземный ветер", "surface wind", "viento en superficie", "surface-wind"),
        ):
            with self.subTest(english=english):
                self.assertRegex(
                    text,
                    re.compile(
                        rf"\[{re.escape(russian)}[^\]]*English:\s*{re.escape(english)};\s*"
                        rf"español:\s*{re.escape(spanish)}[^\]]*\]\[{re.escape(link)}\]",
                        re.IGNORECASE,
                    ),
                )
        for link in ("trend", "sigmet", "swl", "ama"):
            self.assertRegex(products_intro, rf"\[[^\]]+\]\[{link}\]")

    def test_weather_guard_rejects_unsafe_synthetic_probes(self):
        probes = (
            "CAVOK всегда означает безопасное ясное небо.",
            "METAR описывает весь маршрут.",
            "TAF гарантирует указанную погоду.",
            "TEMPO можно игнорировать при коротком полёте.",
            "PROB30 — незначительная вероятность, её можно игнорировать.",
            "Без группы G порывов и турбулентности не будет.",
            "SPECI является исправленной версией TAF.",
            "Без SIGMET опасности на маршруте отсутствуют.",
            "Стандартный градиент точно показывает фактический уровень замерзания.",
            "QNH показывает высоту над ВПП.",
            "QFE всегда обязательно для ULM.",
            "Для горной волны обязательно видна линзовидная облачность.",
            "Морской бриз всегда слабый.",
            "Архивный скриншот является текущей погодой.",
            "Климатология является прогнозом на сегодня.",
            "ULM всегда обязан отменить вылет при ветре 15 kt.",
            "ULM нельзя ближе 20 km к грозе.",
        )
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertTrue(weather_safety_errors(probe))
        safe = (
            "CAVOK не означает ясное небо или автоматическую безопасность.",
            "METAR не описывает весь маршрут.",
            "Для ULM нет универсального учебного лимита ветра 15 kt.",
            "Климатология не является прогнозом на сегодня.",
        )
        for value in safe:
            with self.subTest(value=value):
                self.assertEqual([], weather_safety_errors(value))

    def test_task6_files_exist_and_are_in_navigation(self):
        nav_paths = mkdocs_nav_paths((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        for relative_path in TASK6_CHAPTERS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), nav_paths)
        for relative_path in TASK6_SVGS:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_task6_template_scope_and_stable_anchors(self):
        required_anchors = {
            "purpose", "outcomes", "applicability", "theory", "ulm-application",
            "part-fcl-extension", "safety", "common-errors", "summary",
            "review-questions", "sources",
        }
        for relative_path in TASK6_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            plain = _plain_markdown(text)
            with self.subTest(path=relative_path):
                self.assertEqual([], explicit_atx_heading_errors(text))
                self.assertTrue(required_anchors.issubset(markdown_anchors(text)))
                labels = applicability_table_labels(text)
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, labels)
                self.assertRegex(plain, r"(?is)ULM.{0,160}Испани")
                self.assertRegex(plain, r"(?is)(?:LAPL|PPL).{0,180}(?:будущ|переход|расширен)")

    def test_task6_required_topics_are_explicitly_anchored(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        required = {
            "isa-reference", "lapse-rate-inversion", "qnh-qfe-standard",
            "transition-altitude", "gusts", "sea-land-breeze", "mountain-wave-rotor",
            "humidity-dew-point", "cloud-genera", "fog", "cavok",
            "air-masses", "fronts", "pressure-systems", "thunderstorm",
            "icing", "vfr2imc", "density-altitude", "metar-speci-trend",
            "taf-change-groups", "sigmet-airmet-gamet", "ama", "weather-worksheet",
        }
        self.assertTrue(required.issubset(markdown_anchors(text)), required - markdown_anchors(text))

    def test_task6_worked_calculations_have_required_structure_and_limits(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        headings = list(re.finditer(
            r"(?m)^###\s+Учебный расчёт MET-CALC-\d{2}.+\{#met-calc-\d{2}\}\s*$", text
        ))
        self.assertGreaterEqual(len(headings), 4)
        for index, match in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            block = text[match.end():end]
            with self.subTest(calculation=match.group(0)):
                for label in ("Дано", "Формула", "Расчёт", "Результат", "Решение пилота"):
                    self.assertRegex(block, rf"(?m)^\*\*{re.escape(label)}:\*\*")
                self.assertRegex(block, r"(?i)(?:допущен|приближен)")
                self.assertRegex(
                    block,
                    r"(?i)не\s+(?:(?:является\s+)?прогноз|значение\s+AFM|заменяет\s+AFM)",
                )
        plain = _plain_markdown(text)
        self.assertRegex(plain, r"(?is)стандартн\w+\s+градиент.{0,180}не.{0,60}(?:фактическ|уровн\w+\s+замерзан)")

    def test_wind_calculation_uses_one_reference_and_mean_and_gust_cases(self):
        text = (ROOT / TASK6_CHAPTERS[1]).read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^###\s+Учебный расчёт MET-CALC-04.+?(?=^###\s+|^##\s+)", text
        )
        self.assertIsNotNone(match)
        block = _plain_markdown(match.group(0))
        self.assertRegex(block, r"(?is)(?:истинн|магнитн).{0,160}(?:един|одн\w+\s+систем)")
        self.assertRegex(block, r"(?is)(?:слева|справа).{0,100}(?:знак|положительн|отрицательн)")
        self.assertRegex(block, r"(?is)средн\w+.{0,180}порыв")
        self.assertRegex(block, r"SRC-[A-Z0-9-]+")
        self.assertRegex(block, r"проверено\s+2026-07-13")

    def test_task6_has_ten_fully_decoded_synthetic_examples(self):
        text = (ROOT / TASK6_CHAPTERS[5]).read_text(encoding="utf-8")
        examples = list(re.finditer(
            r"(?m)^###\s+Синтетический пример MET-DEC-(\d{2}).+\{#met-dec-\1\}\s*$", text
        ))
        self.assertGreaterEqual(len(examples), 10)
        self.assertGreaterEqual(
            text.count("СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА"), 10
        )
        for index, match in enumerate(examples):
            end = examples[index + 1].start() if index + 1 < len(examples) else len(text)
            block = text[match.end():end]
            with self.subTest(example=match.group(1)):
                self.assertRegex(block, r"(?m)^\*\*Код:\*\*")
                self.assertRegex(block, r"(?m)^\*\*Разбор:\*\*")
                self.assertRegex(block, r"(?m)^\*\*Решение пилота:\*\*")
                self.assertRegex(block, r"SRC-[A-Z0-9-]+")
                self.assertRegex(block, r"проверено\s+2026-07-13")
        plain = _plain_markdown(text)
        for token in (
            "METAR", "G", "VRB", "CAVOK", "AUTO", "SPECI", "TREND",
            "BECMG", "FM", "TEMPO", "PROB30", "PROB40", "AMD", "COR",
        ):
            self.assertIn(token.casefold(), plain.casefold())

        dec03 = re.search(
            r"(?ms)^###\s+Синтетический пример MET-DEC-03.+?(?=^###\s+)", text
        ).group(0)
        self.assertRegex(dec03, r"(?is)не\s+менее\s+3\s*kt")
        self.assertRegex(dec03, r"(?is)(?:измен|разброс).{0,80}180°")
        self.assertRegex(dec03, r"(?is)(?:невозмож|нельзя).{0,80}(?:един|одно).{0,40}направлен")
        self.assertRegex(dec03, r"SRC-AEMET-GUIA-MET-2025.{0,80}(?:p\.?|стр(?:аница)?\.?)[ ]*18")

    def test_task6_has_six_labelled_spanish_scenarios(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        scenarios = re.findall(
            r"(?m)^###\s+Сценарий ESP-MET-\d{2}\s+—\s+.+\{#scenario-esp-met-\d{2}\}\s*$",
            text,
        )
        self.assertGreaterEqual(len(scenarios), 6)
        plain = _plain_markdown(text)
        for pattern in (
            r"Средиземномор.{0,120}(?:бриз|конверген)",
            r"Кантабр.{0,120}(?:адвектив|стратус)",
            r"Месет.{0,120}(?:инверси|радиационн)",
            r"горн.{0,100}(?:волна|ротор)",
            r"Эстречо-де-Гибралтар.{0,120}(?:канализ|струйн)",
            r"Канар.{0,120}(?:пассат|орограф|подветрен)",
        ):
            self.assertRegex(plain, re.compile(pattern, re.IGNORECASE | re.DOTALL))
        self.assertRegex(plain, r"(?is)климатолог\w+.{0,80}не.{0,40}прогноз")

    def test_spain_scenarios_are_ordered_conditional_and_use_one_template(self):
        ordered = []
        for relative_path in TASK6_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            matches = list(re.finditer(
                r"(?m)^###\s+Сценарий ESP-MET-(\d{2})\s+—.+\{#scenario-esp-met-\1\}\s*$",
                text,
            ))
            for index, match in enumerate(matches):
                end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
                next_heading = re.search(r"(?m)^##?\s+", text[match.end():end])
                if next_heading:
                    end = match.end() + next_heading.start()
                block = text[match.end():end]
                ordered.append(match.group(1))
                for label in (
                    "Условные учебные данные", "Риск", "Не хватает данных",
                    "Решение", "Наблюдаемый триггер",
                ):
                    self.assertRegex(block, rf"(?m)^\*\*{re.escape(label)}:\*\*")
                self.assertRegex(block, r"SRC-[A-Z0-9-]+")
                self.assertRegex(block, r"проверено\s+2026-07-13")
        self.assertEqual(["01", "02", "03", "04", "05", "06"], ordered)

    def test_task6_nine_step_weather_decision_worksheet(self):
        text = (ROOT / TASK6_CHAPTERS[6]).read_text(encoding="utf-8")
        worksheet = re.search(
            r"(?ms)^###\s+Девятишаговый.+?\{#weather-worksheet\}\s*\n"
            r"(.+?)(?=^###\s+Матрица)",
            text,
        )
        self.assertIsNotNone(worksheet)
        self.assertTrue(worksheet.group(1).strip())
        steps = re.findall(r"(?m)^####\s+Шаг\s+([1-9])\s+—\s+.+\{#weather-step-\1\}\s*$", text)
        self.assertEqual(list("123456789"), steps)
        step_matches = list(re.finditer(
            r"(?m)^####\s+Шаг\s+([1-9])\s+—\s+.+\{#weather-step-\1\}\s*$", text
        ))
        for index, match in enumerate(step_matches):
            end = step_matches[index + 1].start() if index + 1 < len(step_matches) else text.index("### Матрица")
            block = text[match.end():end]
            self.assertRegex(block, r"SRC-[A-Z0-9-]+")
            self.assertRegex(block, r"проверено\s+2026-07-13")
        plain = _plain_markdown(text)
        for decision in ("GO", "DELAY", "REROUTE", "CANCEL"):
            self.assertIn(decision, plain)
        for trigger in ("задержк", "уход", "разворот", "посадк"):
            self.assertRegex(plain, re.compile(trigger, re.IGNORECASE))
        self.assertRegex(plain, r"(?is)неблагоприятн\w+\s+тенденц\w+.{0,100}не.{0,30}автоматическ\w+\s+отмен")
        self.assertRegex(plain, r"(?is)заранее\s+согласован\w+.{0,120}до\s+потер\w+\s+безопасн\w+\s+геометр")
        self.assertRegex(plain, r"(?is)триггер.{0,80}достигнут.{0,80}разворот")
        self.assertRegex(plain, r"(?is)разреш[её]нн\w+\s+аэродром.{0,180}вынужденн\w+\s+посадк")

        matrix_and_checkpoint = re.search(
            r"(?ms)^###\s+Матрица.+?(?=^###\s+Coast|^###\s+Побереж|^###\s+Рельеф)", text
        ).group(0)
        self.assertRegex(matrix_and_checkpoint, r"SRC-[A-Z0-9-]+")
        self.assertRegex(matrix_and_checkpoint, r"проверено\s+2026-07-13")

    def test_task6_has_thirty_five_substantive_unique_questions(self):
        blocks = []
        violations = []
        for relative_path in TASK6_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            chapter = parsed_question_blocks(text)
            self.assertEqual(5, len(chapter), relative_path)
            blocks.extend(chapter)
            violations.extend(f"{relative_path}: {item}" for item in question_block_errors(text))
        self.assertEqual(35, len(blocks))
        self.assertEqual(35, len({block["id"] for block in blocks}))
        prompts = {
            re.sub(r"\W+", " ", _plain_markdown(block["prompt"]).casefold()).strip()
            for block in blocks
        }
        self.assertEqual(35, len(prompts))
        self.assertEqual([], violations)
        for block in blocks:
            with self.subTest(question=block["id"]):
                self.assertRegex(block["body"], r"(?m)^\*\*Источник объяснения:\*\*")
                self.assertRegex(block["body"], r"SRC-[A-Z0-9-]+")
                self.assertRegex(block["body"], r"проверено\s+2026-07-13")

    def test_task6_distractors_avoid_reviewed_strawmen(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        for pattern in (
            r"групп\w*\s+G.{0,30}только\s+(?:к\s+)?температур",
            r"G\s+публику\w*.{0,30}после\s+(?:завершения\s+)?пол[её]т",
            r"морск\w+\s+бриз.{0,30}только\s+на\s+морск\w+\s+суд",
            r"длин\w+\s+строк\w*.{0,20}(?:без\s+пробел|сообщен)",
            r"SPECI.{0,35}(?:семь|7)\s+дн",
            r"средн\w+\s+арифметическ\w*.{0,35}(?:предел|значен)",
            r"предел.{0,35}выбира\w+\s+пассажир",
        ):
            self.assertNotRegex(_plain_markdown(text), re.compile(pattern, re.IGNORECASE))

        question_specific = {
            "Q-MET-001": r"(?i)ISA|стандартн|модел|профил|температур|давлен",
            "Q-MET-002": r"(?i)QNH|QFE|высотомер|уровн\w+\s+мор|аэродром|1013",
            "Q-MET-003": r"(?i)переход|AIP|аэродром|давлен|ATIS|ATS|FL",
            "Q-MET-007": r"(?i)горн|волн|ротор|ветр|устойчив|нисход|облак",
            "Q-MET-008": r"(?i)боков|составляющ|ветр|порыв|ВПП|AFM|POH|предел",
            "Q-MET-010": r"(?i)приземн|ветр|профил|сдвиг|сло|высот",
        }
        blocks = {
            block["id"]: block
            for path in TASK6_CHAPTERS[:2]
            for block in parsed_question_blocks((ROOT / path).read_text(encoding="utf-8"))
        }
        for identifier, required in question_specific.items():
            block = blocks[identifier]
            answer = re.search(r"\*\*Правильный ответ:\*\*\s*([A-D])\.", block["body"]).group(1)
            options = re.findall(r"(?m)^([A-D])\.\s+(.+?)(?:<br>)?\s*$", block["body"])
            for letter, value in options:
                if letter == answer:
                    continue
                with self.subTest(question=identifier, option=letter):
                    self.assertRegex(_plain_markdown(value), required)

    def test_task6_safety_blocks_have_adjacent_sources(self):
        for relative_path in TASK6_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            block = re.search(
                r"(?ms)^##\s+Безопасность\b.+?(?=^##\s+)", text
            ).group(0)
            with self.subTest(path=relative_path):
                self.assertRegex(block, r"SRC-[A-Z0-9-]+")
                self.assertRegex(block, r"проверено\s+2026-07-13")

    def test_task6_dynamic_sources_and_code_discrepancy_are_explicit(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        plain = _plain_markdown(text)
        self.assertRegex(plain, r"(?is)(?:AIP|AEMET|AMA).{0,120}динамическ")
        self.assertRegex(plain, r"(?is)архивн\w+.{0,80}не.{0,60}(?:текущ|пол[её]т)")
        self.assertRegex(plain, r"(?is)\bV1\b.{0,60}(?:ниже|<)\s*1000\s*м")
        self.assertRegex(plain, r"(?is)\bV5\b.{0,60}1000.{0,30}5000\s*м")
        self.assertRegex(plain, r"SRC-ENAIRE-AIP-GEN-3-5-2026")
        self.assertRegex(plain, r"проверено\s+2026-07-13")

    def test_part_nco_scope_is_operation_based_not_licence_triggered(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        plain = _plain_markdown(text)
        self.assertRegex(
            plain,
            r"(?is)некоммерческ\w+\s+эксплуатац\w+\s+самол[её]т\w+.{0,120}"
            r"Регламент\w*\s*\(ЕС\)\s*965/2012.{0,100}Annex VII.{0,80}Part-NCO",
        )
        self.assertRegex(
            plain,
            r"(?is)наличи\w+\s+(?:лицензи\w+\s+)?(?:LAPL|PPL).{0,100}"
            r"не.{0,30}определя\w+.{0,80}применимост",
        )
        self.assertNotRegex(plain, r"(?is)(?:future|будущ\w+)\s+(?:LAPL|PPL).{0,80}Part-NCO")
        self.assertNotRegex(plain, r"(?is)Part-NCO.{0,100}continual reassessment")

        sources = {
            source["id"]: source for source in json.loads(SOURCE_REGISTRY.read_text())
        }
        scope = sources["SRC-EASA-AIR-OPS-2026"]["scope"]
        for required in ("Article 5(4)", "Annex VII", "NCO.OP.160", "GM1", "GM2"):
            self.assertIn(required, scope)
        self.assertNotRegex(scope, r"(?i)future\s+LAPL/PPL|continual reassessment")
        self.assertIn(
            "одно наличие лицензии не определяет применимость Part-NCO",
            scope,
        )
        self.assertNotRegex(
            scope,
            r"(?is)(?:испан\w*|Spanish).{0,80}ULM|ULM.{0,80}(?:испан\w*|Spanish)",
        )

        for relative_path in (
            TASK6_CHAPTERS[0], TASK6_CHAPTERS[1], TASK6_CHAPTERS[3],
            TASK6_CHAPTERS[5], TASK6_CHAPTERS[6],
        ):
            chapter = (ROOT / relative_path).read_text(encoding="utf-8")
            extension = chapter.split("## Расширение LAPL/PPL", 1)[1].split(
                "## Безопасность", 1
            )[0]
            with self.subTest(relative_path=relative_path):
                self.assertIn("SRC-EASA-AIR-OPS-2026", extension)
                self.assertIn("SRC-BOE-RD-765-2022", extension)
                self.assertIn("проверено 2026-07-13", extension)

    def test_task6_scenarios_are_not_presented_as_climatology(self):
        wind = (ROOT / TASK6_CHAPTERS[1]).read_text(encoding="utf-8")
        self.assertIn(
            "Сценарии — условные синтетические проверки механизма, "
            "а не климатология или прогноз.",
            wind,
        )
        self.assertNotIn("Сценарии дают климатологическую ориентацию", wind)

    def test_task6_visibility_and_icao_source_scopes_are_narrow(self):
        water = _plain_markdown(
            (ROOT / TASK6_CHAPTERS[2]).read_text(encoding="utf-8")
        )
        self.assertRegex(
            water,
            r"(?is)METAR.{0,100}преобладающ\w+\s+горизонтальн\w+\s+видимост\w+"
            r".{0,180}не.{0,50}подтвержда\w+.{0,100}(?:рельеф|препятств)",
        )
        self.assertRegex(
            water,
            r"SRC-ENAIRE-AIP-GEN-3-5-2026.{0,100}§§3\.2\.1–3\.2\.2",
        )
        sources = {
            source["id"]: source for source in json.loads(SOURCE_REGISTRY.read_text())
        }
        self.assertEqual(
            "21st Edition, August 2025",
            sources["SRC-ICAO-ANNEX3-2025"]["edition"],
        )

    def test_task6_rejects_universal_limits_and_refutes_shortcuts(self):
        text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK6_CHAPTERS
        )
        self.assertEqual([], weather_safety_errors(text))
        plain = _plain_markdown(text)
        for phrase in (
            "CAVOK не означает", "METAR не описывает весь маршрут",
            "TAF не является обещанием", "TEMPO нельзя игнорировать",
            "PROB30 нельзя считать пренебрежимо малой", "отсутствие G не означает",
            "SPECI не является исправлением TAF", "отсутствие SIGMET не означает",
            "QNH не показывает высоту над ВПП", "QFE не является универсально обязательным",
            "линзовидное облако не обязательно", "морской бриз не всегда слабый",
            "архивный снимок не является текущей погодой", "климатология не является прогнозом",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), plain.casefold())
        self.assertRegex(plain, r"(?is)нет\s+универсальн\w+.{0,100}ULM.{0,180}(?:ветр|порыв|видимост|гроз)")

    def test_task6_sources_and_terms_are_registered(self):
        sources = {source["id"] for source in json.loads(SOURCE_REGISTRY.read_text())}
        required_sources = {
            "SRC-AEMET-GUIA-MET-2025", "SRC-AEMET-CODE-FORMS-2021",
            "SRC-AEMET-AERODROME-GUIDES", "SRC-ENAIRE-AIP-GEN-3-5-2026",
            "SRC-ENAIRE-AIP-ENR-1-7-2026", "SRC-EASA-AIR-OPS-2026",
            "SRC-WMO-CLOUD-ATLAS-2017", "SRC-ICAO-DOC-7488", "SRC-ICAO-ANNEX3-2025",
            "SRC-FAA-AWH-28B-2026",
        }
        self.assertTrue(required_sources.issubset(sources), required_sources - sources)
        audit = (ROOT / "docs/sources/audit-technical.md").read_text(encoding="utf-8")
        registry_md = SOURCE_REGISTRY_MD.read_text(encoding="utf-8")
        for source_id in required_sources:
            self.assertIn(source_id, audit)
            self.assertIn(source_id, registry_md)
        canonical = {term["canonical"] for term in json.loads(TERMS_REGISTRY.read_text())}
        for term in (
            "International Standard Atmosphere (ISA)", "flight level (FL)", "QFE",
            "CAVOK", "SPECI", "TREND", "SIGMET", "AIRMET", "GAMET",
            "Aeronautical Meteorological Self-service (AMA)", "density altitude",
            "wind shear", "VFR into IMC (VFR2IMC)",
        ):
            self.assertIn(term, canonical)

    def test_task6_svgs_are_accessible_original_and_semantic(self):
        namespace = "{http://www.w3.org/2000/svg}"
        required_ids = (
            {"conceptual-front", "conceptual-low", "conceptual-high", "forecast-warning"},
            {"avoidance-boundary", "updraft", "downdraft", "hail", "lightning", "no-distance"},
            {"observation", "forecast", "change-groups", "not-live-weather"},
        )
        for relative_path, expected_ids in zip(TASK6_SVGS, required_ids):
            root = ET.parse(ROOT / relative_path).getroot()
            with self.subTest(path=relative_path):
                self.assertEqual(f"{namespace}svg", root.tag)
                self.assertEqual("img", root.attrib.get("role"))
                self.assertTrue(root.attrib.get("aria-labelledby"))
                self.assertIsNotNone(root.find(f"{namespace}title"))
                self.assertIsNotNone(root.find(f"{namespace}desc"))
                self.assertFalse(list(root.iter(f"{namespace}image")))
                ids = {item.attrib["id"] for item in root.iter() if "id" in item.attrib}
                self.assertTrue(expected_ids.issubset(ids), expected_ids - ids)
                vx, vy, vw, vh = (float(value) for value in root.attrib["viewBox"].split())
                self.assertLessEqual(vw, 700)
                text_sizes = [
                    float(item.attrib["font-size"].removesuffix("px"))
                    for item in root.iter(f"{namespace}text") if "font-size" in item.attrib
                ]
                self.assertTrue(text_sizes)
                self.assertGreaterEqual(min(text_sizes) * 340 / vw, 14.0)
                for item in root.iter():
                    bbox = element_bbox(item)
                    if bbox is None:
                        continue
                    x, y, width, height = bbox
                    self.assertGreaterEqual(x, vx)
                    self.assertGreaterEqual(y, vy)
                    self.assertLessEqual(x + width, vx + vw)
                    self.assertLessEqual(y + height, vy + vh)

        fronts = " ".join(ET.parse(ROOT / TASK6_SVGS[0]).getroot().itertext()).casefold()
        storm = " ".join(ET.parse(ROOT / TASK6_SVGS[1]).getroot().itertext()).casefold()
        decoder = " ".join(ET.parse(ROOT / TASK6_SVGS[2]).getroot().itertext()).casefold()
        self.assertIn("концептуаль", fronts)
        self.assertIn("не прогноз", fronts)
        self.assertIn("нет универсальной дистанции", storm)
        self.assertIn("не текущая погода", decoder)

    def test_task6_svgs_encode_reviewed_comparisons_and_escape_logic(self):
        fronts_root = ET.parse(ROOT / TASK6_SVGS[0]).getroot()
        fronts = {item.attrib.get("id"): item for item in fronts_root.iter()}
        self.assertIn("warm-front-panel", fronts)
        self.assertIn("cold-front-panel", fronts)
        self.assertFalse(
            bboxes_overlap(
                element_bbox(fronts["warm-front-panel"]),
                element_bbox(fronts["cold-front-panel"]),
            )
        )
        wind_text = (ROOT / TASK6_CHAPTERS[1]).read_text(encoding="utf-8")
        front_text = (ROOT / TASK6_CHAPTERS[3]).read_text(encoding="utf-8")
        self.assertNotIn("fronts-and-pressure.svg", wind_text)
        self.assertIn("fronts-and-pressure.svg", front_text)

        storm_root = ET.parse(ROOT / TASK6_SVGS[1]).getroot()
        storm = {item.attrib.get("id"): item for item in storm_root.iter()}
        self.assertIn("escape-path", storm)
        boundary = element_bbox(storm["avoidance-boundary"])
        escape = element_bbox(storm["escape-path"])
        self.assertTrue(
            escape[0] + escape[2] < boundary[0]
            or escape[0] > boundary[0] + boundary[2]
        )
        title = storm["no-distance-title"]
        self.assertGreaterEqual(len(list(title)), 2)
        self.assertFalse(
            bboxes_overlap(
                element_bbox(storm["updraft-label"]),
                element_bbox(storm["downdraft-label"]),
            )
        )

        decoder_root = ET.parse(ROOT / TASK6_SVGS[2]).getroot()
        decoder = {item.attrib.get("id"): item for item in decoder_root.iter()}
        self.assertFalse(
            bboxes_overlap(
                element_bbox(decoder["observation"]),
                element_bbox(decoder["forecast"]),
            )
        )
        parents = {
            child.attrib.get("id"): parent.attrib.get("id")
            for parent in decoder_root.iter()
            for child in parent
            if child.attrib.get("id")
        }
        self.assertEqual("observation", parents["trend"])
        self.assertEqual("forecast", parents["change-groups"])


def radio_phraseology_safety_errors(text):
    """Return unsafe radio shortcuts from learner prose, clause by clause."""
    learner_text = re.split(
        r"(?m)^##\s+(?:Контрольные вопросы|Типичные ошибки)\b", text, maxsplit=1
    )[0]
    patterns = (
        r"\bROGER\b.{0,45}(?:полн\w+\s+)?(?:readback|повтор\w+)",
        r"(?:traffic information|информаци\w+\s+о\s+движен)\w*.{0,45}(?:явля\w+|это)\s+(?:ATC\s+)?(?:clearance|разрешен|разрешён)",
        r"(?:молчани\w+|тишин\w+).{0,45}(?:означа\w+|доказыва\w+).{0,25}(?:нет|отсутств)\w*\s+движен",
        r"радиовызов.{0,45}(?:созда[её]т|да[её]т).{0,25}(?:приоритет|право\s+пути)",
        r"(?:English|английск\w+).{0,35}(?:Spanish|испанск\w+).{0,40}(?:свободн|произвольн)\w+\s+смеш",
        r"кажд\w+\s+сообщени\w+.{0,35}(?:одинаков|те\s+же)\w*\s+(?:поля|элементы)",
        r"\bMAYDAY\b.{0,35}\bPAN\s+PAN\b.{0,35}(?:взаимозамен|одно\s+и\s+то\s+же)",
        r"\b7600\b.{0,25}(?:код\w+\s+)?(?:бедств|distress)",
        r"\b7700\b.{0,25}(?:отказ\w+\s+радио|radio failure)",
        r"\b121[.,]500\b.{0,40}(?:обычн\w+|планов\w+|рутинн\w+)\s+(?:проверк|radio check)",
        r"сохран[её]нн\w+\s+частот\w+.{0,45}(?:всегда\s+)?(?:актуальн|действующ)",
        r"\bAFIS\b.{0,35}(?:выда[её]т|да[её]т).{0,25}(?:ATC\s+)?(?:clearance|разрешен|разрешён)",
        r"(?:uncontrolled|неконтролируем\w+)\w*.{0,35}(?:означа\w+|это).{0,20}(?:нет|отсутств\w+)\s+правил",
        r"светов\w+\s+сигнал\w+.{0,35}(?:необязательн|декорац)",
        r"(?:неразборчив|не\s+расслыш).{0,35}(?:придум|сочин).{0,35}(?:разрешен|разрешён)\w+\s+(?:на\s+)?ВПП",
        r"(?:ULM|MAF).{0,20}RTC.{0,40}(?:достаточн|разреша\w+).{0,35}(?:controlled airspace|контролируем\w+\s+пространств)",
    )
    errors = []
    for sentence in _sentences(learner_text):
        clauses = re.split(r"(?i);\s*|,\s*(?:а|но|зато|и)\s+", _plain_markdown(sentence))
        for clause in clauses:
            for pattern in patterns:
                match = re.search(pattern, clause, re.IGNORECASE)
                if not match:
                    continue
                prefix = clause[max(0, match.start() - 36):match.start()]
                within = clause[max(0, match.start() - 8):match.end()]
                negated = re.search(
                    r"(?i)(?:\bне\s+(?:явля\w+|означа\w+|созда[её]т|да[её]т|"
                    r"выда[её]т|можно|достаточн|разреша\w+|заменя\w+|гарантир\w+)|"
                    r"\bне\s+взаимозамен|\bне\s+обязательн|\bне\s+обязано\b|\bне\s+означает\b|"
                    r"\bнедостаточн)",
                    within,
                ) or re.search(r"(?i)\bневерн\w*\s*,?\s*$", prefix)
                if not negated:
                    errors.append(clause.strip())
                break
    return errors


class Task7CommunicationsTests(unittest.TestCase):
    def _all_text(self):
        return "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in TASK7_CHAPTERS
        )

    def _scenario(self, number):
        text = self._all_text()
        match = re.search(
            rf"(?ms)^###\s+Сценарий RTC-{number:02d}\b.*?"
            rf"(?=^###\s+Сценарий RTC-|^##\s|\Z)",
            text,
        )
        self.assertIsNotNone(match, f"RTC-{number:02d}")
        return match.group(0)

    def test_radio_guard_rejects_clause_local_unsafe_probes(self):
        probes = (
            "ROGER является полным readback.",
            "Traffic information является ATC clearance.",
            "Молчание в эфире означает отсутствие движения.",
            "Радиовызов создаёт право пути.",
            "English и Spanish можно свободно смешивать.",
            "Каждое сообщение содержит одинаковые поля.",
            "MAYDAY и PAN PAN взаимозаменяемы.",
            "7600 — код бедствия.",
            "7700 — код отказа радио.",
            "121.500 подходит для обычной проверки радио.",
            "Сохранённая частота всегда актуальна.",
            "AFIS выдаёт ATC clearance.",
            "Uncontrolled означает отсутствие правил.",
            "Световые сигналы — необязательная декорация.",
            "Если не расслышал, можно придумать разрешение на ВПП.",
            "ULM с RTC достаточно для controlled airspace.",
            "ROGER не является полным readback, зато AFIS выдаёт clearance.",
        )
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertTrue(radio_phraseology_safety_errors(probe))
        for safe in (
            "ROGER не является полным readback.",
            "Traffic information не является ATC clearance.",
            "Молчание не означает отсутствия движения.",
            "AFIS не выдаёт ATC clearance.",
            "ULM с RTC недостаточно для controlled airspace.",
        ):
            with self.subTest(safe=safe):
                self.assertEqual([], radio_phraseology_safety_errors(safe))

    def test_task7_files_exist_and_are_in_navigation(self):
        nav_paths = mkdocs_nav_paths((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        for relative_path in (*TASK7_CHAPTERS, TASK7_REFERENCE):
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), nav_paths)
        self.assertTrue((ROOT / TASK7_SVG).is_file(), TASK7_SVG)

    def test_task7_template_scope_and_stable_anchors(self):
        required = {
            "purpose", "outcomes", "applicability", "theory", "ulm-application",
            "part-fcl-extension", "safety", "common-errors", "summary",
            "review-questions", "sources",
        }
        for relative_path in TASK7_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertEqual([], explicit_atx_heading_errors(text))
                self.assertTrue(required.issubset(markdown_anchors(text)))
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, applicability_table_labels(text))
                plain = _plain_markdown(text)
                self.assertRegex(plain, r"(?is)ULM.{0,180}Испани")
                self.assertRegex(plain, r"(?is)(?:LAPL|PPL).{0,220}(?:позже|переход|Part-FCL)")

    def test_task7_required_topics_and_exact_operational_boundaries(self):
        text = self._all_text()
        anchors = markdown_anchors(text)
        required = {
            "communication-model", "vhf-limitations", "alphabet-numbers-time",
            "callsigns", "message-structure", "mandatory-readback", "plain-language",
            "controlled-departure", "conditional-clearance", "controlled-entry",
            "traffic-information", "controlled-arrival", "afis-boundary",
            "air-to-air", "distress", "urgency", "communication-failure",
            "ssr-codes", "light-signals",
        }
        self.assertTrue(required.issubset(anchors), required - anchors)
        plain = _plain_markdown(text)
        for pattern in (
            r"полн\w+\s+позывн\w+.{0,130}перв\w+\s+контакт.{0,160}сокращ.{0,120}станци",
            r"TAKE-OFF.{0,160}(?:только|исключительн).{0,120}(?:разрешен|разрешён|отмен)",
            r"STANDBY.{0,100}не.{0,35}(?:одобр|разреш)",
            r"121[.,]500.{0,130}(?:необходим|целесообраз)",
            r"7000.{0,130}не.{0,45}универсальн\w+.{0,30}(?:VFR|ПВП)",
            r"IDENT.{0,100}только.{0,40}(?:указан|команд|инструкц)",
        ):
            self.assertRegex(plain, re.compile(pattern, re.IGNORECASE | re.DOTALL))

    def test_reviewed_controlled_exchanges_use_exact_current_forms(self):
        rtc01 = self._scenario(1)
        self.assertIn(
            "[CALLSIGN], [STATION], READABILITY FOUR",
            rtc01,
        )
        self.assertIn("SERA.14070", _plain_markdown(rtc01))

        rtc03 = self._scenario(3)
        self.assertIn("[STATION], [FULL CALLSIGN]", rtc03)
        self.assertIn("[FULL CALLSIGN], [STATION]", rtc03)
        english_line = next(
            line for line in rtc03.splitlines() if line.startswith("**English:**")
        )
        self.assertNotIn("PASS YOUR MESSAGE", english_line)
        self.assertIn("SERA.14055", _plain_markdown(rtc03))

        rtc04 = self._scenario(4)
        self.assertIn("HOLD SHORT OF RUNWAY [RUNWAY]", rtc04)
        self.assertIn("HOLDING SHORT OF RUNWAY [RUNWAY], [CALLSIGN]", rtc04)
        self.assertIn("MANTENGA FUERA DE PISTA [RUNWAY]", rtc04)
        self.assertIn("MANTENGO FUERA DE PISTA [RUNWAY], [CALLSIGN]", rtc04)
        self.assertIn("Annex V 1.4.9(d–f)", rtc04)
        self.assertIn("SERA.8015(e)", _plain_markdown(rtc04))

        rtc06 = self._scenario(6)
        for phrase in (
            "(CONDITION), LINE UP, (BRIEF REITERATION)",
            "(CONDITION), LINING UP, (BRIEF REITERATION)",
            "(CONDICIÓN), ALINEE (O ENTRE) Y MANTENGA, (BREVE REITERACIÓN)",
            "(CONDICIÓN), ALINEANDO (O ENTRANDO) Y MANTENIENDO, (BREVE REITERACIÓN)",
            "Annex V 1.4.11(i–j)",
        ):
            self.assertIn(phrase, rtc06)
        self.assertIn("GM1 SERA.8015(ec)", _plain_markdown(rtc06))

        rtc07 = self._scenario(7)
        self.assertIn("LINE UP [AND WAIT]", rtc07)
        self.assertIn("ALINEE (O ENTRE) [Y MANTENGA]", rtc07)
        self.assertIn("Annex V 1.4.11(f–g)", rtc07)
        self.assertRegex(
            _plain_markdown(rtc07),
            r"(?is)PISTA\s+\[RUNWAY\].{0,180}(?:нескольк|неоднознач|спут)",
        )

        rtc08 = self._scenario(8)
        protected_lines = "\n".join(
            line for line in rtc08.splitlines()
            if line.startswith(("**English:**", "**Español:**"))
        )
        self.assertNotIn("[WIND]", protected_lines)

        rtc13 = self._scenario(13)
        self.assertIn("ENTRE (O INGRESE) EN", rtc13)
        self.assertNotIn("INCORPÓRESE", rtc13)

    def test_position_report_matches_amended_sera_8025(self):
        chapter = (ROOT / TASK7_CHAPTERS[3]).read_text(encoding="utf-8")
        position_section = re.search(
            r"(?ms)^###\s+[^\n]*\{#position-report\}.*?(?=^###\s|^##\s|\Z)",
            chapter,
        ).group(0)
        plain = _plain_markdown(position_section)
        for pattern in (
            r"идентификац\w+\s+воздушн\w+\s+судн",
            r"позиц",
            r"врем",
            r"скорост\w+.{0,90}(?:назнач|задан)",
            r"друг\w+\s+сведен\w+.{0,90}(?:указал|указан|потребован)",
            r"обязательн\w+\s+пункт.{0,120}врем.{0,120}(?:уров|высот)",
            r"следующ\w+\s+пункт.{0,180}(?:только|лишь).{0,100}(?:процедур|указан|инструкц)",
        ):
            self.assertRegex(plain, re.compile(pattern, re.IGNORECASE | re.DOTALL))
        self.assertIn("SERA.8025", _plain_markdown(position_section))

        rtc10 = self._scenario(10)
        for field in (
            "[CALLSIGN]", "[POSITION]", "[TIME]", "[LEVEL]",
            "[ASSIGNED SPEED]", "[OTHER INSTRUCTED INFORMATION]",
        ):
            self.assertIn(field, rtc10)
        self.assertRegex(
            _plain_markdown(rtc10),
            r"(?is)\[NEXT POINT\].{0,200}(?:только|если).{0,120}(?:процедур|указан|инструкц)",
        )

    def test_blind_transmission_is_repeated_verbatim_and_receiver_failure_is_distinct(self):
        chapter = (ROOT / TASK7_CHAPTERS[5]).read_text(encoding="utf-8")
        rtc20 = self._scenario(20)
        self.assertNotIn("THIS MESSAGE TWICE", chapter)
        self.assertNotIn("MENSAJE REPETIDO", chapter)
        complete_message = (
            "TRANSMITTING BLIND, [STATION], [CALLSIGN], RADIO FAILURE, "
            "[POSITION], [ALTITUDE], LANDING AT [SUITABLE AERODROME]"
        )
        self.assertGreaterEqual(rtc20.count(complete_message), 2)
        self.assertIn("TRANSMITTING BLIND DUE TO RECEIVER FAILURE", chapter)
        failure_text = _plain_markdown(chapter)
        self.assertRegex(
            failure_text,
            r"(?is)receiver failure.{0,420}(?:врем\w+\s+следующ\w+\s+.*передач|"
            r"time of (?:the )?next transmission)",
        )
        self.assertRegex(
            failure_text,
            r"(?is)receiver failure.{0,520}(?:намерен|intended action)",
        )
        self.assertIn("SERA.14085(b)", failure_text)

    def test_digits_and_operational_number_groups_are_taught_step_by_step(self):
        chapter = (ROOT / TASK7_CHAPTERS[0]).read_text(encoding="utf-8")
        number_section = re.search(
            r"(?ms)^###\s+[^\n]*\{#alphabet-numbers-time\}.*?(?=^###\s|^##\s|\Z)",
            chapter,
        ).group(0)
        for digit, spoken in enumerate(
            ("ZE-RO", "WUN", "TOO", "TREE", "FOW-er", "FIFE", "SIX", "SEV-en", "AIT", "NIN-er")
        ):
            self.assertRegex(number_section, rf"(?m)^\|\s*{digit}\s*\|\s*{re.escape(spoken)}\s*\|")
        for example in (
            "118.005 → ONE ONE EIGHT DECIMAL ZERO ZERO FIVE",
            "080° → HEADING ZERO EIGHT ZERO",
            "3 400 ft → THREE THOUSAND FOUR HUNDRED FEET",
            "QNH 1009 → QNH ONE ZERO ZERO NINE",
            "0920 UTC → ZERO NINE TWO ZERO",
        ):
            self.assertIn(example, number_section)
        plain_number_section = _plain_markdown(number_section)
        for pinpoint in (
            "SERA.14020", "SERA.14035", "SERA.14040", "SERA.14045",
            "RCA 10.5.2.1.3.1.1",
        ):
            self.assertIn(pinpoint, plain_number_section)
        self.assertNotIn("SERA.14015", plain_number_section)

    def test_task7_source_scopes_and_adjacent_pinpoints_are_precise(self):
        sources = {item["id"]: item for item in json.loads(SOURCE_REGISTRY.read_text())}
        sera_scope = sources["SRC-EASA-SERA-2025"]["scope"]
        for pinpoint in (
            "SERA.8025", "SERA.14055", "SERA.14070", "SERA.14085",
            "SERA.14095",
        ):
            self.assertIn(pinpoint, sera_scope)
        rd_scope = sources["SRC-BOE-RD-1180-2018"]["scope"]
        for pinpoint in (
            "RCA 10.5.2.1.3.1.1", "RCA 10.5.3",
            "RCA 4.7.1.5.1.3", "Annex V 1.4.9", "Annex V 1.4.11",
            "Annex V 1.4.14–1.4.18",
        ):
            self.assertIn(pinpoint, rd_scope)
        self.assertIn("SRC-FAA-AIM-RADIO-2026", sources)

        adjacency = {
            (0, "vhf-limitations"): ("SRC-FAA-AIM-RADIO-2026", "AIM 4-2-1"),
            (0, "frequency-discipline"): ("SRC-EASA-SERA-2025", "SERA.14045"),
            (0, "callsigns"): ("SRC-EASA-SERA-2025", "SERA.14050", "SERA.14055"),
            (1, "plain-language"): ("SRC-EASA-SERA-2025", "SERA.14001", "SERA.14075"),
            (4, "air-to-air"): ("SRC-ENAIRE-AIP-GEN-3-4-2026", "SRC-FAA-AIM-RADIO-2026"),
        }
        for (chapter_index, anchor), expected in adjacency.items():
            chapter = (ROOT / TASK7_CHAPTERS[chapter_index]).read_text(encoding="utf-8")
            section = re.search(
                rf"(?ms)^###\s+[^\n]*\{{#{re.escape(anchor)}\}}.*?(?=^###\s|^##\s|\Z)",
                chapter,
            )
            self.assertIsNotNone(section, anchor)
            for token in expected:
                self.assertIn(token, _plain_markdown(section.group(0)), f"{anchor}: {token}")

    def test_ssr_meaning_and_abbreviations_are_unambiguous(self):
        terms = {item["canonical"]: item for item in json.loads(TERMS_REGISTRY.read_text())}
        clearance = terms["ATC clearance"]
        self.assertIsNone(clearance["abbreviation"])
        ssr = terms["secondary surveillance radar (SSR)"]
        self.assertNotRegex(ssr["russian"].casefold(), r"ответчик|транспондер")

        rows = []
        for line in ABBREVIATIONS.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\|\s*([^|]+?)\s*\|", line)
            if match and match.group(1).strip() not in {"Сокращение", "---"}:
                rows.append(match.group(1).strip())
        self.assertEqual(1, rows.count("ATC"))
        self.assertEqual(1, rows.count("SSR"))
        ssr_line = next(line for line in ABBREVIATIONS.read_text(encoding="utf-8").splitlines() if line.startswith("| SSR |"))
        self.assertNotRegex(ssr_line.casefold(), r"ответчик|транспондер")

    def test_scenarios_and_question_rationales_are_russian_first(self):
        def unexplained_latin(value):
            value = re.sub(r"`[^`\n]*`", " ", value)
            value = re.sub(r"\[[^\]\n]+\](?:\[[^\]\n]*\]|\([^\n)]+\))", " ", value)
            value = re.sub(r"\[[A-Z0-9_ /-]+\]", " ", value)
            value = re.sub(r"<[^>]+>|SRC-[A-Z0-9-]+", " ", value)
            return re.findall(r"(?<![A-Za-z])[a-z][a-z'-]{2,}(?![A-Za-z])", value)

        errors = []
        for number in range(1, 21):
            block = self._scenario(number)
            heading = block.splitlines()[0].split("—", 1)[-1]
            if not re.search(r"[А-Яа-яЁё]", heading):
                errors.append(f"RTC-{number:02d} heading: {heading}")
            for label in (
                "Тип обслуживания", "Контекст", "Пояснение",
                "[Readback][readback]/[acknowledgement][acknowledgement]",
                "Решение при сомнении",
            ):
                match = re.search(rf"(?m)^\*\*{re.escape(label)}:\*\*\s*(.+)$", block)
                self.assertIsNotNone(match, f"RTC-{number:02d}: {label}")
                latin = unexplained_latin(match.group(1))
                if latin:
                    errors.append(f"RTC-{number:02d} {label}: {' '.join(latin)}")

        for relative_path in TASK7_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            for label in ("Почему", "Почему главный отвлекающий вариант неверен"):
                for match in re.finditer(rf"(?m)^\*\*{label}:\*\*\s*(.+)$", text):
                    latin = unexplained_latin(match.group(1))
                    if latin:
                        line = text.count("\n", 0, match.start()) + 1
                        errors.append(f"{relative_path}:{line} {label}: {' '.join(latin)}")
        self.assertEqual([], errors)

    def test_all_task7_learner_prose_is_russian_first_outside_labelled_transmissions(self):
        errors = []
        for relative_path in TASK7_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            text = re.sub(r"(?m)^\*\*(?:English|Español):\*\*.*$", "", text)
            # A linked canonical term is the course's required cross-reference to
            # its Russian/English/Spanish glossary explanation, not unexplained
            # English learner prose.  Mask both inline and reference-style
            # glossary links while leaving unlinked hybrids detectable.
            glossary_reference_keys = {
                match.group(1)
                for match in re.finditer(
                    r"(?m)^\[([^\]]+)\]:\s+[^\n]*glossary\.md#term-", text
                )
            }
            text = re.sub(
                r"\[[^\]\n]+\]\([^\n)]*glossary\.md#term-[^\n)]+\)",
                "термин",
                text,
            )
            if glossary_reference_keys:
                keys = "|".join(
                    re.escape(key)
                    for key in sorted(glossary_reference_keys, key=len, reverse=True)
                )
                text = re.sub(rf"\[[^\]\n]+\]\[(?:{keys})\]", "термин", text)
            chapter_errors = unexplained_english_phrase_occurrences(text)
            errors.extend(
                f"{relative_path}:{line} {phrase}"
                for line, phrase in chapter_errors
            )
        self.assertEqual([], errors)

    def test_aa_templates_are_explicitly_local_non_normative_field_sets(self):
        chapter = (ROOT / TASK7_CHAPTERS[4]).read_text(encoding="utf-8")
        aa_section = re.search(
            r"(?ms)^###\s+[^\n]*\{#air-to-air\}.*?(?=^###\s|^##\s|\Z)", chapter
        ).group(0)
        plain = _plain_markdown(aa_section)
        self.assertRegex(
            plain,
            r"(?is)(?:не\s+явля\w+|ненормативн\w+).{0,100}(?:универсальн\w+\s+фразеолог|скрипт)",
        )
        self.assertRegex(plain, r"(?is)набор\w*\s+полей.{0,180}(?:AIP|местн\w+\s+форм)")
        self.assertRegex(plain, r"(?is)SALIDA.{0,160}SALIENDO")

    def test_emergency_station_responses_and_placeholder_legend_are_concrete(self):
        chapter = (ROOT / TASK7_CHAPTERS[5]).read_text(encoding="utf-8")
        for generic in ("[ASSISTANCE/QUESTION]", "[INSTRUCTION/INFORMATION]"):
            self.assertNotIn(generic, chapter)
        for number in (18, 19):
            block = self._scenario(number)
            self.assertRegex(block, r"(?is)station:.{0,300}(?:REPORT|ROGER).{0,120}(?:RUNWAY|PERSONS|ENDURANCE|WIND)")
            self.assertRegex(block, r"(?is)estación:.{0,300}(?:NOTIFIQUE|RECIBIDO).{0,120}(?:PISTA|PERSONAS|AUTONOMÍA|VIENTO)")
        self.assertRegex(
            _plain_markdown(chapter),
            r"(?is)обозначени\w+\s+переменн.{0,220}(?:английск|испанск).{0,220}не\s+произнос",
        )

    def test_mayday_threshold_preserves_serious_and_or_imminent_condition(self):
        chapter = (ROOT / TASK7_CHAPTERS[5]).read_text(encoding="utf-8")
        blocks = {
            "urgency upgrade": re.search(
                r"(?ms)^###\s+PAN PAN:.*?\{#urgency\}.*?(?=^###\s|^##\s|\Z)",
                chapter,
            ).group(0),
            "RTC-19 decision": self._scenario(19),
            "summary": re.search(
                r"(?ms)^##\s+Конспект.*?\{#summary\}.*?(?=^##\s|\Z)",
                chapter,
            ).group(0),
            "Q-RTC-026": re.search(
                r"(?ms)^###\s+Q-RTC-026\b.*?(?=^###\s|^##\s|\Z)",
                chapter,
            ).group(0),
        }
        for name, block in blocks.items():
            plain = _plain_markdown(block)
            with self.subTest(block=name):
                self.assertRegex(
                    plain,
                    r"(?is)серь[её]зн\w+\s+и/или\s+непосредственн\w+"
                    r".{0,120}(?:немедленн\w+\s+помощ|"
                    r"необходимост\w+\s+немедленн\w+\s+помощ)",
                )
                self.assertNotRegex(
                    plain,
                    r"(?is)серь[её]зн\w+\s+и\s+непосредственн\w+",
                )

    def test_lebg_intersection_departure_scope_is_not_generalised(self):
        chapter = (ROOT / TASK7_CHAPTERS[4]).read_text(encoding="utf-8")
        aa_section = re.search(
            r"(?ms)^###\s+[^\n]*\{#air-to-air\}.*?(?=^###\s|^##\s|\Z)",
            chapter,
        ).group(0)
        sources = {item["id"]: item for item in json.loads(SOURCE_REGISTRY.read_text())}
        evidence = (
            aa_section,
            sources["SRC-ENAIRE-AIP-LEBG-2026"]["scope"],
            (ROOT / "docs/sources/official-sources.md").read_text(encoding="utf-8"),
            (ROOT / "docs/sources/audit-technical.md").read_text(encoding="utf-8"),
        )
        for value in evidence:
            self.assertRegex(
                _plain_markdown(value),
                r"(?is)AD\s*2\.20.{0,220}(?:вылет\w*\s+с\s+пересеч|"
                r"intersection\s+departure)",
            )

    def test_rtc07_runway_designator_readback_remains_conditional(self):
        rtc07 = self._scenario(7)
        readback = re.search(
            r"(?m)^\*\*\[Readback\]\[readback\]/"
            r"\[acknowledgement\]\[acknowledgement\]:\*\*\s*(.+)$",
            rtc07,
        ).group(1)
        self.assertRegex(
            _plain_markdown(readback),
            r"(?is)обозначени\w*\s+ВПП.{0,120}(?:если|когда).{0,120}"
            r"(?:включ[её]н|требу|неоднознач|нескольк)",
        )

    def test_reviewed_question_distractors_are_plausible_novice_errors(self):
        weak = {
            6: ("D", "Сообщение о предполагаемом времени вылета"),
            8: ("C", "Нужно немедленно выполнить ожидаемое действие"),
            14: ("D", "Потому что слово используется только в météo reports"),
            15: ("D", "Только если изменена частота"),
            16: ("D", "Переключиться на emergency frequency"),
            18: ("D", "Go-around запрещён"),
            19: ("D", "До пересечения holding point при вылете"),
            20: ("D", "Ждать, пока другой pilot даст совет"),
            21: ("D", "Отмену published circuit"),
            22: ("D", "Runway закрыта для всех остальных"),
        }
        for number, (letter, old) in weak.items():
            block = re.search(
                rf"(?ms)^### Q-RTC-{number:03d}\b.*?(?=^### Q-RTC-|^##\s|\Z)",
                self._all_text(),
            ).group(0)
            option = re.search(rf"(?m)^{letter}\.\s+(.+)$", block).group(1)
            self.assertNotIn(old, option)
            self.assertGreaterEqual(len(re.findall(r"[А-Яа-яЁёA-Za-z]+", _plain_markdown(option))), 5)

    def test_task7_ulm_rtc_and_part_fcl_gates_are_separate(self):
        text = self._all_text()
        plain = _plain_markdown(text)
        for pattern in (
            r"ULM.{0,90}MAF.{0,90}RTC.{0,160}недостаточн.{0,120}контролируем",
            r"1\s+апрел\w+\s+2026.{0,220}Part-FCL.{0,180}эквивалентн",
            r"(?:Communications|Связь).{0,120}экзамен.{0,180}не.{0,80}FCL\.055",
            r"национальн\w+\s+RTC.{0,160}не.{0,70}автоматическ.{0,100}(?:зач[её]т|Part-FCL)",
            r"FCL\.055.{0,180}(?:Level\s*4|уровн\w+\s*4)",
        ):
            self.assertRegex(plain, re.compile(pattern, re.IGNORECASE | re.DOTALL))
        for chapter in TASK7_CHAPTERS:
            self.assertEqual([], radio_phraseology_safety_errors((ROOT / chapter).read_text(encoding="utf-8")))

    def test_task7_has_twenty_complete_labelled_synthetic_scenarios(self):
        text = self._all_text()
        matches = list(re.finditer(
            r"(?m)^###\s+Сценарий RTC-(\d{2})\s+—\s+.+\{#scenario-rtc-\1\}\s*$",
            text,
        ))
        self.assertEqual(20, len(matches))
        self.assertEqual([f"{number:02d}" for number in range(1, 21)], [m.group(1) for m in matches])
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            next_h2 = re.search(r"(?m)^##\s+", text[match.end():end])
            if next_h2:
                end = match.end() + next_h2.start()
            block = text[match.end():end]
            plain_block = _plain_markdown(block)
            with self.subTest(scenario=match.group(1)):
                self.assertIn("СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА", block)
                for label in (
                    "Тип обслуживания", "Контекст", "English", "Español",
                    "Пояснение", "Readback/acknowledgement", "Решение при сомнении",
                ):
                    self.assertRegex(plain_block, rf"{re.escape(label)}:")
                self.assertRegex(block, r"SRC-[A-Z0-9-]+")
                self.assertRegex(block, r"проверено\s+2026-07-13")
        self.assertEqual(20, text.count("СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА"))

    def test_scenarios_cover_services_and_required_exchanges(self):
        plain = _plain_markdown(self._all_text())
        for service in (
            r"контролируем\w*\s+ATS",
            r"AFIS",
            r"неконтролируем\w*\s+A/A",
            r"(?:аварийн|бедств|срочност)",
        ):
            self.assertRegex(plain, re.compile(service, re.IGNORECASE))
        for token in (
            "RADIO CHECK", "CONTACT [NEXT STATION] [FREQUENCY]", "TAXI", "BEHIND", "LINE UP",
            "CLEARED FOR TAKE-OFF", "POSITION", "REQUEST ENTRY", "TRAFFIC",
            "REPORT BASE", "CLEARED TO LAND", "GO AROUND", "RUNWAY VACATED",
            "MAYDAY", "PAN PAN", "7600",
        ):
            self.assertIn(token.casefold(), plain.casefold())
        self.assertRegex(plain, r"(?is)AFIS.{0,180}не.{0,60}(?:clearance|разрешен|разрешён)")
        self.assertRegex(plain, r"(?is)A/A.{0,200}(?:намерени|information).{0,180}не.{0,60}(?:clearance|разрешен|разрешён)")

    def test_scenario_data_are_placeholders_and_dynamic_warnings_are_explicit(self):
        text = self._all_text()
        for match in re.finditer(r"\b\d{3}[.,]\d{3}\b", text):
            with self.subTest(frequency=match.group()):
                context = text[max(0, match.start() - 180):match.end() + 180]
                if match.group() == "118.005":
                    self.assertIn(
                        "СИНТЕТИЧЕСКИЙ ПРИМЕР ПРОИЗНОШЕНИЯ — НЕ ЧАСТОТА ДЛЯ ПОЛЁТА",
                        context,
                    )
                    continue
                self.assertIn(match.group(), ("121.500", "121,500"))
                self.assertRegex(
                    context,
                    re.compile(
                        r"(?:emergency|аварийн|бедств|срочност|MAYDAY|PAN\s+PAN)",
                        re.IGNORECASE,
                    ),
                )
        for placeholder in ("[CALLSIGN]", "[AERODROME]", "[RUNWAY]", "[FREQUENCY]"):
            self.assertIn(placeholder, text)
        plain = _plain_markdown(text)
        self.assertRegex(plain, r"(?is)частот.{0,120}(?:динамич|изменя).{0,160}текущ.{0,80}AIP")
        self.assertRegex(plain, r"(?is)(?:AIP|NOTAM).{0,180}(?:местн|аэродромн).{0,140}перед\s+пол[её]т")
        self.assertRegex(plain, r"(?is)сохран[её]нн\w+\s+частот.{0,80}не.{0,30}(?:гарантир|доказыва|означа).{0,40}актуальн")

    def test_task7_has_thirty_substantive_unique_questions(self):
        blocks = []
        errors = []
        for relative_path in TASK7_CHAPTERS:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            chapter = parsed_question_blocks(text)
            self.assertEqual(5, len(chapter), relative_path)
            blocks.extend(chapter)
            errors.extend(f"{relative_path}: {error}" for error in question_block_errors(text))
        self.assertEqual(30, len(blocks))
        self.assertEqual(30, len({block["id"] for block in blocks}))
        self.assertEqual(30, len({re.sub(r"\W+", " ", _plain_markdown(block["prompt"]).casefold()).strip() for block in blocks}))
        self.assertEqual([], errors)

    def test_task7_sources_are_registered_with_exact_pinpoints(self):
        sources = {item["id"]: item for item in json.loads(SOURCE_REGISTRY.read_text())}
        required = {
            "SRC-BOE-RD-1180-2018", "SRC-BOE-FOM-1146-2019",
            "SRC-AESA-ULM-RTC-PROGRAM", "SRC-ENAIRE-AIP-GEN-3-4-2026",
            "SRC-ENAIRE-AIP-ENR-1-4-2026", "SRC-EASA-SERA-2025",
            "SRC-EASA-AIRCREW-2026", "SRC-BOE-RD-765-2022",
        }
        self.assertTrue(required.issubset(sources), required - sources.keys())
        combined = " ".join(
            f"{sources[source]['edition']} {sources[source]['scope']}" for source in required
        )
        for pinpoint in (
            "SERA.14015", "SERA.8015(e)", "SERA.14083", "SERA.13001",
            "FCL.055", "arts. 12–13", "art. 4.1(d)", "GEN 3.4", "ENR 1.4-5",
            "20 h", "10 h", "1 h",
        ):
            self.assertIn(pinpoint, combined)
        chapter_text = self._all_text()
        for source in required:
            self.assertIn(source, chapter_text)

    def test_task7_blank_cards_are_training_aids_not_cockpit_checklists(self):
        text = (ROOT / TASK7_REFERENCE).read_text(encoding="utf-8")
        self.assertEqual([], explicit_atx_heading_errors(text))
        for anchor in ("scenario-index", "english-card", "spanish-card", "emergency-card"):
            self.assertIn(anchor, markdown_anchors(text))
        self.assertGreaterEqual(text.count("________________"), 12)
        self.assertRegex(text, r"(?is)не.{0,60}(?:cockpit|кабинн|бортов).{0,80}чек-лист")
        self.assertRegex(text, r"(?is)не.{0,40}заменя.{0,80}(?:AFM|POH).{0,100}местн")
        for number in range(1, 21):
            self.assertIn(f"RTC-{number:02d}", text)

    def test_task7_terms_and_ru_first_explanations_are_registered(self):
        terms = {item["canonical"]: item for item in json.loads(TERMS_REGISTRY.read_text())}
        required = {
            "radiotelephony (R/T)", "air traffic control (ATC)",
            "aerodrome flight information service (AFIS)", "air-to-air (A/A)",
            "readback", "acknowledgement", "callsign", "plain language",
            "listening watch", "distress", "urgency", "communication failure",
            "secondary surveillance radar (SSR)", "language proficiency endorsement",
        }
        self.assertTrue(required.issubset(terms), required - terms.keys())
        glossary = GLOSSARY.read_text(encoding="utf-8")
        for canonical in required:
            record = terms[canonical]
            self.assertIn(f'<a id="{record["anchor"]}"></a>', glossary)
            self.assertTrue(record["russian"].strip())
            self.assertTrue(record["english"].strip())
            self.assertTrue(record["spanish"].strip())

    def test_task7_svg_is_accessible_mobile_readable_and_semantic(self):
        root = ET.parse(ROOT / TASK7_SVG).getroot()
        ns = "{http://www.w3.org/2000/svg}"
        self.assertEqual(f"{ns}svg", root.tag)
        self.assertEqual("img", root.attrib.get("role"))
        self.assertTrue(root.attrib.get("aria-labelledby"))
        self.assertIsNotNone(root.find(f"{ns}title"))
        self.assertIsNotNone(root.find(f"{ns}desc"))
        self.assertFalse(list(root.iter(f"{ns}image")))
        vx, vy, vw, vh = (float(value) for value in root.attrib["viewBox"].split())
        self.assertLessEqual(vw, 700)
        sizes = [float(item.attrib["font-size"].removesuffix("px")) for item in root.iter(f"{ns}text") if "font-size" in item.attrib]
        self.assertTrue(sizes)
        self.assertGreaterEqual(min(sizes) * 340 / vw, 14.0)
        ids = {item.attrib.get("id"): item for item in root.iter() if item.attrib.get("id")}
        required = {
            "prepare", "listen", "call", "classify", "clearance", "information",
            "intention", "readback", "acknowledgement", "uncertainty",
            "stop-before-action", "correct", "act-monitor", "return-path",
        }
        self.assertTrue(required.issubset(ids), required - ids.keys())
        for item in root.iter():
            bbox = element_bbox(item)
            if bbox is None:
                continue
            x, y, width, height = bbox
            self.assertGreaterEqual(x, vx)
            self.assertGreaterEqual(y, vy)
            self.assertLessEqual(x + width, vx + vw)
            self.assertLessEqual(y + height, vy + vh)
        self.assertGreaterEqual(sum(1 for item in root.iter() if item.attrib.get("marker-end", "").startswith("url(#")), 10)
        words = " ".join(root.itertext()).casefold()
        for phrase in ("разрешение", "информация", "намерение", "say again", "не выполнять"):
            self.assertIn(phrase, words)

    def test_task7_svg_return_path_has_a_clear_gutter_and_acknowledgement_fits(self):
        root = ET.parse(ROOT / TASK7_SVG).getroot()
        ns = "{http://www.w3.org/2000/svg}"
        _, _, vw, _ = (float(value) for value in root.attrib["viewBox"].split())
        ids = {item.attrib.get("id"): item for item in root.iter() if item.attrib.get("id")}

        right_edge = max(
            element_bbox(ids[group_id].find(f"{ns}rect"))[0]
            + element_bbox(ids[group_id].find(f"{ns}rect"))[2]
            for group_id in ("intention", "intention-check", "act-monitor")
        )
        path_numbers = [
            float(value)
            for value in re.findall(
                r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
                ids["return-path"].attrib["d"],
            )
        ]
        path_points = list(zip(path_numbers[0::2], path_numbers[1::2]))
        vertical_gutters = [
            first[0]
            for first, second in zip(path_points, path_points[1:])
            if first[0] == second[0] and abs(first[1] - second[1]) > 200
        ]
        self.assertTrue(vertical_gutters)
        self.assertGreaterEqual(max(vertical_gutters) - right_edge, 10)

        acknowledgement_text = ids["acknowledgement"].find(f"{ns}text")
        acknowledgement_spans = list(acknowledgement_text.iter(f"{ns}tspan"))
        self.assertEqual("ПОДТВЕРДИТЬ", "".join(acknowledgement_spans[0].itertext()))
        font_size = float(acknowledgement_text.attrib["font-size"])
        self.assertGreaterEqual(font_size * 340 / vw, 14.0)
        rect_x, _, rect_width, _ = element_bbox(
            ids["acknowledgement"].find(f"{ns}rect")
        )
        heading_width = len("ПОДТВЕРДИТЬ") * font_size * 0.56
        heading_left = float(acknowledgement_spans[0].attrib["x"]) - heading_width / 2
        self.assertGreaterEqual(heading_left, rect_x + 4)
        self.assertLessEqual(heading_left + heading_width, rect_x + rect_width - 4)


class Task8NavigationTests(unittest.TestCase):
    REQUIRED_SOURCE_IDS = {
        "SRC-AESA-ULM-LEARNING-OBJECTIVES-GU09-ED01",
        "SRC-EASA-AIRCREW-2026",
        "SRC-ENAIRE-AIP-ESPANA",
        "SRC-ENAIRE-AIP-NAVIGATION-2026",
        "SRC-ENAIRE-VFR500-2026",
        "SRC-EASA-SERA-2025",
        "SRC-EASA-AIR-OPS-2026",
        "SRC-FAA-PHAK-25C-CH16",
        "SRC-NZ-CAA-VISUAL-NAV-V1",
        "SRC-EASA-SIB-2022-02R4",
        "SRC-EGNOS-SOL-SDD-3-6",
        "SRC-BOE-RD-765-2022",
    }

    def _read(self, relative_path):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), relative_path)
        return path.read_text(encoding="utf-8")

    def _xml(self, relative_path):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), relative_path)
        return ET.parse(path).getroot()

    def _all_text(self):
        return "\n".join(self._read(path) for path in TASK8_CHAPTERS)

    def _calculation_blocks(self):
        text = self._all_text()
        matches = list(
            re.finditer(
                r"(?m)^###\s+(CALC-NAV-(\d{2}))\s+—[^\n]*\{#calc-nav-\2\}\s*$",
                text,
            )
        )
        blocks = {}
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            next_h2 = re.search(r"(?m)^##\s+", text[match.end():end])
            if next_h2:
                end = match.end() + next_h2.start()
            blocks[match.group(1)] = text[match.start():end]
        return blocks

    def test_task8_files_exist_and_are_in_navigation(self):
        nav_paths = mkdocs_nav_paths((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        for relative_path in (*TASK8_CHAPTERS, TASK8_REFERENCE):
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
                self.assertIn(relative_path.removeprefix("docs/"), nav_paths)
        for relative_path in TASK8_SVGS:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_task8_template_scope_and_stable_anchors(self):
        required = {
            "purpose", "outcomes", "applicability", "theory", "ulm-application",
            "part-fcl-extension", "safety", "common-errors", "summary",
            "review-questions", "sources",
        }
        for relative_path in TASK8_CHAPTERS:
            text = self._read(relative_path)
            with self.subTest(path=relative_path):
                self.assertEqual([], explicit_atx_heading_errors(text))
                self.assertTrue(required.issubset(markdown_anchors(text)))
                for label in APPLICABILITY_LABELS:
                    self.assertIn(label, applicability_table_labels(text))
                plain = _plain_markdown(text)
                self.assertRegex(plain, r"(?is)ULM.{0,180}Испани")
                self.assertRegex(plain, r"(?is)(?:LAPL|PPL).{0,220}(?:позже|переход|Part-FCL)")

    def test_task8_required_topic_anchors(self):
        anchors = markdown_anchors(self._all_text())
        required = {
            "latitude-longitude", "utc-local-date", "true-magnetic-compass",
            "chart-scale", "vfr500-workflow", "aip-sup-aic-notam-airac",
            "airspace-volume", "wind-convention", "wind-triangle", "wca-sign",
            "time-distance-speed", "eta-updates", "flight-log-workflow",
            "vor-radial-bearing", "dme-slant-range", "adf-ndb-limitations",
            "gnss-position-integrity", "database-currency", "jamming-spoofing",
            "raim-sbas-egnos", "lost-priorities", "one-in-sixty", "diversion",
            "international-boundary",
        }
        self.assertTrue(required.issubset(anchors), required - anchors)

    def test_gu09_navigation_scope_and_current_ulm_day_night_gate_are_complete(self):
        text = _plain_markdown(self._all_text())
        anchors = markdown_anchors(self._all_text())
        required_anchors = {
            "civil-twilight", "distance-units", "terrestrial-magnetism",
            "route-projections", "pilotage-map-orientation", "top-of-descent",
        }
        self.assertTrue(required_anchors.issubset(anchors), required_anchors - anchors)

        for pattern in (
            r"(?is)гражданск\w+\s+сумерк.{0,220}(?:6|шест)\s*(?:°|градус).{0,160}горизонт",
            r"(?is)начал\w+\s+утренн\w+\s+гражданск\w+\s+сумер.{0,220}конц\w+\s+вечерн\w+\s+гражданск\w+\s+сумер",
            r"(?is)RD\s*765/2022.{0,160}(?:art\.|стать).?\s*4\.1\(e\).{0,220}01\.04\.2026.{0,220}дневн\w+.{0,80}VFR.{0,80}VMC",
            r"(?is)ULM.{0,80}MAF.{0,160}(?:сам[аио]|без).{0,100}не.{0,80}(?:достаточ|разреш)",
            r"(?is)сухопутн\w+\s+миля.{0,100}1[,.]609344\s*(?:km|километр)",
            r"(?is)морск\w+\s+миля.{0,100}1[,.]852\s*(?:km|километр)",
            r"(?is)1\s*NM.{0,80}1[,.]15078\s*SM",
            r"(?is)магнитн\w+\s+пол.{0,180}(?:географическ|истинн).{0,180}магнитн\w+\s+полюс",
            r"(?is)изогон.{0,180}(?:годов|ежегодн).{0,100}(?:измен|вариац)",
            r"(?is)цилиндрическ\w+\s+проекц.{0,240}(?:Ламберт|коническ)",
            r"(?is)ортодром.{0,180}локсодром.{0,180}(?:постоянн\w+\s+курс|румб)",
            r"(?is)ориентир\w+\s+карт.{0,180}(?:местност|рельеф|линейн).{0,180}(?:двум|независим|подтверж)",
            r"(?is)(?:точк|начал).{0,80}снижен.{0,180}(?:разност|потер).{0,100}высот.{0,160}(?:вертикальн|скорост).{0,100}(?:GS|путев)",
        ):
            with self.subTest(pattern=pattern):
                self.assertRegex(text, re.compile(pattern))

        sunrise_boundary_pattern = re.compile(
            r"(?is)(?:фактическ\w+\s+)?(?:восход|заход)"
            r"(?:(?![.!?]).){0,220}не(?:(?![.!?]).){0,80}совпад"
            r"(?:(?![.!?]).){0,100}правов\w+\s+границ"
        )
        earth = _plain_markdown(self._read(TASK8_CHAPTERS[0]))
        self.assertRegex(earth, sunrise_boundary_pattern)
        self.assertIsNone(
            sunrise_boundary_pattern.search(
                "Фактический восход не совпадает с заходом."
            )
        )

        night_gate_patterns = (
            re.compile(r"(?is)до\s+начала\s+утренн\w+\s+гражданск\w+\s+сумер"),
            re.compile(r"(?is)после\s+конца\s+вечерн\w+\s+гражданск\w+\s+сумер"),
            re.compile(
                r"(?is)(?:оборудован|оснащен).{0,260}"
                r"(?:эквивалентн\w+\s+лиценз|Part-FCL).{0,220}"
                r"ночн\w+\s+(?:полномоч|прав)"
            ),
        )

        def has_complete_night_gate(value):
            return all(pattern.search(value) for pattern in night_gate_patterns)

        self.assertTrue(has_complete_night_gate(earth))
        for mutation in (
            "Фактический восход не совпадает с заходом; самолёт оборудован, "
            "есть Part-FCL с ночными полномочиями.",
            "До начала вечерних гражданских сумерек самолёт оборудован; "
            "Part-FCL с ночными полномочиями достаточно.",
        ):
            with self.subTest(mutation=mutation):
                self.assertFalse(has_complete_night_gate(mutation))

    def test_gu09_coordinate_formats_time_zones_and_vfr_symbol_families_are_complete(self):
        earth = _plain_markdown(self._read(TASK8_CHAPTERS[0]))
        for pattern in (
            r"(?is)(?:градус.+минут.+секунд|DMS).{0,180}(?:градус.+десятичн\w+\s+минут|DDM).{0,180}(?:десятичн\w+\s+градус|DD)",
            r"(?is)(?:северн|N).{0,100}(?:восточн|E).{0,100}положительн",
            r"(?is)(?:южн|S).{0,100}(?:западн|W).{0,100}отрицательн",
            r"(?is)360\s*°?.{0,80}24.{0,80}15\s*°.{0,120}(?:часов\w+\s+пояс|долгот)",
            r"(?is)(?:восток|восточн).{0,100}(?:позже|прибав).{0,140}(?:запад|западн).{0,100}(?:раньше|вычит)",
        ):
            with self.subTest(pattern=pattern):
                self.assertRegex(earth, re.compile(pattern))
        self.assertRegex(
            earth,
            re.compile(r"(?is)Δt\s*=\s*Δλ\s*/\s*15\s*°?.{0,100}(?:h|час)"),
        )

        charts = _plain_markdown(self._read(TASK8_CHAPTERS[1]))
        for pattern in (
            r"(?is)(?:ICAO|OACI).{0,100}(?:условн\w+\s+знак|символ)",
            r"(?is)аэродром",
            r"(?is)препятств",
            r"(?is)(?:P/R/D|запретн\w+.{0,40}ограниченн\w+.{0,40}опасн)",
            r"(?is)(?:ЛЭП|лини[яи]\s+электропередач)",
            r"(?is)инфраструктур",
            r"(?is)(?:наземн\w+\s+ориентир|географическ\w+\s+объект)",
        ):
            with self.subTest(pattern=pattern):
                self.assertRegex(charts, re.compile(pattern))

        svg_path = ROOT / TASK8_SVGS[3]
        self.assertTrue(svg_path.is_file(), TASK8_SVGS[3])
        self.assertIn(
            "../assets/diagrams/chart-symbols-gen23.svg",
            self._read(TASK8_CHAPTERS[1]),
        )
        self.assertIn(
            "https://aip.enaire.es/AIP/contenido_AIP/GEN/LE_GEN_2_3_es.html",
            self._read(TASK8_CHAPTERS[1]),
        )
        symbols = ET.fromstring(svg_path.read_text(encoding="utf-8"))
        ns = "{http://www.w3.org/2000/svg}"
        self.assertFalse(list(symbols.iter(f"{ns}image")))
        by_id = {
            node.attrib["id"]: node
            for node in symbols.iter()
            if node.attrib.get("id")
        }
        required_geometry = {
            "symbol-civil-aerodrome": {"circle", "line"},
            "symbol-obstacle-group": {"polyline", "circle"},
            "symbol-prd-zone": {"rect", "path"},
            "symbol-powerline": {"line", "polyline"},
            "symbol-motorway": {"line"},
            "symbol-railway": {"line", "rect"},
            "symbol-landmark": {"path", "rect"},
        }
        for identifier, required_tags in required_geometry.items():
            with self.subTest(symbol=identifier):
                self.assertIn(identifier, by_id)
                actual_tags = {
                    node.tag.removeprefix(ns) for node in by_id[identifier].iter()
                }
                self.assertTrue(required_tags.issubset(actual_tags), required_tags - actual_tags)

    def test_reviewed_wind_and_eta_calculations_expose_all_assumptions(self):
        wind = self._calculation_blocks()["CALC-NAV-22"]
        for value in ("WCA = −12°", "TH = 078°", "GS = 98 kt"):
            self.assertIn(value, wind)

        eta = self._calculation_blocks()["CALC-NAV-24"]
        eta_plain = _plain_markdown(eta)
        for value in ("исходная ETA", "09:40 UTC", "09:44 UTC"):
            self.assertIn(value, eta_plain)
        self.assertRegex(eta_plain, r"(?is)(?:допущен|предполож).{0,120}(?:GS|скорост)")

    def test_task8_dynamic_operational_warning_is_on_every_chapter(self):
        for relative_path in TASK8_CHAPTERS:
            text = self._read(relative_path)
            with self.subTest(path=relative_path):
                self.assertRegex(
                    _plain_markdown(text),
                    r"Проверено 13\.07\.2026; перед полётом проверить "
                    r"AIP/SUP/AIC/NOTAM и текущ(?:ий|ее).{0,240}\bAIRAC\b",
                )
                self.assertIn(
                    "../reference/glossary.md#term-aeronautical-information-regulation-control-airac",
                    text,
                )
        charts = self._read(TASK8_CHAPTERS[1])
        plain = _plain_markdown(charts)
        self.assertRegex(plain, r"(?is)AIRAC\s+07/26.{0,120}(?:будущ|не.{0,40}действ).{0,120}06\.08\.2026")
        self.assertRegex(plain, r"(?is)footer|нижн\w+\s+колонтитул.{0,100}не.{0,50}(?:дат|редакц).{0,80}(?:всего|цел).{0,50}AIP")

    def test_vfr500_snapshot_is_heterogeneous_and_has_correction_workflow(self):
        text = _plain_markdown(self._read(TASK8_CHAPTERS[1]))
        for value in (
            "GC 2025", "20.03.2025", "LE1 2025", "02.10.2025",
            "LE2 2025", "LE3–LE6 2026", "19.03.2026", "VFR500 Changes",
            "28.05.2026", "InsigniaVFR", "VIGOR",
        ):
            self.assertIn(value, text)
        self.assertRegex(text, r"(?is)семь\s+лист.{0,180}не.{0,60}(?:един|одн).{0,80}2026")
        for product in ("AIP", "SUP", "AIC", "NOTAM", "AIRAC"):
            self.assertIn(product, text)

    def test_task8_has_twenty_recomputable_structured_calculations(self):
        blocks = self._calculation_blocks()
        self.assertGreaterEqual(len(blocks), 20)
        self.assertEqual(len(blocks), len(set(blocks)))
        for identifier, block in blocks.items():
            with self.subTest(calculation=identifier):
                for label in ("Дано", "Формула", "Расчёт", "Результат", "Решение пилота"):
                    self.assertRegex(block, rf"(?m)^\*\*{re.escape(label)}:\*\*")
                self.assertRegex(block, r"(?:NM|km|kt|km/h|h|min|L|L/h|°|ft)")

        expected = {
            "CALC-NAV-01": 18.0,
            "CALC-NAV-02": 22.5,
            "CALC-NAV-03": 22.0,
            "CALC-NAV-04": 84.0,
            "CALC-NAV-05": 120.0,
            "CALC-NAV-06": 27.0,
            "CALC-NAV-07": 96.0,
            "CALC-NAV-08": 30.0,
            "CALC-NAV-09": 24.0,
            "CALC-NAV-10": 38.0,
            "CALC-NAV-11": 7.2,
            "CALC-NAV-12": 10.0,
            "CALC-NAV-13": 88.0,
            "CALC-NAV-14": 90.0,
            "CALC-NAV-15": 84.0,
            "CALC-NAV-16": 4.0,
            "CALC-NAV-17": 12.0,
            "CALC-NAV-18": 8.0,
            "CALC-NAV-19": 9.0,
            "CALC-NAV-20": 2.0,
            "CALC-NAV-21": 12.0,
        }
        self.assertTrue(expected.keys() <= blocks.keys())
        for identifier, value in expected.items():
            self.assertIn(f"<!-- recompute-result: {value:.1f} -->", blocks[identifier])

        recomputed = {
            "CALC-NAV-01": 3.6 * 500_000 / 100_000,
            "CALC-NAV-02": 15 / 40 * 60,
            "CALC-NAV-03": 44 / 2,
            "CALC-NAV-04": 42 / 0.5,
            "CALC-NAV-05": 60 * 2,
            "CALC-NAV-06": 90 * 0.3,
            "CALC-NAV-07": 24 / 0.25,
            "CALC-NAV-08": 60 * 0.5,
            "CALC-NAV-09": 12 * 2,
            "CALC-NAV-10": 19 / 0.5,
            "CALC-NAV-11": 18 * 0.4,
            "CALC-NAV-12": 20 / 2,
            "CALC-NAV-13": 92 - 4,
            "CALC-NAV-14": 88 + 2,
            "CALC-NAV-15": 90 - 6,
            "CALC-NAV-16": 4 / 60 * 60,
            "CALC-NAV-17": 4 + 8,
            "CALC-NAV-18": 16 / 2,
            "CALC-NAV-19": 18 * 0.5,
            "CALC-NAV-20": 60 * 2 / 60,
            "CALC-NAV-21": (13**2 - 5**2) ** 0.5,
        }
        for identifier, value in recomputed.items():
            self.assertAlmostEqual(expected[identifier], value, places=1)

    def test_wind_calculations_define_sign_and_independent_plausibility(self):
        text = _plain_markdown(self._read(TASK8_CHAPTERS[2]))
        self.assertRegex(text, r"(?is)ветер.{0,80}(?:откуда|приходит).{0,80}не.{0,40}(?:куда|ид[её]т)")
        self.assertRegex(text, r"(?is)WCA.{0,140}(?:положительн|\+).{0,100}(?:вправо|прав)")
        self.assertRegex(text, r"(?is)WCA.{0,140}(?:отрицательн|−|-).{0,100}(?:влево|лев)")
        self.assertRegex(text, r"(?is)(?:независим|груб\w+).{0,80}(?:проверк|оценк).{0,160}(?:GS|путев\w+\s+скорост)")

    def test_complete_synthetic_log_has_all_fields_and_post_leg_update(self):
        text = self._read(TASK8_REFERENCE)
        self.assertIn("СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ НАВИГАЦИОННЫЙ ЛОГ (FLIGHT LOG) — НЕ ДЛЯ НАВИГАЦИИ", text)
        for field in (
            "Дата источников", "Маршрут", "Контрольные точки", "Рельеф",
            "Воздушное пространство", "Погода", "TC", "W", "V", "MC",
            "DEV", "CH", "Дистанция", "TAS", "WCA", "GS", "Время участка",
            "ETA", "Топливо", "[FREQUENCY]", "Запасной аэродром",
            "Триггер ухода", "Пересчёт после участка",
        ):
            self.assertIn(field, text)
        self.assertGreaterEqual(text.count("________________"), 20)
        self.assertRegex(text, r"(?is)не.{0,50}(?:операционн|реальн).{0,40}план")

    def test_synthetic_log_arithmetic_decision_gate_and_ru_first_labels(self):
        text = self._read(TASK8_REFERENCE)
        rows = {}
        for line in text.splitlines():
            match = re.match(r"^\|\s*([123])\s*\|", line)
            if match and "________________" not in line:
                rows[match.group(1)] = [cell.strip() for cell in line.strip().strip("|").split("|")]
        self.assertEqual({"1", "2", "3"}, rows.keys())

        # Columns: leg, route, TC, wind, variation, MC, TH, MH, deviation, CH,
        # distance, TAS, WCA, GS, leg time, ETA, fuel, references, trigger.
        expected = {
            "1": (-7.7, 89.2, 12.1, 3.6),
            "2": (-5.4, 98.1, 14.7, 4.4),
            "3": (3.2, 100.7, 17.9, 5.4),
        }
        for leg, (wca, gs, minutes, fuel) in expected.items():
            cells = rows[leg]
            numbers = lambda index: float(re.search(r"[−+-]?\d+(?:[.,]\d+)?", cells[index]).group().replace("−", "-").replace(",", "."))
            self.assertAlmostEqual(wca, numbers(12), places=1)
            self.assertAlmostEqual(gs, numbers(13), places=1)
            self.assertAlmostEqual(minutes, numbers(14), places=1)
            self.assertAlmostEqual(fuel, numbers(16), places=1)
            self.assertAlmostEqual(numbers(10) / numbers(13) * 60, numbers(14), delta=0.1)
            self.assertAlmostEqual(numbers(14) / 60 * 18, numbers(16), delta=0.1)

        self.assertIn("`3,6 + 4,4 + 5,4 = 13,4 L`", text)
        self.assertIn("CP1 опознана в 09:16 UTC", _plain_markdown(text))
        self.assertNotIn("CP1 time `09:19 UTC`", text)
        for label in ("Участок", "Маршрут/контрольная точка", "Ветер", "Истинный курс носа", "Магнитный курс носа", "Источники/условия"):
            self.assertIn(label, text)

    def test_flight_log_has_magnetic_course_in_both_tables_and_recomputes_it(self):
        text = self._read(TASK8_REFERENCE)
        table_headers = [
            line for line in text.splitlines()
            if line.startswith("| Участок | Маршрут/контрольная точка |")
        ]
        self.assertEqual(2, len(table_headers))
        for header in table_headers:
            self.assertRegex(header, r"\|\s*(?:Магнитная заданная линия пути\s+)?MC\s*\|")

        rows = {}
        for line in text.splitlines():
            match = re.match(r"^\|\s*([123])\s*\|", line)
            if match and "________________" not in line:
                rows[match.group(1)] = [
                    cell.strip() for cell in line.strip().strip("|").split("|")
                ]
        for leg, cells in rows.items():
            def degrees(index):
                return float(
                    re.search(r"\d+(?:[.,]\d+)?", cells[index])
                    .group()
                    .replace(",", ".")
                )

            tc = degrees(2)
            variation = degrees(4)
            if "W" in cells[4].upper():
                variation *= -1
            self.assertRegex(cells[4], r"(?i)[EW]")
            mc = degrees(5)
            self.assertAlmostEqual((tc - variation) % 360, mc, places=1, msg=leg)

    def test_coordinate_and_utc_conversions_are_structured_calculations(self):
        text = self._read(TASK8_CHAPTERS[0])
        for identifier, required in {
            "CALC-NAV-26": ("41° 24,5′ N", "41,4083° N", "recompute-result: 41.4083"),
            "CALC-NAV-27": ("23:35 UTC", "01:35", "13 июля", "recompute-result: 95.0"),
        }.items():
            match = re.search(
                rf"(?ms)^###\s+{identifier}\s+—.*?(?=^###\s+CALC-NAV-|^##\s+)",
                text,
            )
            self.assertIsNotNone(match, identifier)
            for value in required:
                self.assertIn(value, match.group(0))

    def test_vor_diagram_separates_azimuth_and_elevation_projections(self):
        root = ET.fromstring((ROOT / TASK8_SVGS[1]).read_text(encoding="utf-8"))
        ids = {node.attrib.get("id") for node in root.iter()}
        self.assertIn("vor-plan-view", ids)
        self.assertIn("dme-elevation-view", ids)
        description = " ".join("".join(root.itertext()).split()).casefold()
        self.assertIn("вид сверху", description)
        self.assertIn("вид сбоку", description)

    def test_gnss_question_distractors_are_plausible_novice_errors(self):
        text = self._read(TASK8_CHAPTERS[5])
        for absurd in (
            "Jamming всегда улучшает точность",
            "пилот включил Wi-Fi",
            "Два одинаковых снимка экрана",
            "имя пассажира",
        ):
            self.assertNotIn(absurd, text)

    def test_task8_boundaries_and_myth_refutations_are_explicit(self):
        text = _plain_markdown(self._all_text())
        required_patterns = (
            r"истинн\w+.{0,30}магнитн\w+.{0,100}не.{0,30}смеш",
            r"курс.{0,80}не.{0,30}(?:равен|совпад).{0,40}(?:лини[яеи] пути|track)",
            r"moving map.{0,100}не.{0,30}(?:разреша|авториз|созда).{0,60}(?:вход|простран)",
            r"стар\w+.{0,30}печатн\w+\s+карт.{0,120}не.{0,30}(?:оста[её]тся|гарантир).{0,40}актуальн",
            r"GNSS.{0,50}позиц.{0,80}не.{0,30}(?:означа|доказыва).{0,40}целостност",
            r"планшет.{0,120}не.{0,40}(?:автоматич|обязательно).{0,80}(?:RAIM|SoL)",
            r"радиал.{0,80}(?:FROM|от).{0,80}не.{0,30}(?:к|TO).{0,30}станци",
            r"DME.{0,80}не.{0,30}(?:всегда|обязательно).{0,60}горизонт",
            r"1-in-60.{0,100}не.{0,30}точн.{0,50}(?:кажд|люб).{0,30}угл",
            r"ETA.{0,80}(?:обнов|пересчит)",
            r"одн\w+.{0,30}(?:GNSS|радионавигац).{0,120}(?:недостат|перекр[её]стн|cross-check)",
        )
        for pattern in required_patterns:
            self.assertRegex(text, re.compile(pattern, re.IGNORECASE | re.DOTALL))

        border = self._read(TASK8_CHAPTERS[6])
        plain_border = _plain_markdown(border)
        self.assertRegex(plain_border, r"(?is)RD\s+765/2022.{0,100}(?:стать|art\.).?\s*4\.2")
        self.assertRegex(plain_border, r"(?is)закон.{0,80}(?:государств|стран).{0,80}(?:прол[её]т|overflown)")
        self.assertRegex(plain_border, r"(?is)(?:LAPL|PPL).{0,140}не.{0,50}(?:превраща|дела).{0,80}Part-21")
        self.assertRegex(plain_border, r"(?is)flight plan|план\s+пол[её]та.{0,120}не.{0,50}(?:разреша|авториз).{0,80}иностран")
        self.assertRegex(plain_border, r"(?is)(?:маршрут|сценари).{0,120}(?:только|внутри).{0,40}Испани")
        self.assertRegex(plain_border, r"(?is)Part-NCO.{0,160}(?:операци|воздушн\w+\s+судн).{0,160}не.{0,40}(?:лиценз|налич)")

    def test_part_fcl_radio_navigation_is_separate_and_current_details_are_dynamic(self):
        chapter = self._read(TASK8_CHAPTERS[4])
        self.assertIn("[PART-FCL — ОБЩЕЕ]", chapter)
        plain = _plain_markdown(chapter)
        self.assertRegex(plain, r"(?is)GU09.{0,140}(?:GPS|GNSS).{0,160}не.{0,80}(?:подробн|детальн).{0,80}(?:VOR|DME|ADF)")
        self.assertRegex(plain, r"(?is)LAPL\(A\).{0,120}(?:PPL|общ).{0,80}(?:теоретическ|syllabus)")
        self.assertRegex(plain, r"(?is)(?:частот|идентификатор).{0,120}(?:ENR\s+4\.1|AD\s+2).{0,120}(?:перед|текущ)")
        self.assertNotRegex(chapter, r"\b(?:10[89]|11\d|12[0-35])[.,]\d{3}\b")

    def test_common_part_fcl_navigation_is_labelled_lapl_and_ppl_without_fake_delta(self):
        for relative_path in TASK8_CHAPTERS:
            text = _plain_markdown(self._read(relative_path))
            with self.subTest(path=relative_path):
                self.assertRegex(text, r"(?is)PART-FCL\s+—\s+ОБЩЕЕ.{0,280}LAPL.{0,100}PPL")
                self.assertNotRegex(
                    text,
                    r"(?is)PPL\s+—\s+РАСШИРЕНИЕ.{0,180}(?:добавля|более\s+сложн|более\s+полн|углуб).{0,120}(?:теори|задач|модел|радионавигац)",
                )

        text = _plain_markdown(self._all_text())
        self.assertRegex(text, r"(?is)LAPL.{0,100}PPL.{0,160}(?:одинаков|общ).{0,160}(?:программ|syllabus)")
        self.assertRegex(text, r"(?is)Part-NCO.{0,180}(?:операци|воздушн\w+\s+судн).{0,180}не.{0,60}(?:лиценз|налич)")

    def test_gnss_safety_scope_and_current_sib_are_taught(self):
        text = _plain_markdown(self._read(TASK8_CHAPTERS[5]))
        for value in ("jamming", "spoofing", "03.07.2026", "2022-02R4", "RAIM", "SBAS", "EGNOS"):
            self.assertIn(value.casefold(), text.casefold())
        self.assertRegex(text, r"(?is)SIB.{0,120}(?:рекоменд|advisory).{0,120}не.{0,40}(?:обязательн|универсальн)")
        self.assertRegex(text, r"(?is)(?:сертифицирован|подходящ).{0,100}(?:при[её]мник|оборудован).{0,120}(?:RAIM|EGNOS)")
        self.assertRegex(text, r"(?is)(?:потребительск|обычн).{0,50}(?:планшет|EFB).{0,100}не.{0,50}(?:припис|счита).{0,60}(?:RAIM|SoL)")

    def test_task8_has_thirty_five_substantive_unique_questions(self):
        blocks = []
        errors = []
        for relative_path in TASK8_CHAPTERS:
            text = self._read(relative_path)
            chapter = parsed_question_blocks(text)
            self.assertEqual(5, len(chapter), relative_path)
            blocks.extend(chapter)
            errors.extend(f"{relative_path}: {error}" for error in question_block_errors(text))
        self.assertEqual(35, len(blocks))
        self.assertEqual(35, len({block["id"] for block in blocks}))
        self.assertEqual(35, len({re.sub(r"\W+", " ", _plain_markdown(block["prompt"]).casefold()).strip() for block in blocks}))
        self.assertEqual([], errors)

    def test_task8_sources_are_registered_audited_and_pinpointed(self):
        sources = {item["id"]: item for item in json.loads(SOURCE_REGISTRY.read_text())}
        self.assertTrue(self.REQUIRED_SOURCE_IDS.issubset(sources), self.REQUIRED_SOURCE_IDS - sources.keys())
        combined = " ".join(
            f"{sources[source]['edition']} {sources[source]['scope']}" for source in self.REQUIRED_SOURCE_IDS
        )
        for pinpoint in (
            "Navegación, pp. 28–32", "§§9.1–9.2", "GEN 3.1", "GEN 3.2",
            "GEN 2.3", "ENR 2.1", "ENR 5.5", "ENR 6", "ENR 4.1",
            "ENR 1.10", "28.05.2026", "SERA.2010(b)", "SERA.4001",
            "NCO.GEN.135", "NCO.OP.135", "16-2–16-8", "16-11–16-18",
            "pp. 4–10", "pp. 18–22", "pp. 27–28", "03.07.2026",
            "Appendix B", "p. 60", "art. 4.2",
        ):
            self.assertIn(pinpoint, combined)
        audit = (ROOT / "docs/sources/audit-technical.md").read_text(encoding="utf-8")
        chapter_text = self._all_text()
        for source in self.REQUIRED_SOURCE_IDS:
            self.assertIn(sources[source]["url"], audit)
            self.assertIn(source, chapter_text)

    def test_task8_terms_are_registered_with_ru_en_es_definitions(self):
        terms = {item["canonical"]: item for item in json.loads(TERMS_REGISTRY.read_text())}
        required = {
            "dead reckoning (DR)", "true course (TC)", "magnetic course (MC)",
            "compass heading (CH)", "wind correction angle (WCA)",
            "groundspeed (GS)", "estimated time of arrival (ETA)",
            "global navigation satellite system (GNSS)", "receiver autonomous integrity monitoring (RAIM)",
            "satellite-based augmentation system (SBAS)", "VHF omnidirectional range (VOR)",
            "distance measuring equipment (DME)", "automatic direction finder (ADF)",
            "true heading (TH)", "magnetic heading (MH)", "true airspeed (TAS)",
            "compass deviation (DEV)", "non-directional beacon (NDB)",
            "European Geostationary Navigation Overlay Service (EGNOS)",
            "Coordinated Universal Time (UTC)", "air traffic services (ATS)",
            "Aeronautical Information Regulation and Control (AIRAC)",
        }
        self.assertTrue(required.issubset(terms), required - terms.keys())
        for canonical in required:
            record = terms[canonical]
            for field in ("russian", "english", "spanish", "definition"):
                self.assertTrue(record[field].strip())

        self.assertEqual("derrota verdadera", terms["true course (TC)"]["spanish"])
        self.assertEqual("derrota magnética", terms["magnetic course (MC)"]["spanish"])
        self.assertEqual("FPL", terms["flight plan"]["abbreviation"])
        forbidden_definition_anglicisms = re.compile(
            r"(?i)\b(?:heading|magnetic variation|deviation|signed|progress|integrity information|radial|bearing)\b"
        )
        for canonical, record in terms.items():
            if canonical in required:
                with self.subTest(term=canonical):
                    self.assertIsNone(forbidden_definition_anglicisms.search(record["definition"]))

    def test_navigation_chapters_and_nav_labels_are_russian_first(self):
        chapter3 = self._read(TASK8_CHAPTERS[2])
        self.assertIn("угол поправки на ветер", chapter3.split("## Теория", 1)[0])
        self.assertIn("путевую скорость", chapter3.split("## Теория", 1)[0])

        chapter5 = self._read(TASK8_CHAPTERS[4])
        self.assertTrue(chapter5.startswith("# Радионавигация"))
        self.assertRegex(
            chapter5,
            r"(?is)ненаправленн\w+\s+радиомаяк.{0,160}English:\s*non-directional beacon,\s*NDB.{0,120}español:",
        )

        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("Счисление пути и навигационный лог", nav)
        self.assertIn("Потеря ориентировки и уход с маршрута", nav)
        self.assertNotIn("flight log:", nav)
        self.assertNotIn("diversion:", nav)

    def test_navigation_first_use_terms_and_alt_texts_are_russian_first(self):
        earth = self._read(TASK8_CHAPTERS[0])
        purpose = earth.split("## Результаты обучения", 1)[0]
        self.assertRegex(
            purpose,
            r"(?is)координированн\w+\s+всемирн\w+\s+врем.{0,100}English:\s*Coordinated Universal Time,\s*UTC.{0,100}español:",
        )

        log = self._read(TASK8_CHAPTERS[3])
        before_outcomes = log.split("## Результаты обучения", 1)[0]
        self.assertRegex(
            before_outcomes,
            r"(?is)расч[её]тн\w+\s+врем\w+\s+прибыт.{0,100}English:\s*estimated time of arrival,\s*ETA.{0,100}español:",
        )

        lost = self._read(TASK8_CHAPTERS[6])
        before_outcomes = lost.split("## Результаты обучения", 1)[0]
        for pattern in (
            r"(?is)обслуживан\w+\s+воздушн\w+\s+движен.{0,100}English:\s*air traffic services,\s*ATS.{0,100}español:",
            r"(?is)план\w*\s+пол[её]та.{0,100}English:\s*flight plan,\s*FPL.{0,100}español:",
        ):
            self.assertRegex(before_outcomes, pattern)

        for relative_path in TASK8_CHAPTERS:
            text = self._read(relative_path)
            for is_image, label, _ in markdown_references(text):
                if is_image:
                    first_letter = re.search(r"[A-Za-zА-Яа-яЁё]", label)
                    self.assertIsNotNone(first_letter, relative_path)
                    self.assertRegex(first_letter.group(), r"[А-Яа-яЁё]", relative_path)

    def test_navigation_abbreviations_follow_course_order_and_link_after_definition(self):
        combined = "\n".join(self._read(path) for path in TASK8_CHAPTERS)
        introductions = {
            "UTC": r"(?is)координированн\w+\s+всемирн\w+\s+врем.{0,100}English:\s*Coordinated Universal Time,\s*UTC.{0,100}español:\s*tiempo universal coordinado",
            "AIRAC": r"(?is)регламентирован\w+\s+и\s+контролирован\w+\s+аэронавигационн\w+\s+информац.{0,120}English:\s*Aeronautical Information Regulation and Control,\s*AIRAC.{0,120}español:\s*reglamentación y control de la información aeronáutica",
            "ATS": r"(?is)обслуживан\w+\s+воздушн\w+\s+движен.{0,100}English:\s*air traffic services,\s*ATS.{0,100}español:\s*servicios de tránsito aéreo",
            "ETA": r"(?is)расч[её]тн\w+\s+врем\w+\s+прибыт.{0,100}English:\s*estimated time of arrival,\s*ETA.{0,100}español:\s*hora estimada de llegada",
            "VOR": r"(?is)всенаправленн\w+\s+VHF-радиомаяк.{0,100}English:\s*VHF omnidirectional range,\s*VOR.{0,100}español:\s*radiofaro omnidireccional VHF",
            "FPL": r"(?is)план\w*\s+пол[её]та.{0,140}English:\s*(?:ATS\s+)?flight plan,\s*FPL.{0,120}español:\s*plan de vuelo(?:\s+ATS)?",
        }
        for abbreviation, pattern in introductions.items():
            match = re.search(pattern, combined)
            self.assertIsNotNone(match, abbreviation)
            first = re.search(rf"\b{re.escape(abbreviation)}\b", combined)
            self.assertIsNotNone(first, abbreviation)
            self.assertLessEqual(match.start(), first.start(), abbreviation)
            self.assertGreater(match.end(), first.start(), abbreviation)

        def mask(value):
            value = strip_code(value)
            value = re.sub(
                r"(?m)^\[[^]\n]+\]:[^\n]*(?:\n|$)",
                lambda item: _mask_non_newlines(item.group(0)),
                value,
            )
            return re.sub(
                r"!?\[[^]\n]+\](?:\[[^]\n]*\]|\([^\n)]*\))",
                lambda item: _mask_non_newlines(item.group(0)),
                value,
            )

        for relative_path in (*TASK8_CHAPTERS, TASK8_REFERENCE):
            unlinked = mask(self._read(relative_path))
            for abbreviation in introductions:
                matches = list(re.finditer(rf"\b{re.escape(abbreviation)}\b", unlinked))
                with self.subTest(path=relative_path, abbreviation=abbreviation):
                    self.assertEqual(
                        [],
                        [unlinked.count("\n", 0, item.start()) + 1 for item in matches],
                    )

    def test_navigation_distractors_stay_in_the_question_domain(self):
        blocks = {
            block["id"]: block
            for relative_path in TASK8_CHAPTERS
            for block in parsed_question_blocks(self._read(relative_path))
        }
        domain_patterns = {
            "Q-NAV-001": r"(?i)(?:координат|широт|долгот|градус|минут|полушари|[NSEW])",
            "Q-NAV-002": r"(?i)(?:UTC|местн\w+\s+врем|смещен|дат|час)",
            "Q-NAV-003": r"(?i)(?:магнитн\w+\s+склон|истинн|магнитн|[MT]\s*=)",
            "Q-NAV-004": r"(?i)(?:девиац|компас|магнитн\w+\s+склон|курс\w*\s+носа|карт)",
            "Q-NAV-005": r"(?i)(?:мнемоник|знак|истинн|магнитн|компасн|T/M/C|склон|девиац)",
            "Q-NAV-006": r"(?i)(?:масштаб|сантиметр|километр|морск\w+\s+мил|проекц|расстоя)",
            "Q-NAV-007": r"(?i)(?:AIRAC|дат|публик|вступлен|действ|VFR|IFR|NOTAM)",
            "Q-NAV-008": r"(?i)(?:колонтитул|страниц|AIP|редакц|поправ|NOTAM|AIRAC)",
            "Q-NAV-009": r"(?i)(?:пространств|границ|предел|класс|актив|высот|карт)",
            "Q-NAV-010": r"(?i)(?:VFR500|лист|редакц|дат|исправ|Changes|InsigniaVFR|AIS|AIP|NOTAM|карт)",
            "Q-NAV-011": r"(?i)(?:ветр|воздушн\w+\s+масс|север|юг|направлен|перенос)",
            "Q-NAV-012": r"(?i)(?:WCA|курс\w*\s+носа|лини[яи]\s+пути|GS|TAS|склон|девиац)",
            "Q-NAV-013": r"(?i)(?:ветр|снос|курс\w*\s+носа|лини[яи]\s+пути|WCA|TAS|GS|девиац)",
            "Q-NAV-014": r"(?i)(?:GS|TAS|встречн\w+\s+ветр|WCA|путев\w+\s+скорост)",
            "Q-NAV-015": r"(?i)(?:контрольн\w+\s+точк|GS|ETA|топлив|врем|навигационн\w+\s+лог)",
            "Q-NAV-016": r"(?i)(?:минут|час|узл|NM|врем|18|60|0[.,]3)",
            "Q-NAV-017": r"(?i)(?:контрольн\w+\s+точк|DR|лог|врем|решен|GNSS|визуальн)",
            "Q-NAV-018": r"(?i)(?:ETA|GS|задерж|врем|топлив|дистанц)",
            "Q-NAV-019": r"(?i)(?:топлив|резерв|AFM|POH|ULM|вместим|остат|расход)",
            "Q-NAV-020": r"(?i)(?:навигационн\w+\s+лог|ETA|GS|топлив|фактическ\w+\s+врем|положен)",
            "Q-NAV-021": r"(?i)(?:VOR|радиал|станц|пеленг|курс\w*\s+носа|NM)",
            "Q-NAV-022": r"(?i)(?:VOR|станц|идентификатор|флаг|статус|геометр|сигнал|стрелк)",
            "Q-NAV-023": r"(?i)(?:DME|наклонн\w+\s+дальност|горизонтальн\w+\s+расстоя|высот|станц)",
            "Q-NAV-024": r"(?i)(?:ADF|NDB|ноч|гроз|статик|берег|рельеф|пеленг|помех|VOR)",
            "Q-NAV-025": r"(?i)(?:VOR|DME|ENR|AD\s*2|NOTAM|станц|частот|идентификатор|статус)",
            "Q-NAV-026": r"(?i)(?:GNSS|позици|целостност|баз|spoofing|EGNOS|SoL|символ|предупрежден)",
            "Q-NAV-027": r"(?i)(?:GNSS|маршрут|баз|точк|лини[яи]\s+пути|расстоя|AIS|карт|участок)",
            "Q-NAV-028": r"(?i)(?:spoofing|jamming|сигнал|при[её]м|позици|спутник|предупрежден)",
            "Q-NAV-029": r"(?i)(?:RAIM|при[её]мник|документац|3D|приложен|EGNOS|целостност)",
            "Q-NAV-030": r"(?i)(?:GNSS|приложен|датчик|рельеф|врем|курс\w*\s+носа|DR|карт|положен)",
            "Q-NAV-031": r"(?i)(?:положен|AVIATE|управлен|VMC|рельеф|препятств|пространств|ETA|курс|приложен)",
            "Q-NAV-032": r"(?i)(?:1-in-60|угл|расстоя|боков\w+\s+отклон|пройденн\w+\s+путь)",
            "Q-NAV-033": r"(?i)(?:угл|расхожден|возврат|лини[яи]\s+пути|снос|курс|ветр|склон)",
            "Q-NAV-034": r"(?i)(?:план\w*\s+пол[её]та|FPL|ATS|ULM|признан|разрешен|Part-21|государств\w+\s+прол[её]т)",
            "Q-NAV-035": r"(?i)(?:Part-NCO|воздушн\w+\s+судн|вид\w*\s+эксплуатац|операц|Annex\s+VII|Air Ops|лиценз|регистрац|FPL)",
        }
        self.assertEqual(set(blocks), set(domain_patterns))
        for identifier, pattern in domain_patterns.items():
            options = re.findall(
                r"(?m)^[A-D]\.\s+(.+?)(?:<br>)?\s*$", blocks[identifier]["body"]
            )
            self.assertEqual(4, len(options), identifier)
            for index, option in enumerate(options, 1):
                with self.subTest(question=identifier, option=index):
                    self.assertRegex(_plain_markdown(option), pattern)

        off_domain = re.compile(
            r"(?i)(?:поворачива\w+\s+карт|относительно\s+UTC|"
            r"\bштил|цвет\w*\s+(?:маршрут|лини)|внешн\w+\s+вид\w*\s+таблиц|"
            r"через\s+пять\s+минут|электронн\w+\s+карт\w+.{0,50}разреш)"
        )
        for block in blocks.values():
            for option in re.findall(r"(?m)^[A-D]\.\s+(.+?)(?:<br>)?\s*$", block["body"]):
                self.assertIsNone(off_domain.search(_plain_markdown(option)), block["id"])

    def test_q_nav_017_agrees_with_feminine_control_point_noun(self):
        text = self._read(TASK8_CHAPTERS[3])
        block = re.search(r"(?ms)^### Q-NAV-017\b.*?(?=^### Q-NAV-|^## )", text)
        self.assertIsNotNone(block)
        options = re.findall(r"(?m)^[A-D]\.\s+(.+?)(?:<br>)?\s*$", block.group(0))
        self.assertEqual(4, len(options))
        self.assertTrue(options[0].startswith("Она заметна, однозначна"))
        self.assertTrue(options[1].startswith("Она "))
        self.assertTrue(options[2].startswith("Она "))
        self.assertTrue(options[3].startswith("Её "))
        self.assertNotRegex(" ".join(options), r"\b(?:Он|Его)\b")

    def test_sample_route_names_and_escape_arrow_match_the_route_dossier(self):
        svg_text = self._read(TASK8_SVGS[2])
        route_chapter = self._read(TASK8_CHAPTERS[6])
        flight_log = self._read(TASK8_REFERENCE)
        for name in ("ES-ORIGIN", "ES-DESTINATION"):
            self.assertIn(name, svg_text)
            self.assertIn(name, route_chapter)
            self.assertIn(name, flight_log)
        self.assertNotRegex(svg_text, r"ES-(?:START|FINISH)")
        self.assertRegex(svg_text, r"(?is)уход\s+на\s+восток.{0,100}(?:СТОП|stop).{0,80}(?:провер|check).{0,80}AREA-A")

        root = ET.fromstring(svg_text)
        ns = "{http://www.w3.org/2000/svg}"
        escape = next(node for node in root.iter() if node.attrib.get("id") == "escape-east")
        self.assertEqual(1, len(list(escape.iter(f"{ns}line"))))
        self.assertFalse(list(escape.iter(f"{ns}rect")))
        self.assertFalse(list(escape.iter(f"{ns}text")))
        top_level_ids = [node.attrib.get("id") for node in list(root)]
        self.assertEqual("escape-east", top_level_ids[-1])

    def test_task8_svgs_are_accessible_mobile_and_semantically_geometric(self):
        required_ids = (
            {"heading-vector", "track-vector", "wind-vector", "wca-arc", "drift-arc", "arrowhead"},
            {"vor-station", "radial-from", "bearing-to", "aircraft", "dme-slant", "ground-range"},
            {"origin", "checkpoint-1", "checkpoint-2", "destination", "airspace", "terrain", "escape-east", "escape-west", "route-line"},
        )
        for relative_path, semantic_ids in zip(TASK8_SVGS, required_ids):
            root = self._xml(relative_path)
            ns = "{http://www.w3.org/2000/svg}"
            with self.subTest(path=relative_path):
                self.assertEqual(f"{ns}svg", root.tag)
                self.assertEqual("img", root.attrib.get("role"))
                self.assertTrue(root.attrib.get("aria-labelledby"))
                self.assertIsNotNone(root.find(f"{ns}title"))
                self.assertIsNotNone(root.find(f"{ns}desc"))
                self.assertFalse(list(root.iter(f"{ns}image")))
                _, _, vw, _ = (float(value) for value in root.attrib["viewBox"].split())
                self.assertLessEqual(vw, 760)
                sizes = [float(item.attrib["font-size"].removesuffix("px")) for item in root.iter(f"{ns}text") if "font-size" in item.attrib]
                self.assertTrue(sizes)
                self.assertGreaterEqual(min(sizes) * 340 / vw, 14.0)
                ids = {item.attrib.get("id") for item in root.iter() if item.attrib.get("id")}
                self.assertTrue(semantic_ids.issubset(ids), semantic_ids - ids)
                self.assertGreaterEqual(sum(1 for item in root.iter() if item.attrib.get("marker-end", "").startswith("url(#")), 2)

        wind_root = self._xml(TASK8_SVGS[0])
        wind_words = " ".join(wind_root.itertext()).casefold()
        for token in ("курс носа / heading", "линия пути / track", "ветер от / wind from", "wca", "снос / drift", "+ вправо", "− влево"):
            self.assertIn(token, wind_words)
        vor_words = " ".join(self._xml(TASK8_SVGS[1]).itertext()).casefold()
        for token in ("радиал от / radial from", "пеленг на / bearing to", "наклонная дальность / slant range", "горизонтальная дальность / horizontal"):
            self.assertIn(token, vor_words)
        route_words = " ".join(self._xml(TASK8_SVGS[2]).itertext())
        self.assertIn("СИНТЕТИЧЕСКАЯ УЧЕБНАЯ СХЕМА — НЕ ДЛЯ НАВИГАЦИИ", route_words)
        for token in ("Условный рельеф", "границы/статус: ПРОВЕРИТЬ", "уход на запад", "только Испания"):
            self.assertIn(token, route_words)

        for relative_path in TASK8_SVGS:
            root = self._xml(relative_path)
            title = root.find("{http://www.w3.org/2000/svg}title")
            desc = root.find("{http://www.w3.org/2000/svg}desc")
            with self.subTest(path=relative_path):
                self.assertRegex(title.text or "", r"[А-Яа-яЁё]")
                self.assertRegex(desc.text or "", r"[А-Яа-яЁё]")
                self.assertFalse((title.text or "").strip().startswith(("Wind", "Synthetic")))


class GU09MigrationTests(unittest.TestCase):
    CURRENT_ID = "SRC-AESA-ULM-LEARNING-OBJECTIVES-GU09-ED01"
    HISTORICAL_ID = "SRC-AESA-MAF-SYLLABUS-ED01"
    CURRENT_URL = (
        "https://www.seguridadaerea.gob.es/sites/default/files/"
        "FOR-ULM-P01-ETI01-GU09_Objetivos_de_aprendizaje_ULM.pdf"
    )
    HISTORICAL_URL = (
        "https://www.seguridadaerea.gob.es/sites/default/files/"
        "FOR-ULM-P01-ETI01-GU01%20Conocimientos%20teoricos%20"
        "habilitacion%20licencia%20de%20piloto%20de%20ULM%20%28MAF%29.pdf"
    )
    SUBJECT_SCOPES = (
        ("Derecho Aéreo", "pp. 7–14"),
        ("Principios de Vuelo", "pp. 15–20"),
        ("Performance y Planificación Vuelo", "pp. 21–27"),
        ("Navegación", "pp. 28–32"),
        ("Conocimiento General de la Aeronave", "pp. 33–39"),
        ("Meteorología", "pp. 40–48"),
        ("Procedimientos Operacionales", "pp. 49–58"),
        ("Actuaciones y Limitaciones Humanas", "pp. 59–62"),
        ("Comunicaciones", "p. 63"),
        ("Habilitación Radiotelefonía", "pp. 64–65"),
    )

    def _sources(self):
        return {
            source["id"]: source
            for source in json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
        }

    def test_current_and_historical_sources_are_distinct_and_explicitly_superseded(self):
        sources = self._sources()
        self.assertIn(self.CURRENT_ID, sources)
        self.assertIn(self.HISTORICAL_ID, sources)
        current = sources[self.CURRENT_ID]
        historical = sources[self.HISTORICAL_ID]
        self.assertEqual(self.CURRENT_URL, current["url"])
        self.assertEqual(self.HISTORICAL_URL, historical["url"])
        self.assertNotEqual(current["url"], historical["url"])
        self.assertRegex(
            current["edition"],
            r"GU09 Ed\.01.*страниц\w*.{0,20}обновлен\w* 29\.05\.2026.*"
            r"HTTP Last-Modified 29\.05\.2026.*Desde publicación",
        )
        self.assertNotIn("опубликовано 29.05.2026", current["edition"])
        self.assertIn("66", current["scope"])
        self.assertIn(
            "52947c9347a07f5df34e83853f8032528ca3df54938b73190eb728ef63938cf2",
            current["scope"],
        )
        self.assertRegex(
            historical["scope"],
            rf"(?is)(?:историческ|замен[её]н|superseded).{{0,180}}{re.escape(self.CURRENT_ID)}",
        )
        self.assertRegex(
            current["scope"],
            r"(?is)(?:цели обучения|learning objectives).{0,200}"
            r"не.{0,80}(?:источник|заменяет).{0,100}(?:физик|техническ)",
        )

    def test_old_gu01_id_is_absent_from_active_learner_chapters(self):
        violations = []
        for path in learner_chapter_files():
            if self.HISTORICAL_ID in path.read_text(encoding="utf-8"):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual([], violations)

        allowed_history_files = {
            "docs/sources/official-sources.json",
            "docs/sources/official-sources.md",
            "docs/sources/audit-technical.md",
            "docs/sources/audit-spain-2026.md",
        }
        occurrences = {
            str(path.relative_to(ROOT))
            for path in COURSE_DOCS.rglob("*.md")
            if self.HISTORICAL_ID in path.read_text(encoding="utf-8")
        }
        self.assertEqual(
            allowed_history_files - {"docs/sources/official-sources.json"},
            occurrences,
        )

    def test_each_active_gu09_citation_has_an_adjacent_exact_subject_page_scope(self):
        aggregate_scope = re.compile(
            r"(?is)(?:девят\w+\s+предмет|вс[ея]\s+программ).{0,100}"
            r"pp\.\s*7[–-]63"
        )
        violations = []
        seen = 0
        for path in learner_chapter_files():
            text = path.read_text(encoding="utf-8")
            for paragraph in re.split(r"\n\s*\n", text):
                if self.CURRENT_ID not in paragraph:
                    continue
                seen += paragraph.count(self.CURRENT_ID)
                exact = any(
                    subject in paragraph and pages in paragraph
                    for subject, pages in self.SUBJECT_SCOPES
                )
                if not exact and not aggregate_scope.search(paragraph):
                    line = text.count("\n", 0, text.find(paragraph)) + 1
                    violations.append(f"{path.relative_to(ROOT)}:{line}")
        self.assertGreater(seen, 0)
        self.assertEqual([], violations)

    def test_audit_matrix_represents_all_ten_gu09_subject_page_groups(self):
        audit = (ROOT / "docs/sources/audit-technical.md").read_text(encoding="utf-8")
        for subject, pages in self.SUBJECT_SCOPES:
            with self.subTest(subject=subject):
                row = next(
                    (
                        line
                        for line in audit.splitlines()
                        if self.CURRENT_ID in line and subject in line and pages in line
                    ),
                    None,
                )
                self.assertIsNotNone(row, f"{subject}, {pages}")

    def test_gu09_document_control_anomalies_and_uncontrolled_copy_are_recorded(self):
        evidence = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                SOURCE_REGISTRY,
                SOURCE_REGISTRY_MD,
                ROOT / "docs/sources/audit-technical.md",
                ROOT / "docs/sources/audit-spain-2026.md",
            )
        )
        for pattern in (
            r"(?is)p\.\s*66.{0,100}GU10\s+Ed\.01",
            r"(?is)p\.\s*3.{0,160}Trazabilidad.{0,220}"
            r"(?:нет|отсутств|не\s+содержит).{0,120}(?:отдельн|перечень|список)",
            r"(?is)(?:неконтролируем|uncontrolled).{0,140}"
            r"(?:сайт|web|страниц).{0,120}(?:AESA|актуальн|текущ)",
        ):
            self.assertRegex(evidence, pattern)

    def test_question_bank_transition_warning_is_dynamic_and_not_a_date_promise(self):
        sources = self._sources()
        source = sources["SRC-AESA-ULM-QUESTION-BANKS"]
        self.assertEqual("https://www.seguridadaerea.gob.es/es/node/3759", source["url"])
        self.assertIn("23.06.2026", source["edition"])

        chapter = (ROOT / "docs/00-start/03-medical-training-exams.md").read_text(
            encoding="utf-8"
        )
        warning = re.search(
            r"(?ms)^###\s+Переход банка вопросов.*?(?=^###\s|^##\s|\Z)",
            chapter,
        )
        self.assertIsNotNone(warning)
        plain = _plain_markdown(warning.group(0))
        for pattern in (
            r"(?is)23\.06\.2026",
            r"(?is)банк.{0,120}(?:пересматр|провер).{0,120}(?:GU09|нов\w+\s+цел)",
            r"(?is)после\s+лета\s+2026.{0,140}(?:план|намер)",
            r"(?is)дат\w+.{0,100}(?:объяв|опублик).{0,100}отдельн",
            r"(?is)не.{0,100}(?:полн\w+\s+соответств|уже\s+соответств)",
            r"(?is)не.{0,100}(?:обещан|гарантирован|фиксирован).{0,80}дат",
        ):
            self.assertRegex(plain, pattern)
        self.assertIn("SRC-AESA-ULM-QUESTION-BANKS", warning.group(0))
        self.assertNotRegex(
            plain,
            r"(?is)(?:переход|замена|внедрение).{0,50}"
            r"(?:с|произойд[её]т|назначен).{0,30}\d{1,2}[./]\d{1,2}[./]2026",
        )

    def test_gu09_source_registry_markdown_and_both_audits_are_in_parity(self):
        sources = self._sources()
        registry_rows = {
            row["id"]: row
            for row in source_rows_from_markdown(
                SOURCE_REGISTRY_MD.read_text(encoding="utf-8")
            )
        }
        for source_id in (
            self.CURRENT_ID,
            self.HISTORICAL_ID,
            "SRC-AESA-ULM-QUESTION-BANKS",
        ):
            self.assertEqual(sources[source_id], registry_rows[source_id])
        for path in (
            ROOT / "docs/sources/audit-technical.md",
            ROOT / "docs/sources/audit-spain-2026.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertIn(self.CURRENT_URL, text)
            self.assertIn("https://www.seguridadaerea.gob.es/es/node/3759", text)
        self.assertIn(
            self.HISTORICAL_URL,
            (ROOT / "docs/sources/audit-technical.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
