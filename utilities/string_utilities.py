import json


def cleanup_translated_text(text):
    return text.replace("&quot;", "\"")
