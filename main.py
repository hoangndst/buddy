import discord
import datetime
from api import getCovidMess, getWeatherMess, getCatMess, getDogMess, getStandPL, getGaisImage
from regex import sayhi, bodyshaming, ny, covid, weather, cat, alive, badWord, dog, plstand, anhgai, old, game, film, learn
from server import activate
client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    match = sayhi.search(message.content)
    match_1 = bodyshaming.search(message.content)
    match_2 = ny.search(message.content)
    match_3 = badWord.search(message.content)
    match_4 = covid.search(message.content)
    match_5 = weather.search(message.content)
    match_6 = cat.search(message.content)
    match_7 = alive.search(message.content)
    match_8 = dog.search(message.content)
    match_9 = plstand.search(message.content)
    match_10 = anhgai.search(message.content)
    match_11 = old.search(message.content)
    match_12 = game.search(message.content)
    match_13 = film.search(message.content)
    match_14 = learn.search(message.content)
    now = datetime.datetime.now().strftime("%H:%M")
    if match:
        await message.channel.send('Xin chào ' + message.author.name + '!\n~ Chúc mọi điều tốt lành sẽ đến với bạn!')
    elif match_2:
        await message.channel.send('ny cc')
    elif match_1:
        await message.channel.send('Đừng body shaming bạn eii!')
    if match_3:
        await message.channel.send('Ngôn từ vô văn hóa')
    if match_4:
        covid_mess = getCovidMess()
        await message.channel.send(covid_mess)
    if match_5:
        weather_mess = getWeatherMess()
        await message.channel.send(weather_mess)
    if match_6:
        cat_mess = getCatMess()
        await message.channel.send(cat_mess)
    if match_7:
        await message.channel.send('Vẫn còn thở bro ạ 🙃')
    if match_8:
        dog_mess = getDogMess()
        await message.channel.send(dog_mess)
    if match_9:
        stand_mess = getStandPL()
        await message.channel.send(stand_mess)
    if match_10:
        gaiMess = getGaisImage()
        await message.channel.send(gaiMess)
    if match_11:
        await message.channel.send('Bug cũ rồi bro ạ 🙃')
    if match_12:
        await message.channel.send('@everyone' + ' gảm thôi các người anh em 🤩 📢')
    if match_13:
        await message.channel.send('@everyone' + ' phim thôi các người anh em 🤩 📢')
    if match_14:
        await message.channel.send('Bỏ học gảm thôi các người anh em 🎮 😋')
    if now == "21:09":
        await message.channel.send('Bây giờ là ' + now)
activate()
client.run('ODc3NTQxMDM1NDkwODIwMTQ4.YR0Hxg.snocV1aD3HJ1a-rWOPUg6w_hiTI')