import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def test_can_create_article():
    author = Author("Test Writer")
    author.save()
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()

    article = Article("AI is Here", author.id, magazine.id)
    article.save()

    assert article.id is not None

def test_article_links_to_author_and_magazine():
    author = Author("Test Writer")
    author.save()
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()
    article = Article("AI is Here", author.id, magazine.id)
    article.save()

    found_article = Article.find_by_title("AI is Here")
    assert found_article is not None

    assert found_article.author().name == "Test Writer"
    assert found_article.magazine().name == "Tech Today"