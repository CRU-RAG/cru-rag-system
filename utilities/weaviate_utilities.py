import json
from typing import List, Dict, Any


def get_content_bodies(docs: Dict[str, Any]) -> List[str]:
    return [content["body"] for content in docs["data"]["Get"]["CRURAG"]]


def flatten_response(docs: Dict[str, Any]) -> str:
    bodies = get_content_bodies(docs)
    return ", ".join(bodies)
