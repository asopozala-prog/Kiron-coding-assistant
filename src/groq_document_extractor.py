# Groq-powered structured document extraction for the Kiron workspace demo.

import json
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from groq import Groq


MODEL_ID = "openai/gpt-oss-20b"

FIELDS = [
    "Responsible Attorney",
    "Prepared By",
    "Department",
    "Matter ID",
    "Case Type",
    "Matter Title",
    "Matter Description",
    "Agreement Date",
    "Client Name",
    "Company Registration",
    "Client Address",
    "Client Representative",
    "Representative Position",
    "Contact Email",
    "Contact Telephone",
    "Scope of Representation",
    "Court Representation Required",
    "Negotiation Required",
    "Contract Review Required",
    "Other Services",
    "Fee Arrangement",
    "Estimated Professional Fees",
    "Billing Method",
    "Payment Due Days",
    "Expected External Expenses",
    "Applicable Law",
    "Jurisdiction",
    "Special Instructions",
    "Additional Notes",
]

REQUIRED_AGREEMENT_FIELDS = [
    "Responsible Attorney",
    "Matter ID",
    "Case Type",
    "Matter Description",
    "Agreement Date",
    "Client Name",
    "Company Registration",
    "Client Address",
    "Client Representative",
    "Fee Arrangement",
]


@dataclass
class ExtractionResult:
    data: dict[str, Any]
    status: str
    verification_markdown: str


def _schema_instruction() -> str:
    field_lines = "\n".join(f'- "{field}"' for field in FIELDS)
    return f"""
Return ONE valid JSON object only.

The JSON must contain exactly these keys:
{field_lines}

Rules:
- Extract only information supported by the source document.
- Never invent missing facts.
- Use null when a field is not present.
- Keep names, IDs, addresses, dates, and fee wording faithful to the source.
- For Yes/No fields, use "Yes", "No", or null.
- Matter Description should be concise: one or two sentences.
- Scope of Representation should summarize the requested legal work.
- Infer Case Type only when the source clearly describes the legal matter.
- Do not add markdown or commentary outside the JSON object.
"""


def extract_case_data(source_text: str) -> ExtractionResult:
    """Extract structured legal engagement data from one source document."""
    load_dotenv()

    client = Groq()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Kiron, a careful legal-document data extraction assistant. "
                    "Your task is extraction, not legal advice. "
                    + _schema_instruction()
                ),
            },
            {
                "role": "user",
                "content": f"Extract the engagement data from this source document:\n\n{source_text}",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = completion.choices[0].message.content
    parsed = json.loads(raw)

    data = {field: parsed.get(field) for field in FIELDS}
    missing_required = [
        field for field in REQUIRED_AGREEMENT_FIELDS if not data.get(field)
    ]

    if not missing_required:
        status = (
            "Kiron: I found all required agreement data. "
            "Please verify the extracted information below."
        )
    elif len(missing_required) <= 2:
        status = (
            "Kiron: I extracted the available data, but "
            f"{len(missing_required)} required field(s) are missing: "
            + ", ".join(missing_required)
            + ". Please review them before confirming."
        )
    else:
        status = (
            "Kiron: Some required information is missing. I could not find: "
            + ", ".join(missing_required)
            + "."
        )

    return ExtractionResult(
        data=data,
        status=status,
        verification_markdown=build_verification_markdown(data),
    )


def _display(value: Any) -> str:
    if value is None or value == "":
        return "⚠️ Not found in source"
    return str(value)


def build_verification_markdown(data: dict[str, Any]) -> str:
    """Render extracted data into Alex's review document."""
    return f"""# Review Schema — Legal Services Engagement Agreement

Purpose:
Extract only the information required to generate the Legal Services Engagement Agreement.

---

## Law Firm Information

Responsible Attorney: {_display(data["Responsible Attorney"])}

Prepared By: {_display(data["Prepared By"])}

Department: {_display(data["Department"])}

---

## Matter Information

Matter ID: {_display(data["Matter ID"])}

Case Type: {_display(data["Case Type"])}

Matter Title: {_display(data["Matter Title"])}

Matter Description: {_display(data["Matter Description"])}

Agreement Date: {_display(data["Agreement Date"])}

---

## Client Information

Client Name: {_display(data["Client Name"])}

Company Registration: {_display(data["Company Registration"])}

Client Address: {_display(data["Client Address"])}

Client Representative: {_display(data["Client Representative"])}

Representative Position: {_display(data["Representative Position"])}

Contact Email: {_display(data["Contact Email"])}

Contact Telephone: {_display(data["Contact Telephone"])}

---

## Legal Scope

Scope of Representation: {_display(data["Scope of Representation"])}

Court Representation Required: {_display(data["Court Representation Required"])}

Negotiation Required: {_display(data["Negotiation Required"])}

Contract Review Required: {_display(data["Contract Review Required"])}

Other Services: {_display(data["Other Services"])}

---

## Financial Information

Fee Arrangement: {_display(data["Fee Arrangement"])}

Estimated Professional Fees: {_display(data["Estimated Professional Fees"])}

Billing Method: {_display(data["Billing Method"])}

Payment Due Days: {_display(data["Payment Due Days"])}

Expected External Expenses: {_display(data["Expected External Expenses"])}

---

## Legal Information

Applicable Law: {_display(data["Applicable Law"])}

Jurisdiction: {_display(data["Jurisdiction"])}

---

## Optional Notes

Special Instructions: {_display(data["Special Instructions"])}

Additional Notes: {_display(data["Additional Notes"])}

---

## Verification

Verified by Alex Hoffmann

Verification Date:

Reviewer Comments:
"""
