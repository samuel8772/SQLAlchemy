from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        self.id = cursor.lastrowid
        conn.commit()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    def articles(self):
        from lib.models.article import Article  # local import to avoid circular import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        return [Article(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"]) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine  # local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        return [Magazine(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article  # local import
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None