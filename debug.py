from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

def demo():
    create_tables()
    a = Author(name="Nancy Kanyingi")
    a.save()

    m = Magazine(name="Current Affairs", category="Politics")
    m.save()

    art = Article(
        title="The Youth Movement",
        content="This is an article about ...",
        author=a,
        magazine=m
    )
    art.save()

    print("Author ID:", a.id)
    print("Magazine ID:", m.id)
    print("Article ID:", art.id)

if __name__ == "__main__":
    demo()
