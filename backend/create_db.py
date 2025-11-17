
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Topic, User

# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    print("❌ ERROR: SUPABASE_DB_URL is not in .env file")
    exit(1)

# ============================================================================
# Database Setup
# ============================================================================
engine = create_engine(SUPABASE_DB_URL)
SessionLocal = sessionmaker(bind=engine)

# ============================================================================
# Create Tables
# ============================================================================
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Insert users
        users_data = [
            {"first_name": "John", "email": "john@test.com"},
            {"first_name": "Jane", "email": "jane@test.com"}
        ]
        for user_data in users_data:
            if not db.query(User).filter(User.email == user_data["email"]).first():
                db.add(User(**user_data))
        db.commit()

        # Get users for topic seeding
        john = db.query(User).filter(User.first_name == "John").first()
        jane = db.query(User).filter(User.first_name == "Jane").first()

        # Insert initial topics for John
        initial_topics = ["learning", "surfing", "parenting", "arts", "productivity", "relationships", "health"]
        for topic_name in initial_topics:
            if not db.query(Topic).filter(Topic.name == topic_name, Topic.user_id == john.id).first():
                db.add(Topic(name=topic_name, user_id=john.id))

        # Insert initial topics for Jane
        for topic_name in initial_topics:
            if not db.query(Topic).filter(Topic.name == topic_name, Topic.user_id == jane.id).first():
                db.add(Topic(name=topic_name, user_id=jane.id))

        db.commit()
        print("✅ Tables created, users and topics seeded successfully!")
    finally:
        db.close()
