import discord
from discord.ext import commands
from discord import ui, Interaction
import Discord.logic as logic

class CareerChoiceView(ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        for option in logic.get_career_options():
            self.add_item(CareerButton(option[0], user_id))

class CareerButton(ui.Button):
    def __init__(self, label, user_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.career_choice = label
        self.user_id = user_id

    async def callback(self, interaction: Interaction):
        logic.update_career_choice(str(interaction.user.id), self.career_choice)
        await interaction.response.send_message(
            f"{interaction.user.mention}, your career choice '{self.career_choice}' has been updated!", ephemeral=True
        )

def register_commands(bot):

    @bot.command(name='register')
    async def register(ctx):
        logic.add_user(str(ctx.author.id), ctx.author.name)
        await ctx.send(f'{ctx.author.mention}, your registration is complete!')
        view = CareerChoiceView(ctx.author.id)
        await ctx.send("Please choose a career:", view=view)

    @bot.command(name='choose')
    async def choose(ctx, *, career_choice):
        logic.update_career_choice(str(ctx.author.id), career_choice)
        await ctx.send(f'{ctx.author.mention}, your career has been saved as {career_choice}!')

    @bot.command(name='careers')
    async def careers(ctx):
        options = logic.get_career_options()
        text = '\n'.join([opt[0] for opt in options])
        await ctx.send(f'Available careers:\n{text}')

    @bot.command(name='response')
    async def response(ctx, *, responses):
        logic.save_user_responses(str(ctx.author.id), responses)
        await ctx.send(f'{ctx.author.mention}, your responses have been saved!')

    @bot.command(name='choosebutton')
    async def choosebutton(ctx):
        view = CareerChoiceView(ctx.author.id)
        await ctx.send("Please choose a career:", view=view)

    @bot.command(name='dmc_help')
    async def dmc_help(ctx):
        await ctx.send(
            "Welcome to Drive My Career Bot!\n"
            "Use `/career` to get personalized career suggestions based on your expertise or degrees.\n"
            "You can interact with me using messages and buttons.\n"
            "Use `/careers` to see all available career options.\n"
            "Use `/register` to register yourself.\n"
            "Use `/choose <career>` to save your career choice.\n"
            "Use `/response <your answers>` to save your responses."
        )