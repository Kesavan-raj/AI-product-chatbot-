import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from urllib.parse import quote_plus

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an Indian shopping AI. When user asks for a product:
Return ONLY valid JSON in this format:
{
  "query_summary": "wireless earbuds under ₹2000",
  "products": [
    {
      "rank": 1,
      "name": "boAt Airdopes 141",
      "ai_score": 91,
      "tags": ["42H Battery", "IPX4", "Bluetooth 5.1"],
      "why_recommended": "Best battery life in budget, trusted brand",
      "platforms": {
        "flipkart": {"price": 1199, "available": true, "url": ""},
        "amazon":   {"price": 1249, "available": true, "url": ""},
        "myntra":   {"price": null, "available": false, "url": ""},
        "ajio":     {"price": null, "available": false, "url": ""},
        "meesho":   {"price": 1099, "available": true, "url": ""}
      },
      "best_platform": "meesho",
      "best_price": 1099
    }
  ]
}
"""


def _platform_url(product_name: str, platform: str) -> str:
    if not product_name:
        return '#'
    if platform == 'flipkart':
        return f"https://www.flipkart.com/search?q={quote_plus(product_name)}"
    if platform == 'amazon':
        return f"https://www.amazon.in/s?k={quote_plus(product_name)}"
    if platform == 'myntra':
        slug = re.sub(r"[^a-z0-9\s-]", '', product_name.lower())
        slug = re.sub(r"\s+", '-', slug.strip())
        return f"https://www.myntra.com/{slug}"
    if platform == 'ajio':
        return f"https://www.ajio.com/search/?text={quote_plus(product_name)}"
    if platform == 'meesho':
        return f"https://www.meesho.com/search?q={quote_plus(product_name)}"
    return '#'


def _extract_budget(message: str):
    pattern = r'(?:under|below|within|max|upto|up to|less than)\s*[₹rs.]?\s*([\d,]+)\s*k?'
    match = re.search(pattern, message, re.IGNORECASE)
    if match:
        num_str = match.group(1).replace(',', '')
        num = int(num_str)
        if re.search(r'[\d,]+\s*k\b', match.group(0), re.IGNORECASE):
            num *= 1000
        return num
    return None


def _normalize_model_output(ai_text: str):
    ai_text = re.sub(r'```(?:json)?', '', ai_text).strip('`').strip()
    try:
        return json.loads(ai_text)
    except Exception:
        m = re.search(r'(\{.*\})', ai_text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
    return None


def _safe_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        s = re.sub(r"[^0-9]", '', str(value))
        return int(s) if s else None


def ask_ai(message: str, history: list):
    try:
        # Build messages for Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role in ("user", "assistant"):
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,
        )

        ai_message = response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")

    parsed = _normalize_model_output(ai_message)

    if not parsed:
        return ai_message

    budget = _extract_budget(message)
    valid_products = []

    for prod in parsed.get('products', []):
        prod['price_inr'] = _safe_int(prod.get('best_price'))

        if budget is not None and prod['price_inr'] is not None:
            if prod['price_inr'] >= budget:
                continue

        platforms_raw = prod.get('platforms', {}) or {}
        enriched = {}
        for platform in ['flipkart', 'amazon', 'myntra', 'ajio', 'meesho']:
            raw_entry = platforms_raw.get(platform)
            if isinstance(raw_entry, dict):
                price_val = _safe_int(raw_entry.get('price'))
            else:
                price_val = _safe_int(raw_entry)

            if budget is not None and price_val is not None:
                if price_val >= budget:
                    price_val = None

            enriched[platform] = {
                'price': price_val,
                'url': _platform_url(prod.get('name', ''), platform)
            }
        prod['platforms'] = enriched
        valid_products.append(prod)

    parsed['products'] = valid_products
    return parsed