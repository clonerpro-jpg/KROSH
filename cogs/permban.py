import disnake
from disnake.ext import commands

class PermBanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="permban", description="Перманентный бан")
    async def permban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(..., description="Кого забанить"),
        reason: str = commands.Param(..., description="Причина")
    ):
        if not inter.author.guild_permissions.ban_members:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return

        try:
            embed_dm = disnake.Embed(title="Наказание: PERMABAN", color=disnake.Color.black())
            embed_dm.add_field(name="Причина", value=reason, inline=False)
            embed_dm.add_field(name="Модератор", value=inter.author.mention, inline=False)
            embed_dm.add_field(name="Решение", value="Если вы не согласны с решением модератора, обратитесь к ЗГА. @kutuzovgraf", inline=False)
            try:
                await member.send(embed=embed_dm)
            except:
                pass

            await member.ban(reason=reason, delete_message_days=0)
            await inter.response.send_message(f"{member.mention} получил перманентный бан.", ephemeral=False)

        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(PermBanCog(bot))