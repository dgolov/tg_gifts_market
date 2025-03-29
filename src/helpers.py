from config import CHANNEL_ID, bot, logger, SUBSCRIPTION_STATUSES
from db.models import Gift
from typing import List

import re


async def check_subscription(user_id: int) -> bool:
    """ Проверяет подписку пользователя на канал
    :param user_id:
    :return:
    """
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in SUBSCRIPTION_STATUSES
    except Exception as e:
        logger.warning(f"[helpers.check_subscription] error for user: {user_id} ({e})")
        return False


def escape_markdown(text: str) -> str:
    """Экранирует специальные символы для корректного отображения в MarkdownV2.
    """
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


def prepare_gift_list_message(gifts: List[Gift], average: int) -> str:
    """ Формирует сообщение со списком доступных подарков
    """
    logger.debug("[helpers] prepare gift list message")
    response = "Список доступных подарков:\n\n"

    for gift in gifts:
        price_status = "🟢🟢🟢" if gift.price <= average * 0.8 else \
                       "🟢" if gift.price <= average else \
                       "🟡" if gift.price <= average * 1.2 else \
                       "🔴" if gift.price <= average * 1.4 else \
                       "🔴🔴🔴"

        response += f"🎁 *{escape_markdown(gift.gift_name)}* - {price_status}\n"
        response += f"📦 Модель: {escape_markdown(gift.gift_model or '-')}\n"
        response += f"🖼 Фон: {escape_markdown(gift.gift_background or '-')}\n"
        response += f"🎨 Узоры: {escape_markdown(gift.gift_pattern or '-')}\n"
        response += f"💰 Цена: {escape_markdown(gift.price)} TON\n\n"

        if gift.post_id:
            gift_link = f"https://t.me/{CHANNEL_ID.replace('@', '')}/{gift.post_id}"
            response += f"🔗 [Ссылка на подарок]({escape_markdown(gift_link)})\n\n"

    return response
