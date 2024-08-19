# import discord
# from discord import app_commands

# TOKEN = "MTI3NDM5MjU2NTE3NjczMzg1OQ.G9jAo4.V1O9W5YHmH3VIiyTjyVEszYFe07rjMzcvrcmEo"

# intents = discord.Intents.default()  # デフォルトのIntentsを使用
# intents.messages = True
# intents.message_content = True  # メッセージ内容の受信を有効化
# intents.guilds = True  #
# intents.members = True  # メンバー情報を取得するために必要
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)


# @client.event
# async def on_ready():
#     await tree.sync()


# # 全てのインタラクションを取得
# @client.event
# async def on_interaction(inter: discord.Interaction):
#     try:
#         if inter.data["component_type"] == 2:
#             await on_button_click(inter)
#     except KeyError:
#         pass


# ## Buttonの処理
# async def on_button_click(inter: discord.Interaction):
#     custom_id = inter.data["custom_id"]
#     if custom_id == "check":
#         embed = discord.Embed(title="あなたのユーザー名", description=inter.user.name + "#" + inter.user.discriminator, color=0x0000FF)
#         await inter.response.send_message(embed=embed, ephemeral=True)


# @tree.command(name="username", description="自分のユーザー名を確認")
# async def username(interaction: discord.Interaction):
#     button = discord.ui.Button(label="確認", style=discord.ButtonStyle.primary, custom_id="check")
#     view = discord.ui.View()
#     view.add_item(button)
#     await interaction.response.send_message("自分のユーザー名を確認してみましょう。", view=view)


# client.run(TOKEN)


import discord
from discord import app_commands

TOKEN = "MTI3NDM5MjU2NTE3NjczMzg1OQ.GFxivW.AwNLmQRFcisK00139g1gdfIJCI1Wk50hAjbYoI"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # メッセージ内容の受信を有効化
intents.guilds = True  #
intents.members = True  # メンバー情報を取得するために必要

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        await tree.sync()
        print("Commands have been synced.")
    except Exception as e:
        print(f"An error occurred during command syncing: {e}")


@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        await on_button_click(interaction)


async def on_button_click(interaction: discord.Interaction):
    custom_id = interaction.data.get("custom_id")
    if custom_id == "check":
        embed = discord.Embed(title="あなたのユーザー名", description=f"{interaction.user.name}#{interaction.user.discriminator}", color=0x0000FF)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("Unknown button interaction.", ephemeral=True)


@tree.command(name="username", description="自分のユーザー名を確認")
async def username(interaction: discord.Interaction):
    button = discord.ui.Button(label="確認", style=discord.ButtonStyle.primary, custom_id="check")
    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message("自分のユーザー名を確認してみましょう。", view=view)


client.run(TOKEN)
