import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

class PM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pm", description="Отправить личное сообщение пользователю")
    @commands.has_permissions(administrator=True)
    async def pm(self, inter: ApplicationCommandInteraction, user: disnake.Member, *, message: str):
        try:
            embed = disnake.Embed(
                title="Личное Сообщение",
                description=message,
                color=disnake.Color.blurple()
            )
            embed.set_footer(text=f"Отправитель: {inter.author}")
            await user.send(embed=embed)
            await inter.response.send_message(f"Сообщение отправлено {user.mention}", ephemeral=True)
        except:
            await inter.response.send_message(f"Не удалось отправить сообщение.", ephemeral=True)

def setup(bot):
    bot.add_cog(PM(bot))