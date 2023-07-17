import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    """
    Shutdown Command:
        Params:
            - context: required parameter
        Description: Logsout the bot 
    """
    @commands.is_owner()
    @commands.command(name = "shutdown")
    async def shutdown(self, context):
        await context.send("Signin off...")
        await context.bot.logout()

async def setup(bot):
    await bot.add_cog(Admin(bot))
