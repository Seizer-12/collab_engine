from sqlalchemy.orm import Session
from app.models.document import Document, EditLog
from app.schemas.message import EditorMessage


def get_document(db: Session, doc_id: int):
    return db.query(Document).filter(Document.id == doc_id).first()


def create_document(db: Session, title: str):
    db_doc = Document(title=title)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def update_doc_content(db: Session, doc_id: int, content: str, user_id: str):
    # 1. Update the document itself
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        doc.content = content

        # 2. LOg the change in the history table 
        log = EditLog(
            document_id = doc_id,
            user_id = user_id,
            change_data = content
        )
        db.add(log)
        db.commit()
        db.refresh(doc)
    return doc



