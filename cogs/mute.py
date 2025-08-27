import disnake
from disnake.ext import commands
from disnake import Option, OptionType
import asyncio

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="mute", description="Замутить пользователя")
    async def mute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(..., description="Кого замутить"),
        duration: str = commands.Param(..., description="Длительность (например: 10m, 1h)"),
        reason: str = commands.Param(..., description="Причина мута")
    ):
        if not inter.author.guild_permissions.moderate_members:
            await inter.response.send_message("Отсутствуют права администратора", ephemeral=True)
            return

        # перевод в минуты
        time_multipliers = {"m": 60, "h": 3600, "d": 86400}
        seconds = int(duration[:-1]) * time_multipliers[duration[-1]]

        try:
            await member.timeout(duration=disnake.utils.utcnow() + disnake.utils.timedelta(seconds=seconds), reason=reason)

            # ЛС пользователю
            embed_dm = disnake.Embed(title="Наказание: MUTE", color=disnake.Color.orange())
            embed_dm.add_field(name="Длительность", value=duration, inline=False)
            embed_dm.add_field(name="Причина", value=reason, inline=False)
            embed_dm.add_field(name="Модератор", value=inter.author.mention, inline=False)
            embed_dm.add_field(name="Решение", value="Если вы не согласны с решением модератора, обратитесь к ЗГА. @kutuzovgraf", inline=False)
            try:
                await member.send(embed=embed_dm)
            except:
                pass

            # Ответ в чат
            await inter.response.send_message(f"{member.mention} получил мут на {duration}.", ephemeral=True)

        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(MuteCog(bot))