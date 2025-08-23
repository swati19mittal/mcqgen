import re
import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for p in reader.pages:
            page_text = p.extract_text() or ""
            text += page_text + "\n"
    return text

def clean_text(text, max_len=None):
    # simple cleanup
    out = re.sub(r"\s+", " ", text).strip()
    if max_len and len(out) > max_len:
        return out[:max_len]
    return out

def extract_json_from_response(resp_text):
    """
    Try to find the first JSON object in the LLM output and parse it.
    Returns dict or raises ValueError.
    """
    import json, re
    # find first {...} block
    match = re.search(r"\{(?:[^{}]|(?R))*\}", resp_text)
    if not match:
        # fallback: try to find '[' (list) and parse
        match = re.search(r"\[.*\]", resp_text, flags=re.S)
        if not match:
            raise ValueError("No JSON block found in response")
    json_text = match.group(0)
    return json.loads(json_text)
