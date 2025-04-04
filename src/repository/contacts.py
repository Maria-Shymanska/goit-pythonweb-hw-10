from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, or_, func, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactBase


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self, skip: int, limit: int, user: User, q: str | None = None
    ) -> Sequence[Contact]:
        query = select(Contact).filter_by(user=user)
        if q is not None:
            q = f"%{q.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Contact.first_name).like(q),
                    func.lower(Contact.last_name).like(q),
                    Contact.phone.like(q),
                )
            )
        query = query.offset(skip).limit(limit)
        contacts = await self.db.execute(query)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact:
        query = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id, user)

    async def update_contact(
        self, contact_id: int, body: ContactBase, user: User
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)
            return contact

    async def birthday_reminder(self, user: User) -> Sequence[Contact]:
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        query = (
            select(Contact)
            .filter_by(user=user)
            .where(
                or_(
                    # Dates in the same month
                    and_(
                        (extract("month", Contact.birth_date) == start_date.month),
                        (extract("day", Contact.birth_date) >= start_date.day),
                        (
                            extract("day", Contact.birth_date)
                            <= (
                                end_date.day
                                if end_date.month == start_date.month
                                else 31
                            )
                        ),
                    ),
                    # Date in the next month
                    and_(
                        (extract("month", Contact.birth_date) == end_date.month),
                        (extract("day", Contact.birth_date) <= end_date.day),
                        (start_date.month != end_date.month),
                    ),
                )
            )
        )
        contacts = await self.db.execute(query)
        return contacts.scalars().all()