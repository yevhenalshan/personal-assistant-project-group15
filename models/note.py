from datetime import datetime

class Note:
    def __init__(self, text: str, tags: list[str] = None):
        self.text = text
        self.tags = tags or []
        self.created_at = datetime.now()

    def __str__(self):
        tags_str = f" [tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"{self.text}{tags_str} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M')})"

