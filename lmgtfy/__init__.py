from .lmgtfy import LMGTFY

def setup(bot):
    bot.add_cog(LMGTFY(bot))
