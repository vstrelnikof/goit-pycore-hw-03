"""
Клас NoteBook для управління нотатками
"""
import json
from pathlib import Path
from .note import Note


class NoteBook:
    """Клас для зберігання та управління нотатками"""
    def __init__(self, data_dir=None):
        self.notes = []
        
        if data_dir is None:
            # За замовчуванням зберігаємо в папці проекту
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
        else:
            data_dir = Path(data_dir)
        
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = data_dir / "notes.json"

    def add_note(self, note):
        """Додавання нотатки"""
        self.notes.append(note)

    def delete_note(self, index):
        """Видалення нотатки за індексом"""
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return True
        return False

    def find_note(self, index):
        """Пошук нотатки за індексом"""
        if 0 <= index < len(self.notes):
            return self.notes[index]
        return None

    def search(self, query):
        """Пошук нотаток за текстом"""
        results = []
        query_lower = query.lower()
        
        for i, note in enumerate(self.notes):
            if (query_lower in note.title.lower() or 
                query_lower in note.content.lower()):
                results.append((i, note))
        
        return results

    def search_by_tag(self, tag):
        """Пошук нотаток за тегом"""
        results = []
        tag_lower = tag.lower()
        
        for i, note in enumerate(self.notes):
            if tag_lower in note.tags:
                results.append((i, note))
        
        return results

    def get_all_tags(self):
        """Отримання всіх унікальних тегів"""
        tags = set()
        for note in self.notes:
            tags.update(note.tags)
        return sorted(tags)

    def sort_by_tags(self, tag=None):
        """Сортування нотаток за тегами"""
        if tag:
            # Сортування: спочатку нотатки з вказаним тегом
            tag_lower = tag.lower()
            return sorted(
                enumerate(self.notes),
                key=lambda x: (tag_lower not in x[1].tags, x[1].updated_at),
                reverse=True
            )
        else:
            # Сортування за кількістю тегів
            return sorted(
                enumerate(self.notes),
                key=lambda x: len(x[1].tags),
                reverse=True
            )

    def save(self):
        """Збереження нотаток на диск у JSON форматі"""
        notes_list = [note.to_dict() for note in self.notes]
        
        # Атомарне збереження через тимчасовий файл
        temp_file = self.data_file.with_suffix('.tmp')
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(notes_list, f, ensure_ascii=False, indent=2)
            
            # Атомарна заміна
            temp_file.replace(self.data_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise e

    def load(self):
        """Завантаження нотаток з диска"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    notes_list = json.load(f)
                
                self.notes.clear()
                for note_data in notes_list:
                    note = Note.from_dict(note_data)
                    self.notes.append(note)
            except json.JSONDecodeError as e:
                print(f"⚠️  Помилка читання файлу даних: {e}")
                print("Створюється новий блокнот")
                self.notes.clear()
