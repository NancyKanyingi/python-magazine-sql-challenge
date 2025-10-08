from .database_utils import get_connection
from .author import Author
from .magazine import Magazine


class Article:
    def __init__(self, title: str, content: str, author: Author | int, magazine: Magazine | int, id: int | None = None):
        self.title = title
        self.content = content
        self._author = author  # can be an Author object or ID
        self._magazine = magazine  # can be a Magazine object or ID
        self.id = id

    # ---- Properties ----
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def author(self):
        if self._author is None:
            return None
        if isinstance(self._author, Author):
            return self._author
        # assume it's an ID
        self._author = Author.find_by_id(self._author)
        return self._author

    @property
    def magazine(self):
        if self._magazine is None:
            return None
        if isinstance(self._magazine, Magazine):
            return self._magazine
        self._magazine = Magazine.find_by_id(self._magazine)
        return self._magazine

    # ---- Database methods ----
    @classmethod
    def new_from_db(cls, row):
        if row is None:
            return None
        return cls(
            title=row["title"],
            content=row["content"],
            author=row["author_id"],
            magazine=row["magazine_id"],
            id=row["id"],
        )

    @classmethod
    def find_by_id(cls, id_):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE id = ?", (id_,))
            row = cur.fetchone()
            return cls.new_from_db(row)
        finally:
            conn.close()

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()

            author_id = getattr(self.author, "id", None) if self.author else None
            magazine_id = getattr(self.magazine, "id", None) if self.magazine else None

            if author_id is None or magazine_id is None:
                raise ValueError("Article must have an author and a magazine with saved IDs before saving")

            if getattr(self, "id", None) is None:
                cur.execute(
                    "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                    (self._title, self.content, author_id, magazine_id),
                )
                self.id = cur.lastrowid
            else:
                cur.execute(
                    """
                    UPDATE articles
                    SET title = ?, content = ?, author_id = ?, magazine_id = ?, updated_at = datetime('now')
                    WHERE id = ?
                    """,
                    (self._title, self.content, author_id, magazine_id, self.id),
                )

            conn.commit()
        finally:
            conn.close()
