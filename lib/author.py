from .database_utils import get_connection

class Author:
    def __init__(self, name, id=None):
        if len(name.strip()) == 0:
            raise ValueError("Author name cannot be empty")
        self._name = name
        self.id = id

    @classmethod
    def new_from_db(cls, row):
        if row is None:
            return None
        return cls(name=row["name"], id=row["id"])

    @classmethod
    def find_by_id(cls, id_):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM authors WHERE id = ?", (id_,))
            row = cur.fetchone()
            return cls.new_from_db(row)
        finally:
            conn.close()

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            if getattr(self, "id", None) is None:
                cur.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
                self.id = cur.lastrowid
            else:
                cur.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self.id))
            conn.commit()
        finally:
            conn.close()

    def articles(self):
        # import lazily to avoid circular import
        from .article import Article

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            rows = cur.fetchall()
            return [Article.new_from_db(r) for r in rows]
        finally:
            conn.close()

    def magazines(self):
        # distinct magazines this author has articles in
        from .magazine import Magazine

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT DISTINCT m.* FROM magazines m
                INNER JOIN articles a ON a.magazine_id = m.id
                WHERE a.author_id = ?
                """,
                (self.id,),
            )
            rows = cur.fetchall()
            return [Magazine.new_from_db(r) for r in rows]
        finally:
            conn.close()
