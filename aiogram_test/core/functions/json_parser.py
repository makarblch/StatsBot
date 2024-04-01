from dataclasses import dataclass
import json


@dataclass
class User:
    first_name: str
    last_name: str
    status: str
    is_bot: bool
    is_premium: bool
    language: str


def serialize(userlist):
    json_data = json.dumps([data.__dict__ for data in userlist], ensure_ascii=False, indent=4)
    return json_data
