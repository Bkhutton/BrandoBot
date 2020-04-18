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
    @commands.command(name = "shutdown")
    async def shutdown(self, context):
        if commands.is_owner():
            await context.bot.logout()
        else:
            await context.send("No permission!")

def setup(bot):
    bot.add_cog(Admin(bot))