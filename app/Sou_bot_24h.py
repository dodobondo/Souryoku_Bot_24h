# 総力戦専用サーバのBot作成

import text
from server import server_thread

import discord
from discord import app_commands

import asyncio
import time

import os
from dotenv import load_dotenv

load_dotenv()

# botのトークン
token = "MTI3NDM5MjU2NTE3NjczMzg1OQ.GnWAv2.zacN5D8mO85j9bL0EFeEuEjWyHOKBi-VT3DNlk"
id_sys = 1274370445810077761  # チャンネルリンクの一番最後のスラッシュ以降
id_gm = 1274370445810077762
id_talk = 1274370445810077758
id_step1 = 1274370445394575455
id_step2 = 1274370445394575456
id_step3 = 1274370445394575457
id_step4 = 1274370445394575458
id_step5 = 1274370445394575459


intents = discord.Intents.default()  # デフォルトのIntentsを使用
intents.messages = True
intents.message_content = True  # メッセージ内容の受信を有効化
intents.guilds = True  #
intents.members = True  # メンバー情報を取得するために必要

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
key = 0


# ロールを全メンバーに付与する非同期関数
async def give_role(guild, role):
    for member in guild.members:  # サーバー内の全メンバーに対してループ
        if role not in member.roles:  # メンバーが既にロールを持っていない場合
            await member.add_roles(role)  # ロールを付与


# ■ログインの確認
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        await tree.sync()
        print("Commands have been synced.")
    except Exception as e:
        print(f"An error occurred during command syncing: {e}")


@client.event
async def on_disconnect():
    print("Bot has been disconnected")


# Shutdown handling
@client.event
async def on_shutdown():
    await client.close()
    print("Client session closed")


# 全てのインタラクションを取得
@client.event
async def on_interaction(inter: discord.Interaction):
    try:
        if inter.data["component_type"] == 2:
            await on_button_click(inter)
    except KeyError:
        pass


## Buttonの処理
async def on_button_click(inter: discord.Interaction):
    custom_id = inter.data["custom_id"]
    # ここに各ボタンの処理を書いていく
    if custom_id == "add_administrator":
        # 管理者ロールのIDを指定
        role_id = 1274946843415154708

        # ギルドからロールを取得
        guild = inter.guild
        role = guild.get_role(role_id)

        if role is not None:
            # ユーザーが既にロールを持っているか確認
            if role in inter.user.roles:
                # ロールがある場合は削除
                await inter.user.remove_roles(role)
                await inter.response.send_message(f"{role.name} ロールが削除されました。", ephemeral=True)
            else:
                # ロールがない場合は追加
                await inter.user.add_roles(role)
                await inter.response.send_message(f"{role.name} ロールが追加されました。", ephemeral=True)

    elif custom_id == "reset":
        # 応答を遅延させる
        await inter.response.defer(ephemeral=True)

        # 削除するロールのIDを指定（リスト形式）
        role_ids = [
            1274370444811833505,  # オープニング
            1274370444811833504,  # 準備
            1274370444811833503,  # 説明
            1274370444811833502,  # step1
            1274370444811833501,  # step2
            1274370444811833500,  # step3
            1274370444811833499,  # step4
            1274370444811833498,  # step5
            1274370444811833497,  # clear
        ]

        # ギルドからロールを取得して、ユーザーからはく奪
        guild = inter.guild

        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role is not None:
                await inter.user.remove_roles(role)

        # ギルドからロールを取得
        guild = inter.guild

        # 特定のチャンネルのメッセージを削除
        channel = guild.get_channel(id_sys)
        await channel.purge()  # チャンネルのメッセージを全削除
        channel = guild.get_channel(id_gm)
        await channel.purge()  # チャンネルのメッセージを全削除
        channel = guild.get_channel(id_talk)
        await channel.purge()  # チャンネルのメッセージを全削除

        await inter.followup.send("閲覧可能なチャンネルとテキストログを初期状態に戻しました。", ephemeral=True)


@client.event
async def on_message(message):
    global key  # グローバル変数を参照するためにglobal宣言

    if message.author == client.user:
        return

    if message.channel.id != id_sys:
        return

    if message.content == "メッセージクリーン":
        channel = client.get_channel(id_sys)
        await channel.purge()  # チャンネルのメッセージを全削除
        channel = client.get_channel(id_gm)
        await channel.purge()  # チャンネルのメッセージを全削除
        channel = client.get_channel(id_talk)
        await channel.purge()  # チャンネルのメッセージを全削除

    elif message.content == "スタート":
        await message.channel.send(text.text_opening)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="オープニング")  # 指定した名前のロールを取得
        # role = guild.get_role(1274370444811833505)
        await give_role(guild, role)  # ロール付与
        key = 0

    elif message.content == "準備開始":
        await message.channel.send(text.text_prepare)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="準備")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "準備完了":
        await message.channel.send(text.text_explain)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="説明")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "会場":
        await message.channel.send(text.text_room)

    elif message.content == "ゲーム開始":
        await message.channel.send(text.text_start)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step1")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "生":
        await message.channel.send(text.text_Q1)
        # 送信先のチャンネル取得
        channel = client.get_channel(id_step1)
        file_path = os.path.join(os.path.dirname(__file__), "Q1.jpg")
        await channel.send(file=discord.File(file_path))

    elif message.content == "デデデ" or message.content == "ででで" or message.content == "デデデ大王":
        await message.channel.send(text.text_step1_clear)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step2")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "一":
        await message.channel.send(text.text_Q2)
        # 送信先のチャンネル取得
        channel = client.get_channel(id_step2)
        file_path = os.path.join(os.path.dirname(__file__), "Q2.jpg")
        await channel.send(file=discord.File(file_path))

    elif message.content == "キーコン" or message.content == "きーこん":
        await message.channel.send(text.text_step2_clear)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step3")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "日":
        await message.channel.send(text.text_Q3)
        # 送信先のチャンネル取得
        file_path = os.path.join(os.path.dirname(__file__), "Q3.jpg")
        await channel.send(file=discord.File(file_path))

    elif message.content == "スネーク" or message.content == "すねーく":
        await message.channel.send(text.text_step3_clear)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step4")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    elif message.content == "力":
        await message.channel.send(text.text_Q4_choice)

    elif message.content == "イージー" or message.content == "いーじー":
        await message.channel.send(text.text_Q4_easy)
        # 送信先のチャンネル取得
        channel = client.get_channel(id_step4)
        file_path = os.path.join(os.path.dirname(__file__), "Q4_easy.jpg")
        await channel.send(file=discord.File(file_path))

    elif message.content == "ハード" or message.content == "はーど":
        await message.channel.send(text.text_Q4_hard)
        # 送信先のチャンネル取得
        channel = client.get_channel(id_step4)
        file_path = os.path.join(os.path.dirname(__file__), "Q4_hard.jpg")
        await channel.send(file=discord.File(file_path))

    elif (message.content == "ほし" or message.content == "星") and key == 0:
        await message.channel.send(text.text_step4_hoshi)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step5")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与
        key = 1

    elif message.content == "グリーン" or message.content == "ぐりーん":
        await message.channel.send(text.text_step4_green)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="step5")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与
        key = 1

    elif message.content == "星" and key == 1:
        await message.channel.send(text.text_step5_clear)
        guild = message.guild  # メッセージが送信されたサーバーを取得
        role = discord.utils.get(guild.roles, name="clear")  # 指定した名前のロールを取得
        await give_role(guild, role)  # ロール付与

    else:
        await message.channel.send("...")


menu_text = """**__管理者権限 ON/OFF__：**
管理者ロール（持っていると全チャンネルの閲覧が可能）を切り替える

**__リセットする__：**
総力戦プレイ中に獲得できるロール、テキストログをリセットする
（※ボタンを押してから**処理完了まで、長いときは7秒ほどかかります**）"""


@tree.command(name="control", description="自分のユーザー名を確認")
async def username(interaction: discord.Interaction):
    allowed_channel_id = 1275480203291922584  # コントロールチャンネルでしか使用不可

    if interaction.channel.id != allowed_channel_id:
        await interaction.response.send_message("このチャンネルではこのコマンドを使用できません。", ephemeral=True)
        return
    button1 = discord.ui.Button(label="管理者権限 ON/OFF", style=discord.ButtonStyle.primary, custom_id="add_administrator")
    button2 = discord.ui.Button(label="リセットする", style=discord.ButtonStyle.primary, custom_id="reset")
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    embed = discord.Embed(title="コントロールメニュー", description=menu_text, color=0x0000FF)
    await interaction.response.send_message(embed=embed, ephemeral=False, view=view)
    # await interaction.response.send_message(menu_text, view=view)


# Botの起動
# client.run(token)
server_thread()
client.run(os.getenv("TOKEN"))
print("Current working directory:", os.getcwd())
