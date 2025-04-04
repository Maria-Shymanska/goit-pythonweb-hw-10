from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.repository.contacts import ContactRepository
from src.schemas import ContactBase


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(
        self, skip: int, limit: int, user: User, q: str | None = None
    ) -> Sequence[Contact]:
        return await self.contact_repository.get_contacts(skip, limit, user, q)

    async def get_contact(self, contact_id: int, user: User) -> Contact:
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def remove_contact_by_id(self, contact_id: int, user: User) -> Contact:
        return await self.contact_repository.remove_contact(contact_id, user)

    async def update_contact(
        self, contact_id: int, body: ContactBase, user: User
    ) -> Contact | None:
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def birthday_reminder(self, user: User) -> Sequence[Contact]:
        return await self.contact_repository.birthday_reminder(user)