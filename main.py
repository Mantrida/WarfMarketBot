import discord
from discord.ext import commands
import enumerate as enum
import requests
import tok

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Бот online')

@bot.command()
async def цена(ctx, *args):
    embed = discord.Embed(color=0x8A2BE2)
    if not args:
        await ctx.send('Не указано название предмета')
    elif ' '.join(args).title() in enum.dictonary:
        key = ' '.join(args).title()
        item_name = ' '.join(enum.dictonary[key].split('_')).title()

        url = enum.API_BASE_URL + f"/items/{enum.dictonary[key]}/orders"
        res_list = requests.get(url).json()['payload']['orders']
        res_list_ingame = [item for item in res_list if item['order_type'] == "sell" and item['user']['status'] == "ingame"]
        res_list_ingame = sorted(res_list_ingame, key=lambda x: x['platinum'])[0:5]

        for item in res_list_ingame:
            smile = '\U0001F610' if item["user"]["reputation"] < 6 else '\U0001F600'
            string = f'{item["platinum"]}       {item["user"]["ingame_name"]} '
            string2 = f'Region: "{item["user"]["region"]}" | {smile} - {item["user"]["reputation"]} \n'\
                      f'/w {item["user"]["ingame_name"]} Hi! I want to buy: {item_name} for {item["platinum"]} platinum. (warframe.market)'
            embed.set_author(name=string, icon_url=enum.PLATINUM)
            embed.description = string2
            await ctx.send(embed=embed)

        await ctx.send(enum.HOMEPAGE_URL + '/ru/items/' + enum.dictonary[key])

    else:
        await ctx.send(f'Не верное название предмета')

@bot.command()
async def инфо(ctx, *args):

    message = enum.message
    embed = discord.Embed(description=message, color=0x8A2BE2)

    await ctx.send(embed=embed)

@bot.command()
async def итем(ctx, *args):

    args = '' if not args else args[0]
    embed = discord.Embed(color=0x8A2BE2)

    if not args:
        embed.description = 'Не указан итем'
    elif args == 'фрейм':
        embed.description = enum.item_list_frame
    elif args == 'основа':
        embed.description = enum.item_list_primary
    elif args == 'вторичка':
        embed.description = enum.item_list_secondary
    elif args == 'ближка':
        embed.description = enum.item_list_melee
    elif args == 'етц':
        embed.description = enum.item_list_etc
    elif args == 'призма':
        embed.description = enum.item_list_prisma
    elif args == 'призрак':
        embed.description = enum.item_list_wraith
    elif args == 'вандал':
        embed.description = enum.item_list_vandal
    else:
        embed.description = 'Нет такой команды'

    await ctx.send(embed=embed)

bot.run(tok.TOKEN)
