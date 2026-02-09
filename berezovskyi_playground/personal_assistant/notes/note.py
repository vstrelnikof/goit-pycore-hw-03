"""
Клас Note для окремої нотатки
"""
from datetime import datetime


class Note:
    """Клас для зберігання нотатки"""
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_tag(self, tag):
        """Додавання тегу"""
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.now()

    def remove_tag(self, tag):
        """Видалення тегу"""
        if tag.lower() in self.tags:
            self.tags.remove(tag.lower())
            self.updated_at = datetime.now()

    def edit(self, title=None, content=None):
        """Редагування нотатки"""
        if title:
            self.title = title
        if content:
            self.content = content
        self.updated_at = datetime.now()

    def to_dict(self):
        """Серіалізація нотатки в словник для JSON"""
        return {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """Десеріалізація нотатки зі словника JSON"""
        note = Note(data['title'], data['content'])
        note.tags = data.get('tags', [])
        note.created_at = datetime.fromisoformat(data['created_at'])
        note.updated_at = datetime.fromisoformat(data['updated_at'])
        return note

    def __str__(self):
        tags_str = f", теги: [{', '.join(self.tags)}]" if self.tags else ""
        return (f"📝 {self.title}\n"
                f"   {self.content}\n"
                f"   Створено: {self.created_at.strftime('%d.%m.%Y %H:%M')}"
                f"{tags_str}")
