import disnake
from disnake.ext import commands
import sqlite3

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Начисление XP и коинов (без ошибок)
    def add_xp_coins(self, user_id, guild_id, xp_gain=5, coins_gain=3):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, guild_id, xp, coins)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, guild_id)
            DO UPDATE SET
                xp = xp + excluded.xp,
                coins = coins + excluded.coins
        """, (user_id, guild_id, xp_gain, coins_gain))
        conn.commit()
        conn.close()

    # Начисление при сообщении
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or not message.guild:
            return

        guild_id = message.guild.id
        channel_id = message.channel.id

        # Проверяем разрешённые каналы
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM xp_channels WHERE guild_id=? AND channel_id=?", (guild_id, channel_id))
        allowed = c.fetchone()
        conn.close()

        if not allowed:
            return  # канал не разрешён

        # начисляем XP и Coins
        self.add_xp_coins(message.author.id, guild_id)

    # Команда: включить начисление XP и коинов в этом канале
    @commands.slash_command(description="Включить начисление XP и коинов в этом канале")
    @commands.has_permissions(administrator=True)
    async def enable_xp(self, inter):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO xp_channels (guild_id, channel_id) VALUES (?, ?)",
                  (inter.guild.id, inter.channel.id))
        conn.commit()
        conn.close()
        await inter.response.send_message("В этом канале теперь начисляются XP и коины!", ephemeral=True)

    # Команда: выключить начисление XP и коинов в этом канале
    @commands.slash_command(description="Выключить начисление XP и коинов в этом канале")
    @commands.has_permissions(administrator=True)
    async def disable_xp(self, inter):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM xp_channels WHERE guild_id=? AND channel_id=?", (inter.guild.id, inter.channel.id))
        conn.commit()
        conn.close()
        await inter.response.send_message("XP и коины больше не начисляются в этом канале.", ephemeral=True)

def setup(bot):
    bot.add_cog(XP(bot))