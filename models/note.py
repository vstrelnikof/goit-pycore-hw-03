from dataclasses import dataclass, field
from typing import List

@dataclass
class Note:
    text: str
    tags: List[str] = field(default_factory=list)

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "без тегів"
        return f"Нотатка: {self.text} | Теги: {tags_str}"