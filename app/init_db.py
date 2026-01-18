from app.core.database import engine, Base
from app.models.document import Document, EditLog


def create_tables():
    print("Connecting to PostrgreSQL and creating tables")

    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


if __name__ == "__main__":
    create_tables()


