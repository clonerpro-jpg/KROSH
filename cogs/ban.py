import disnake
from disnake.ext import commands
import datetime

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ban", description="Забанить пользователя на время")
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(..., description="Кого забанить"),
        days: int = commands.Param(..., description="Длительность (в днях)"),
        reason: str = commands.Param(..., description="Причина бана")
    ):
        if not inter.author.guild_permissions.ban_members:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return

        try:
            embed_dm = disnake.Embed(title="Наказание: BAN", color=disnake.Color.dark_red())
            embed_dm.add_field(name="Длительность", value=f"{days} дней", inline=False)
            embed_dm.add_field(name="Причина", value=reason, inline=False)
            embed_dm.add_field(name="Модератор", value=inter.author.mention, inline=False)
            embed_dm.add_field(name="Решение", value="Если вы не согласны с решением модератора, обратитесь к ЗГА. @kutuzovgraf", inline=False)
            try:
                await member.send(embed=embed_dm)
            except:
                pass

            await member.ban(reason=reason, delete_message_days=0)
            await inter.response.send_message(f"{member.mention} забанен на {days} дней.", ephemeral=False)

        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(BanCog(bot))