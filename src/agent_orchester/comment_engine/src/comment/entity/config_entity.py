from dataclasses import dataclass

@dataclass
class PostData:
    post_urn: str
    post_text: str
    headers: dict
