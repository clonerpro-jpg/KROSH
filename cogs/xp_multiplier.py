import disnake
from disnake.ext import commands
import sqlite3

class Multiplier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, inter: disnake.ApplicationCommandInteraction):
        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return False
        return True

    @commands.slash_command(description="Установить множитель XP и коинов на сервере")
    async def set_multiplier(self, inter: disnake.ApplicationCommandInteraction, xp: float = 1.0, coins: float = 1.0):
        if not await self.check_admin(inter):
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO guilds (guild_id, xp_multiplier, coins_multiplier)
            VALUES (?, ?, ?)
        """, (inter.guild.id, xp, coins))
        conn.commit()
        conn.close()
        await inter.response.send_message(f"Множители установлены: XP x{xp}, Coins x{coins}", ephemeral=True)

def setup(bot):
    bot.add_cog(Multiplier(bot))