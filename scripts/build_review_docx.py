#!/usr/bin/env python3
"""Build comments using the user's retained Word paragraph and numbering styles."""

import argparse
from copy import copy, deepcopy
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DC = "http://purl.org/dc/elements/1.1/"
NS = {"w": W}
SKILL_DIR = Path(__file__).resolve().parents[1]


def parse_xml(data):
    return etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))


def xml_bytes(root):
    return etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone=True)


def text_of(paragraph):
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def xml_structure(node):
    """Compare actual XML values, independent of inherited namespace declarations."""
    return (node.tag, tuple(sorted(node.attrib.items())), node.text or "",
            tuple(xml_structure(child) for child in node))


def replace_paragraph(prototype, text):
    paragraph = deepcopy(prototype)
    for key in list(paragraph.attrib):
        if etree.QName(key).localname in {"paraId", "textId"}:
            del paragraph.attrib[key]
    run_properties = None
    for run in paragraph.findall("w:r", NS):
        if run.find("w:t", NS) is not None:
            run_properties = run.find("w:rPr", NS)
            break
    if run_properties is None:
        run_properties = paragraph.find("w:pPr/w:rPr", NS)
    run_properties = deepcopy(run_properties) if run_properties is not None else None
    for child in list(paragraph):
        if child.tag != f"{{{W}}}pPr":
            paragraph.remove(child)
    run = etree.SubElement(paragraph, f"{{{W}}}r")
    if run_properties is not None:
        run.append(run_properties)
    node = etree.SubElement(run, f"{{{W}}}t")
    node.text = text
    node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return paragraph


def clean_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    if any(ord(char) < 32 or char in "\u2028\u2029" for char in value):
        raise ValueError(f"{field} must be one paragraph without control characters")
    return value.strip()


def validate_input(data):
    required = {"manuscript_id", "language", "summary", "comments"}
    if not isinstance(data, dict) or set(data) != required:
        raise ValueError(f"Input must contain exactly: {', '.join(sorted(required))}")
    if data["language"] not in ("en", "zh"):
        raise ValueError("language must be en or zh")
    if not isinstance(data["comments"], list):
        raise ValueError("comments must be an array of paragraph strings")
    result = dict(data)
    result["manuscript_id"] = clean_text(data["manuscript_id"], "manuscript_id")
    result["summary"] = clean_text(data["summary"], "summary")
    result["comments"] = []
    for index, value in enumerate(data["comments"], 1):
        value = clean_text(value, f"comments[{index}]")
        if re.match(r"^\d+[.)、]\s*", value):
            raise ValueError(f"comments[{index}] has a typed number; Word supplies numbering")
        result["comments"].append(value)
    return result


def make_package(data, template):
    with ZipFile(template) as source:
        root = parse_xml(source.read("word/document.xml"))
        body = root.find("w:body", NS)
        paragraphs = body.findall("w:p", NS)
        if [text_of(p) for p in paragraphs] != [
            "Comments on {{MANUSCRIPT_ID}}", "{{SUMMARY}}", "", "{{COMMENT}}"
        ]:
            raise ValueError("Template slots are missing or have changed")
        title_p, summary_p, blank_p, comment_p = paragraphs
        section = deepcopy(body.find("w:sectPr", NS))
        if section is None:
            raise ValueError("Template section settings are missing")
        for child in list(body):
            body.remove(child)
        title = "Comments on " + data["manuscript_id"]
        body.append(replace_paragraph(title_p, title))
        body.append(replace_paragraph(summary_p, data["summary"]))
        if data["comments"]:
            body.append(deepcopy(blank_p))
        for index, comment in enumerate(data["comments"]):
            if index and data["language"] == "zh":
                body.append(deepcopy(blank_p))
            body.append(replace_paragraph(comment_p, comment))
        body.append(section)
        core = parse_xml(source.read("docProps/core.xml"))
        title_node = core.find(f"{{{DC}}}title")
        if title_node is None:
            title_node = etree.SubElement(core, f"{{{DC}}}title")
        title_node.text = title
        changes = {"word/document.xml": xml_bytes(root), "docProps/core.xml": xml_bytes(core)}
        stream = BytesIO()
        with ZipFile(stream, "w") as target:
            for member in source.infolist():
                target.writestr(copy(member), changes.get(member.filename, source.read(member.filename)))
        result = stream.getvalue()
        with ZipFile(BytesIO(result)) as target:
            parsed = parse_xml(target.read("word/document.xml"))
            out_ps = parsed.findall("w:body/w:p", NS)
            actual = [text_of(p) for p in out_ps if text_of(p)]
            expected = [title, data["summary"], *data["comments"]]
            if actual != expected:
                raise ValueError("Output text does not match input")
            numbered = [p for p in out_ps if p.find("w:pPr/w:numPr", NS) is not None]
            if len(numbered) != len(data["comments"]):
                raise ValueError("Output comment numbering is inconsistent")
            num_prototype = xml_structure(comment_p.find("w:pPr/w:numPr", NS))
            if any(xml_structure(p.find("w:pPr/w:numPr", NS)) != num_prototype for p in numbered):
                raise ValueError("Output numbering differs from template")
            if xml_structure(parsed.find("w:body/w:sectPr", NS)) != xml_structure(section):
                raise ValueError("Output page settings differ from template")
            for name in source.namelist():
                if name not in changes and target.read(name) != source.read(name):
                    raise ValueError(f"Preserved package part changed: {name}")
        return result


def build_review(data, output):
    data = validate_input(data)
    template = SKILL_DIR / "assets" / f"review-{data['language']}.docx"
    output = Path(output).resolve()
    if output.suffix.lower() != ".docx":
        raise ValueError("Output filename must end in .docx")
    if output == template.resolve():
        raise ValueError("Output cannot replace a retained template")
    package = make_package(data, template)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(package)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Output cannot overwrite the JSON input")
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        output = build_review(data, args.output)
    except (OSError, ValueError, etree.XMLSyntaxError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(json.dumps({"output": str(output), "comments": len(data["comments"]),
                      "structural_validation": "passed", "visual_qa": "required"}, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
