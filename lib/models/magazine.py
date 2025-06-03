from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = cursor.lastrowid
        conn.commit()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], name=row["name"], category=row["category"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], name=row["name"], category=row["category"])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        return [cls(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

    def contributors(self):
        from lib.models.author import Author  # local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return [Author(id=row["id"], name=row["name"]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author  # local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        return [Author(id=row["id"], name=row["name"]) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """)
        rows = cursor.fetchall()
        return [cls(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as article_count FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "article_count": row["article_count"]
            }
            for row in rows
        ]

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [Article(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"]) for row in rows]
