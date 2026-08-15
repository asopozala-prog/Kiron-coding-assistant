# Generate a filled legal engagement agreement PDF from verified session data.

from pathlib import Path
from typing import Any

import pymupdf


REQUIRED_FIELDS = [
    "Agreement Date",
    "Responsible Attorney",
    "Client Name",
    "Company Registration",
    "Client Address",
    "Client Representative",
    "Matter ID",
    "Case Type",
    "Matter Description",
    "Fee Arrangement",
]

FIELD_LAYOUT = {
    "Agreement Date": {
        "placeholder": "[AGREEMENT DATE]",
        "right": 530,
        "kind": "single",
    },
    "Responsible Attorney": {
        "placeholder": "[RESPONSIBLE ATTORNEY]",
        "right": 270,
        "kind": "single",
    },
    "Client Name": {
        "placeholder": "[CLIENT NAME]",
        "right": 530,
        "kind": "single",
    },
    "Company Registration": {
        "placeholder": "[COMPANY REGISTRATION]",
        "right": 530,
        "kind": "single",
    },
    "Client Address": {
        "placeholder": "[CLIENT ADDRESS]",
        "right": 530,
        "kind": "single",
    },
    "Client Representative": {
        "placeholder": "[CLIENT REPRESENTATIVE]",
        "right": 530,
        "kind": "single",
    },
    "Matter ID": {
        "placeholder": "[MATTER ID]",
        "right": 530,
        "kind": "single",
    },
    "Case Type": {
        "placeholder": "[CASE TYPE]",
        "right": 530,
        "kind": "single",
    },
    "Matter Description": {
        "placeholder": "[MATTER DESCRIPTION]",
        "right": 530,
        "bottom": 523,
        "kind": "multiline",
    },
    "Fee Arrangement": {
        "placeholder": "[FEE ARRANGEMENT]",
        "right": 530,
        "kind": "single",
    },
}


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _validate_required(data: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if not _clean_value(data.get(field))]
    if missing:
        raise ValueError(
            "Cannot generate agreement because required fields are missing: "
            + ", ".join(missing)
        )


def _fit_single_line(page: pymupdf.Page, rect: pymupdf.Rect, right: float, text: str) -> None:
    """Insert one line, shrinking slightly when needed."""
    max_width = right - rect.x0
    font_size = 9.0

    while font_size >= 6.5:
        width = pymupdf.get_text_length(text, fontname="helv", fontsize=font_size)
        if width <= max_width:
            break
        font_size -= 0.25

    if pymupdf.get_text_length(text, fontname="helv", fontsize=font_size) > max_width:
        raise ValueError(f"Text is too long to fit the PDF field: {text}")

    page.insert_text(
        (rect.x0, rect.y1 - 1),
        text,
        fontsize=font_size,
        fontname="helv",
        color=(0, 0, 0),
    )


def _fit_multiline(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    right: float,
    bottom: float,
    text: str,
) -> None:
    """Insert wrapped text into a bounded region."""
    box = pymupdf.Rect(rect.x0, rect.y0 - 1, right, bottom)

    for font_size in (9.0, 8.5, 8.0, 7.5, 7.0):
        result = page.insert_textbox(
            box,
            text,
            fontsize=font_size,
            fontname="helv",
            color=(0, 0, 0),
            align=0,
        )
        if result >= 0:
            return

    raise ValueError("Matter Description is too long to fit the PDF template.")


def generate_agreement_pdf(template_path: str | Path, data: dict[str, Any]) -> bytes:
    """Fill the flattened PDF template and return the generated PDF as bytes."""
    _validate_required(data)

    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"PDF template not found: {template_path}")

    document = pymupdf.open(template_path)

    try:
        page = document[0]
        located: dict[str, pymupdf.Rect] = {}

        for field, config in FIELD_LAYOUT.items():
            placeholder = config["placeholder"]
            matches = page.search_for(placeholder)

            if len(matches) != 1:
                raise ValueError(
                    f"Expected exactly one {placeholder} placeholder, found {len(matches)}."
                )

            rect = matches[0]
            located[field] = rect
            page.add_redact_annot(rect + (-1, -1, 1, 1), fill=(1, 1, 1))

        page.apply_redactions()

        for field, config in FIELD_LAYOUT.items():
            text = _clean_value(data.get(field))
            rect = located[field]

            if config["kind"] == "single":
                _fit_single_line(page, rect, config["right"], text)
            else:
                _fit_multiline(
                    page,
                    rect,
                    config["right"],
                    config["bottom"],
                    text,
                )

        return document.tobytes(garbage=4, deflate=True)
    finally:
        document.close()
