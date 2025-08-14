from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from core.config import settings
from core.logger_utils import get_logger

logger = get_logger(__file__)


class MongoDatabaseConnector:
    """Singleton class to connect to MongoDB database."""

    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                # 添加directConnection=True参数
                # cls._instance = MongoClient(settings.MONGO_DATABASE_HOST, directConnection=True)
                # logger.info(
                #     f"Connection to database with uri: {settings.MONGO_DATABASE_HOST} successful"
                # )
                # 移除directConnection=True参数
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
                logger.info(
                    f"Connection to database with uri: {settings.MONGO_DATABASE_HOST} successful"
                )
            except ConnectionFailure:
                logger.error(f"Couldn't connect to the database.")

                raise

        return cls._instance

    @classmethod
    def reset_connection(cls):
        """Reset the database connection with updated settings."""
        if cls._instance:
            cls._instance.close()
            logger.info("Database connection closed.")
        cls._instance = None
        return cls()

    def get_database(self):
        assert self._instance, "Database connection not initialized"

        return self._instance[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._instance:
            self._instance.close()
            logger.info("Connected to database has been closed.")


# 移除模块级别的实例创建
# connection = MongoDatabaseConnector()
