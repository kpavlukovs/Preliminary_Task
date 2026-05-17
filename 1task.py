def clean_and_classify(messages):
  keywords = {
        "grant_search": ["grant", "funding", "deadline", "scholarship"],
        "report_request": ["report", "file", "send again", "document"],
        "general_question": ["how", "what", "can you", "where", "why"]
    }
  cleaned = []
  for msg in messages:
    user_id = msg["user_id"].strip()
    text = msg["message"].strip()
    if not user_id or not text:
      continue
    t = text.lower()
    category="unknown"
    # Here i used priority order from grant_search to report_request to general_question so topic-specific categories win over more generic question patterns.
    for categ in ["grant_search", "report_request", "general_question"]:
      if any(word in t for word in keywords[categ]):
        category=categ
        break
    cleaned.append({
      "user_id": user_id,
      "channel": msg["channel"],
      "message": text,
      "category": category
    })
  return cleaned

messages = [
 {"user_id": "u1", "channel": "email", "message": "Hello, I want info about grants for education."},
 {"user_id": "u2", "channel": "whatsapp", "message": " "},
 {"user_id": "", "channel": "email", "message": "What is the deadline?"},
 {"user_id": "u3", "channel": "email", "message": "Please send the report again."},
 {"user_id": "u1", "channel": "whatsapp", "message": " Can you help me find funding? "},
 {"user_id": "u4", "channel": "telegram", "message": "Good morning!"},
 {"user_id": "u5", "channel": "email", "message": "Can you send me the scholarship document?"},
 {"user_id": "u6", "channel": "whatsapp", "message": ""},
]

result = clean_and_classify(messages)
for r in result:
  print(r)

"""
Result output
{'user_id': 'u1', 'channel': 'email', 'message': 'Hello, I want info about grants for education.', 'category': 'grant_search'}
{'user_id': 'u3', 'channel': 'email', 'message': 'Please send the report again.', 'category': 'report_request'}
{'user_id': 'u1', 'channel': 'whatsapp', 'message': 'Can you help me find funding?', 'category': 'grant_search'}
{'user_id': 'u4', 'channel': 'telegram', 'message': 'Good morning!', 'category': 'unknown'}
{'user_id': 'u5', 'channel': 'email', 'message': 'Can you send me the scholarship document?', 'category': 'grant_search'}
"""
