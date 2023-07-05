import discord
from discord.ext import commands

class Emily(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = "walle")
    async def walle(self, context):
        await context.send("EVAAA!!!")
    
    @commands.command(name = "appy")
    async def appy(self, context):
        await context.send("mew - ^._.^= ∫")

    @commands.command(name = "rawr")
    async def rawr(self, context):
        await context.send("xD rawrmeh ( ^ ᴗ ^ )ε^ )")

async def setup(bot):
    await bot.add_cog(Emily(bot))
