from config import CHANNEL_ID, bot, logger, SUBSCRIPTION_STATUSES


async def check_subscription(user_id: int) -> bool:
    """ Проверяет подписку пользователя на канал
    :param user_id:
    :return:
    """
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in SUBSCRIPTION_STATUSES
    except Exception as e:
        logger.warning(f"[check_subscription] error for user: {user_id} ({e})")
        return False
