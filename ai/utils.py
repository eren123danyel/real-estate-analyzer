import json
import spacy

nlp = spacy.load("en_core_web_sm")
def extract_locations(text: str):
    """
    Extracts location from the given string using spaCy NLP.
    """
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]


def extract_tool_output(result):
    """
    Extracts usable content (text or JSON) from an MCP CallToolResult object.
    """

    content = getattr(result, "content", None)
    if not content or not isinstance(content, list):
        return None

    for block in content:
        block_type = getattr(block, "type", None)

        if block_type == "text" and hasattr(block, "text"):
            text_data = block.text

            if isinstance(text_data, str) and text_data.startswith("### Result"):
                lines = text_data.split('\n', 1)
                if len(lines) > 1:
                    raw = lines[1].strip()
                    try:
                        # unescape if it’s JSON-encoded HTML
                        html = json.loads(raw)
                    except json.JSONDecodeError:
                        # fallback: decode escaped sequences
                        html = raw.encode("utf-8").decode("unicode_escape")
                    return html

            # handle already-plain HTML
            if text_data.startswith('"') and text_data.endswith('"'):
                try:
                    return json.loads(text_data)
                except json.JSONDecodeError:
                    return text_data.encode("utf-8").decode("unicode_escape")

            return text_data

        if block_type == "json" and hasattr(block, "data"):
            return block.data

        if block_type == "blob" and hasattr(block, "data"):
            return block.data

    return None
