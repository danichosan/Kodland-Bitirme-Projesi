from discord.ext import commands
import logic

# Komutları kaydetme fonksiyonu
def register_commands(bot):

    @bot.command(name='kariyer')
    async def kariyer(ctx):
        options = logic.get_career_options()
        options_list = '\n'.join([option[0] for option in options])
        await ctx.send(f'Mevcut kariyer seçenekleri:\n{options_list}')

    @bot.command(name='sec')
    async def sec(ctx, *, career_choice):
        logic.update_career_choice(str(ctx.author.id), career_choice)
        await ctx.send(f'{ctx.author.mention}, kariyer seçiminiz {career_choice} olarak güncellendi!')

    @bot.command(name='kayit')
    async def kayit(ctx):
        logic.add_user(str(ctx.author.id), ctx.author.name)
        await ctx.send(f'{ctx.author.mention}, kayıt işleminiz tamamlandı!')
