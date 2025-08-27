import disnake
from disnake.ext import commands
import sqlite3

class Coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, inter: disnake.ApplicationCommandInteraction):
        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return False
        return True

    @commands.slash_command(description="Добавить коины пользователю")
    async def addcoins(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, amount: int):
        if not await self.check_admin(inter):
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, guild_id, coins, xp) 
            VALUES (?, ?, 0, 0) ON CONFLICT(user_id, guild_id) DO NOTHING
        """, (member.id, inter.guild.id))
        c.execute("UPDATE users SET coins = coins + ? WHERE user_id=? AND guild_id=?", (amount, member.id, inter.guild.id))
        conn.commit()
        conn.close()
        await inter.response.send_message(f"Добавлено {amount} коинов пользователю {member.display_name}", ephemeral=True)

    @commands.slash_command(description="Отнять коины у пользователя")
    async def removecoins(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, amount: int):
        if not await self.check_admin(inter):
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, guild_id, coins, xp) 
            VALUES (?, ?, 0, 0) ON CONFLICT(user_id, guild_id) DO NOTHING
        """, (member.id, inter.guild.id))
        c.execute("UPDATE users SET coins = coins - ? WHERE user_id=? AND guild_id=?", (amount, member.id, inter.guild.id))
        conn.commit()
        conn.close()
        await inter.response.send_message(f"Отнято {amount} коинов у пользователя {member.display_name}", ephemeral=True)

def setup(bot):
    bot.add_cog(Coins(bot))