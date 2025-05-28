from lib.models.author import Author
from lib.models.magazine import Magazine

a = Author.create("Test Author")
m = Magazine.create("Python Weekly", "Tech")
a.add_article(m.id, "Why Python is Great")
print(a.magazines())