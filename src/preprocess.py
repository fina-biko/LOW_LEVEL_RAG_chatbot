import re

def clean_text(text: str) -> str:

    """
    Clean raw extracted text before chunking or passing to an LLM.

    Steps performed:
    1. Replace double newlines ("\n\n") with a single space
       - Merges paragraph breaks into a flowing text.
    2. Replace single newlines ("\n") with a space
       - Ensures lines from PDFs don’t appear broken.
    3. Remove hyphen + newline word breaks
       - Example: "pri-\nmary" → "primary".
    4. Collapse multiple spaces into a single space
       - Example: "I   am   here" → "I am here".
    5. Normalize spaces before punctuation
       - Example: "Hello , world !" → "Hello, world!".
    6. Strip leading and trailing spaces
       - Ensures clean text without unnecessary whitespace at start or end.

    Args:
        text (str): The raw extracted text.

    Returns:
        str: A cleaned, normalized version of the text.
    """

    # 1. Replace double newlines (\n\n) with a single space
    text = text.replace("\n\n", " ")

    # 2. Replace single newlines (\n) with a space
    text = text.replace("\n", " ")

    # 3. Remove broken words where a hyphen is followed by a newline
    # Example: "pri-\nmary" → "primary"
    text = re.sub(r"-\s+", "", text)

    # 4. Collapse multiple spaces into a single space
    # Example: "I   am   here" → "I am here"
    text = re.sub(r"\s+", " ", text)

    # 5. (Optional) Normalize spaces before punctuation
    # Example: "Hello , world !" → "Hello, world!"
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    # 6. (Optional) Strip leading/trailing spaces
    text = text.strip()

    return text
