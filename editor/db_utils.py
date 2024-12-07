from pymongo import MongoClient
from datetime import datetime

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")  # Adjust for hosted MongoDB
db = client['collab_text_editor']  # Database name
documents_collection = db['documents']  # Collection for storing documents

def save_document_to_db(doc_id, content, comments):
    """Save or update a document in MongoDB."""
    document = {
        "document_id": doc_id,
        "content": content,
        "comments": comments,
        "updated_at": datetime.utcnow(),
    }
    # Insert or update the document
    documents_collection.update_one(
        {"document_id": doc_id},
        {"$set": document},
        upsert=True  # Insert if not already present
    )

def fetch_document_from_db(doc_id):
    """Retrieve a document from MongoDB by its ID."""
    return documents_collection.find_one({"document_id": doc_id})
