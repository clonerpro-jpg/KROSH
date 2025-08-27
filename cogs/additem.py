import disnake
from disnake.ext import commands
import sqlite3

class Additem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_admin(self, inter: disnake.ApplicationCommandInteraction):
        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return False
        return True

    @commands.slash_command(description="Добавить товар в магазин")
    async def additem(
        self,
        inter: disnake.ApplicationCommandInteraction,
        item_id: str,
        name: str,
        price: int,
        type: str,
        role: disnake.Role = None
    ):
        if not await self.check_admin(inter):
            return

        if role and role.permissions.administrator:
            await inter.response.send_message("Нельзя добавить админскую роль в магазин", ephemeral=True)
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO shop_items (item_id, name, price, type, role_id)
            VALUES (?, ?, ?, ?, ?)
        """, (item_id, name, price, type, role.id if role else None))
        conn.commit()
        conn.close()

        await inter.response.send_message(f"Товар '{name}' добавлен в магазин", ephemeral=True)

    @commands.slash_command(description="Удалить товар из магазина")
    async def removeitem(self, inter: disnake.ApplicationCommandInteraction, item_id: str):
        if not await self.check_admin(inter):
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM shop_items WHERE item_id=?", (item_id,))
        if c.rowcount == 0:
            await inter.response.send_message(f"Товар с ID '{item_id}' не найден", ephemeral=True)
        else:
            await inter.response.send_message(f"Товар с ID '{item_id}' удалён", ephemeral=True)
        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(Additem(bot))