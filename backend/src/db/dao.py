from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
