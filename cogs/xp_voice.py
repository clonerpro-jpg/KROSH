import disnake
from disnake.ext import commands, tasks
import sqlite3

class VoiceXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_loop.start()

    def add_xp_coins(self, user_id, guild_id, xp_gain=5, coins_gain=2):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, guild_id, xp, coins)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, guild_id)
            DO UPDATE SET
                xp = xp + excluded.xp,
                coins = coins + excluded.coins
        """, (user_id, guild_id, xp_gain, coins_gain))
        conn.commit()
        conn.close()

    @tasks.loop(seconds=30)
    async def voice_loop(self):
        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if member.bot:
                        continue
                    self.add_xp_coins(member.id, guild.id, xp_gain=5, coins_gain=2)

    @voice_loop.before_loop
    async def before_voice_loop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(VoiceXP(bot))