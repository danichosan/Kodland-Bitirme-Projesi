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
        await interaction.response.send_message(f"{interaction.user.mention}, kariyer seçiminiz '{self.career_choice}' olarak güncellendi!", ephemeral=True)

def register_commands(bot):

    @bot.command(name='kayit')
    async def kayit(ctx):
        logic.add_user(str(ctx.author.id), ctx.author.name)
        await ctx.send(f'{ctx.author.mention}, kayıt işleminiz tamamlandı!')
        view = CareerChoiceView(ctx.author.id)
        await ctx.send("Lütfen bir kariyer seçin:", view=view)

    @bot.command(name='sec')
    async def sec(ctx, *, career_choice):
        logic.update_career_choice(str(ctx.author.id), career_choice)
        await ctx.send(f'{ctx.author.mention}, kariyerin {career_choice} olarak kaydedildi!')

    @bot.command(name='kariyer')
    async def kariyer(ctx):
        options = logic.get_career_options()
        text = '\n'.join([opt[0] for opt in options])
        await ctx.send(f'Mevcut kariyerler:\n{text}')

    @bot.command(name='yanit')
    async def yanit(ctx, *, responses):
        logic.save_user_responses(str(ctx.author.id), responses)
        await ctx.send(f'{ctx.author.mention}, yanıtlar kaydedildi!')

    @bot.command(name='secbuton')
    async def secbuton(ctx):
        view = CareerChoiceView(ctx.author.id)
        await ctx.send("Lütfen bir kariyer seçin:", view=view)