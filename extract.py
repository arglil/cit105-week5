
import json
import os
import re
import requests

ALLOWED_UNITS = {
    "each", "box", "case", "pack", "kg", "lb", "liter"
}

REQUIRED_FIELDS = {
    "item_name", "quantity", "unit", "unit_price"
}

PROMPT = """
Extract invoice line items from the text provided.

Return a JSON array of objects. Every object must have exactly
these four keys:

- item_name: non-empty string
- quantity: positive number greater than zero
- unit: one of "each", "box", "case", "pack", "kg", "lb", "liter"
- unit_price: number greater than or equal to zero

Use the singular unit name. Do not invent missing prices,
quantities, or items. If an item cannot be represented with
all four required fields, omit it.

Return [] if there are no valid invoice items.

Do not include a preamble, explanation, markdown code fence,
comments, or any text outside the JSON array.
""".strip()


def validate_items(items):
    """Validate the structure and values of extracted items."""
    if not isinstance(items, list):
        return False, "The response is not a JSON array."

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return False, f"Item {index} is not an object."

        if set(item.keys()) != REQUIRED_FIELDS:
            return False, f"Item {index} has incorrect fields."

        if not isinstance(item["item_name"], str) or not item["item_name"].strip():
            return False, f"Item {index} has an invalid name."

        quantity = item["quantity"]
        if type(quantity) not in (int, float) or not (0 < quantity < float("inf")):
            return False, f"Item {index} has an invalid quantity."

        if item["unit"] not in ALLOWED_UNITS:
            return False, f"Item {index} has an invalid unit."

        price = item["unit_price"]
        if type(price) not in (int, float) or not (0 <= price < float("inf")):
            return False, f"Item {index} has an invalid unit price."

    return True, None


def parse_response(response_text):
    """Extract and validate the first complete JSON array in AI text."""
    if not isinstance(response_text, str):
        return [], "The AI response was not text."

    decoder = json.JSONDecoder()

    for match in re.finditer(r"\[", response_text):
        try:
            items, _ = decoder.raw_decode(response_text[match.start():])
        except (ValueError, TypeError):
            continue

        valid, error = validate_items(items)
        if not valid:
            return [], error

        return items, None

    return [], "No complete JSON array was found in the AI response."


def extract_invoice(text):
    """Call the AI API and return validated invoice items."""
    api_key = os.getenv("AI_API_KEY")
    api_url = os.getenv("AI_API_URL")
    model = os.getenv("AI_MODEL")

    if not api_key or not api_url or not model:
        return [], "Missing AI API configuration.", None

    if not text.strip():
        return [], "Please provide invoice text.", None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.status_code != 200:
            return [], f"AI API returned HTTP {response.status_code}.", None

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError):
            return [], "The AI API returned an unexpected response.", None

        items, error = parse_response(content)

        usage = data.get("usage", {})
        if not isinstance(usage, dict):
            usage = {}

        return items, error, usage

    except requests.exceptions.Timeout:
        return [], "The AI API request timed out.", None

    except requests.exceptions.RequestException:
        return [], "Could not connect to the AI API.", None


def main():
    print("INVOICE ITEM EXTRACTOR")
    print("Paste invoice text. Press Enter on an empty line to finish.")

    lines = []

    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    invoice_text = "\n".join(lines)

    items, error, usage = extract_invoice(invoice_text)

    if error:
        print(f"\nError: {error}")
    else:
        print("\nExtracted invoice items:")
        print(json.dumps(items, indent=2))

    if usage is not None:
        print("\nToken usage:")
        print(f"Prompt tokens: {usage.get('prompt_tokens', 'Unavailable')}")
        print(f"Completion tokens: {usage.get('completion_tokens', 'Unavailable')}")
        print(f"Total tokens: {usage.get('total_tokens', 'Unavailable')}")


if __name__ == "__main__":
    main()

