import disnake
from disnake.ext import commands

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick", description="Кикнуть пользователя")
    async def kick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(..., description="Кого кикнуть"),
        reason: str = commands.Param(..., description="Причина кика")
    ):
        if not inter.author.guild_permissions.kick_members:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return

        try:
            embed_dm = disnake.Embed(title="Наказание: KICK", color=disnake.Color.red())
            embed_dm.add_field(name="Причина", value=reason, inline=False)
            embed_dm.add_field(name="Модератор", value=inter.author.mention, inline=False)
            embed_dm.add_field(name="Решение", value="Если вы не согласны с решением модератора, обратитесь к ЗГА. @kutuzovgraf", inline=False)
            try:
                await member.send(embed=embed_dm)
            except:
                pass

            await member.kick(reason=reason)
            await inter.response.send_message(f"{member.mention} был кикнут.", ephemeral=False)

        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(KickCog(bot))