import asyncpg
import os


DATABASE_URL = os.getenv("DATABASE_URL")  # Храним в переменной окружения


async def create_pool():
    """Создает пул подключений к БД"""
    return await asyncpg.create_pool(DATABASE_URL)


async def save_post(user_id, username, post_id, gift_data, pool):
    """Сохраняет пост в базу данных"""
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO posts (user_id, username, post_id, gift_name, gift_model, gift_background, gift_color, gift_pattern, price)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
            user_id, username, post_id, gift_data["gift_name"], gift_data["gift_model"],
            gift_data["gift_background"], gift_data["gift_color"], gift_data["gift_pattern"],
            gift_data["price"]
        )


async def get_post(user_id, pool):
    """Получает пост пользователя по user_id"""
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM posts WHERE user_id = $1", user_id)


async def update_post(user_id, new_text, pool):
    """Обновляет текст поста"""
    async with pool.acquire() as conn:
        await conn.execute("UPDATE posts SET gift_name = $1 WHERE user_id = $2", new_text, user_id)


async def delete_post(user_id, pool):
    """Удаляет пост"""
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM posts WHERE user_id = $1", user_id)
