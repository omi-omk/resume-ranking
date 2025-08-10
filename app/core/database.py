from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    return db.database

async def init_db():
    """Initialize database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client.get_default_database()
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def create_indexes():
    """Create database indexes"""
    try:
        # Create indexes for better performance
        await db.database.candidates.create_index("email")
        await db.database.candidates.create_index("created_at")
        await db.database.jobs.create_index("job_name")
        await db.database.jobs.create_index("created_at")
        await db.database.matching.create_index([("candidate_id", 1), ("job_id", 1)])
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")

async def close_db():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Database connection closed")