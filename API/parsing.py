import json

ALLOWED_CATEGORIES = {"billing", "technical", "account", "other"}
ALLOWED_PRIORITY = {"low", "medium", "high"}

def parse_and_validate(text):
    # 1. Try to parse as JSON
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        t = text.strip()
        if t.startswith("```"):
            t = t.strip("`")
            t = t.replace("json", "", 1).strip()
        data = json.loads(t)

    # 2. Basic validation
    if data.get("category") not in ALLOWED_CATEGORIES:
        data["category"] = "other"

    if data.get("priority") not in ALLOWED_PRIORITY:
        data["priority"] = "medium"

    if not isinstance(data.get("short_summary", ""), str):
        data["short_summary"] = ""

    return data

# ------------ RUN CODE HERE --------------
text = '{"category":"billing","priority":"high","short_summary":"Payment failed"}'
result = parse_and_validate(text)
print(result)
