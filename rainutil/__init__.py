from .rainutil import RainUtil

def setup(bot):
    bot.add_cog(RainUtil(bot))