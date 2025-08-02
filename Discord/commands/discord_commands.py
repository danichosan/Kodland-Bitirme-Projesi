from discord.ext import commands
import logic

# Command registration function
def register_commands(bot):

    @bot.command(name='careers')
    async def careers(ctx):
        options = logic.get_career_options()
        options_list = '\n'.join([option[0] for option in options])
        await ctx.send(f'Available career options:\n{options_list}')

    @bot.command(name='choose')
    async def choose(ctx, *, career_choice):
        logic.update_career_choice(str(ctx.author.id), career_choice)
        await ctx.send(f'{ctx.author.mention}, your career choice has been updated to {career_choice}!')

    @bot.command(name='register')
    async def register(ctx):
        logic.add_user(str(ctx.author.id), ctx.author.name)
        await ctx.send(f'{ctx.author.mention}, your registration is complete!')
