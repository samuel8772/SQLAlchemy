import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def test_can_create_magazine():
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()
    assert magazine.id is not None

def test_magazine_articles_and_contributors():
    magazine = Magazine.find_by_name("Tech Today")
    articles = magazine.articles()
    contributors = magazine.contributors()

    assert isinstance(articles, list)
    assert all(isinstance(article, Article) for article in articles)

    assert isinstance(contributors, list)
    assert all(isinstance(contributor, Author) for contributor in contributors)

    assert len(articles) > 0
    assert len(contributors) > 0

def test_contributing_authors_filter():
    magazine = Magazine.find_by_name("Tech Today")
    top_authors = magazine.contributing_authors()

    assert isinstance(top_authors, list)
    assert all(isinstance(author, Author) for author in top_authors)

    for author in top_authors:
        assert len(author.articles()) > 2