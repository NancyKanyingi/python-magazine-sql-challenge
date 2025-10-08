from .database_utils import get_connection


class Magazine:
    def __init__(self, name: str, category: str | None = None, id: int | None = None):
        self.name = name  # use setter validation
        self.category = category
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Magazine name must be a string")
        if len(value.strip()) == 0:
            raise ValueError("Magazine name cannot be empty")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Magazine category must be a string or None")
        self._category = value

    @classmethod
    def new_from_db(cls, row):
        if row is None:
            return None
        return cls(name=row["name"], category=row["category"], id=row["id"])

    @classmethod
    def find_by_id(cls, id_):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM magazines WHERE id = ?", (id_,))
            row = cur.fetchone()
            return cls.new_from_db(row)
        finally:
            conn.close()

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            if self.id is None:
                cur.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self._name, self._category),
                )
                self.id = cur.lastrowid
            else:
                cur.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self._name, self._category, self.id),
                )
            conn.commit()
        finally:
            conn.close()

    def articles(self):
        from .article import Article

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cur.fetchall()
            return [Article.new_from_db(r) for r in rows]
        finally:
            conn.close()
