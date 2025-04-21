# utils.py

import re
import spacy
from typing import List, Tuple, Dict

# Load SpaCy model for NER
nlp = spacy.load("en_core_web_sm")

# PII REGEX patterns
PII_REGEX = {
    "email": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
    "credit_debit_no": r'\b(?:\d[ -]*?){13,16}\b',
    "aadhar_num": r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
    "phone_number": r'(\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,5}\)?[-.\s]?){1,5}\d{2,4}',
    "dob": r'\b(0[1-9]|[12][0-9]|3[01])[/-]'
           r'(0[1-9]|1[0-2])[/-]'
           r'(19|20)\d{2}\b',
    "cvv_no": r'(?<!\d)(\d{3,4})(?![\d-])',
    "expiry_no": r'\b(0[1-9]|1[0-2])[\/\-](\d{2}|\d{4})\b'
}

# Order of entity tagging (longest matches first)
PII_ORDER = [
    "email",
    "credit_debit_no",
    "aadhar_num",
    "phone_number",
    "dob",
    "cvv_no",
    "expiry_no"
]


def is_overlap(start: int, end: int, spans: List[Tuple[int, int]]) -> bool:
    """
    Check if the given range overlaps with any existing span.
    """
    return any(s < end and start < e for s, e in spans)


def mask_pii(text: str) -> Tuple[str, List[Dict]]:
    """
    Detect and mask PII entities in the text.
    Returns masked text and metadata for demasking.
    """
    masked_email = text
    entity_list = []
    offset = 0
    used_spans = []

    for entity_type in PII_ORDER:
        pattern = PII_REGEX.get(entity_type)
        if not pattern:
            continue

        for match in re.finditer(pattern, masked_email):
            start, end = match.start(), match.end()
            new_start, new_end = start + offset, end + offset

            if is_overlap(new_start, new_end, used_spans):
                continue

            original = match.group()
            tag = f"[{entity_type}]"
            masked_email = masked_email[:new_start] + tag + masked_email[new_end:]
            entity_list.append({
                "position": [new_start, new_start + len(tag)],
                "classification": entity_type,
                "entity": original
            })

            used_spans.append((new_start, new_start + len(tag)))
            offset += len(tag) - len(original)

    # Apply SpaCy NER for full_name *after* regex masking
    doc = nlp(masked_email)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            if is_overlap(start, end, used_spans):
                continue

            original = ent.text
            tag = "[full_name]"
            masked_email = masked_email[:start] + tag + masked_email[end:]
            entity_list.append({
                "position": [start, start + len(tag)],
                "classification": "full_name",
                "entity": original
            })
            used_spans.append((start, start + len(tag)))

    return masked_email, entity_list


def demask(masked_text: str, entities: List[Dict]) -> str:
    """
    Restore original PII entities in the masked text.
    """
    restored = masked_text
    for ent in sorted(entities, key=lambda x: x['position'][0], reverse=True):
        start, end = ent['position']
        restored = restored[:start] + ent['entity'] + restored[end:]
    return restored
