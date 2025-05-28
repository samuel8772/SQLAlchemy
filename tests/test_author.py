import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clear tables before each test to isolate
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    yield
    # No teardown needed, in-memory DB reset at process end

def test_can_create_author():
    author = Author("Jane Doe")
    author.save()
    assert author.id is not None

def test_find_author_by_name():
    author = Author("Jane Doe")
    author.save()
    found = Author.find_by_name("Jane Doe")
    assert found is not None
    assert found.name == "Jane Doe"

def test_author_articles_and_magazines():
    author = Author("Jane Doe")
    author.save()

    mag = Magazine("Tech Today", "Technology")
    mag.save()

    article = Article("My Article", author.id, mag.id)
    article.save()

    articles = author.articles()
    magazines = author.magazines()

    assert len(articles) == 1
    assert len(magazines) == 1