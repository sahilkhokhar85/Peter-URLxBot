from __future__ import annotations

import asyncpg


class UserStore:
    """Tracks users who talk to the bot: last seen time and ban status."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def init(self) -> None:
        await self.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS bot_users (
                user_id BIGINT PRIMARY KEY,
                first_seen TIMESTAMPTZ NOT NULL DEFAULT now(),
                last_seen TIMESTAMPTZ NOT NULL DEFAULT now(),
                banned BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )

    async def touch(self, user_id: int) -> None:
        await self.pool.execute(
            """
            INSERT INTO bot_users (user_id)
            VALUES ($1)
            ON CONFLICT (user_id)
            DO UPDATE SET last_seen = now()
            """,
            user_id,
        )

    async def is_banned(self, user_id: int) -> bool:
        value = await self.pool.fetchval(
            "SELECT banned FROM bot_users WHERE user_id = $1",
            user_id,
        )
        return bool(value)

    async def set_banned(self, user_id: int, banned: bool) -> None:
        await self.pool.execute(
            """
            INSERT INTO bot_users (user_id, banned)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET banned = EXCLUDED.banned
            """,
            user_id,
            banned,
        )

    async def stats(self) -> dict[str, int]:
        row = await self.pool.fetchrow(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE last_seen > now() - interval '24 hours'
                ) AS active,
                COUNT(*) FILTER (WHERE banned) AS banned
            FROM bot_users
            """
        )
        return {
            "total": int(row["total"]),
            "active": int(row["active"]),
            "banned": int(row["banned"]),
        }
