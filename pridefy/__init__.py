from redbot.core import data_manager
from .pridefy import Pridefy

def setup(bot):
    data_manager.load_bundled_data(cog, __file__)
    bot.add_cog(Pridefy(bot))
