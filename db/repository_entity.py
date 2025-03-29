from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Gift


class BaseEntity:
    def __init__(self, session: AsyncSession):
        self.session = session


class GiftEntity(BaseEntity):
    async def save_gift(self, gift_data: dict):
        """ Сохраняем подарок в БД
        :param gift_data:
        :return:
        """
        gift = Gift(**gift_data)
        self.session.add(gift)
        await self.session.commit()
        await self.session.refresh(gift)
        return gift

    async def get_gifts_by_user(self, user_id: int):
        """ Получаем подарки пользователя
        :param user_id:
        :return:
        """
        result = await self.session.execute(select(Gift).where(Gift.user_id == user_id))
        return result.scalars().first()

    async def get_filtered_gifts(self, gift_name, gift_model, gift_background, gift_pattern, gift_number):
        """ Получаем список подарков, отфильтрованных по параметрам
        """
        query = select(Gift).order_by(Gift.price)
        if gift_name:
            query = query.where(Gift.gift_name.ilike(f"%{gift_name}%"))
        if gift_model:
            query = query.where(Gift.gift_model.ilike(f"%{gift_model}%"))
        if gift_background:
            query = query.where(Gift.gift_background.ilike(f"%{gift_background}%"))
        if gift_pattern:
            query = query.where(Gift.gift_pattern.ilike(f"%{gift_pattern}%"))
        if gift_number:
            query = query.where(Gift.gift_number == gift_number)

        result = await self.session.execute(query)
        gifts = result.scalars().all()

        return gifts

    async def get_average_price(self, gift_name, gift_model, gift_background, gift_pattern, gift_number):
        """ Получаем среднюю цену подарка по схожим параметрам """
        query = select(func.avg(Gift.price))

        if gift_name:
            query = query.where(Gift.gift_name.ilike(f"%{gift_name}%"))
        if gift_model:
            query = query.where(Gift.gift_model.ilike(f"%{gift_model}%"))
        if gift_background:
            query = query.where(Gift.gift_background.ilike(f"%{gift_background}%"))
        if gift_pattern:
            query = query.where(Gift.gift_pattern.ilike(f"%{gift_pattern}%"))
        if gift_number:
            query = query.where(Gift.gift_number == gift_number)

        result = await self.session.execute(query)
        avg_price = result.scalar()

        return avg_price or 0
