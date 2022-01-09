import discord
from api import getCovidMess, getWeatherMess, getCatMess, getDogMess, getStandPL, getGaisImage, getFunImage, Addfilm
from regex import sayhi, bodyshaming, ny, covid, weather, cat, alive, badWord, dog, plstand, anhgai, old, game, film, learn, fun, getAllNumber
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
    match_15 = fun.search(message.content)
    if match:
        content = 'Xin chào ' + message.author.name + '!\n~ Chúc mọi điều tốt lành sẽ đến với bạn!\n'
        content += 'Buddy Film Extension:\n'
        content += '`$fView`: Xem số lượng phim đã xem.\n'
        content += '`$fAdd [Số lượng]`: Thêm hoặc bớt số lượng phim đã xem.\n'
        content += '`$fFix [Số lượng]`: Sửa số lượng phim đã xem.\n'
        content += '\nTính năng vẫn đang phát triển các homie đợi nhóe :3!'
        await message.channel.send(content)
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
        if message.author.id == 493052410713866240:
            await message.channel.send('Kim Da-mi chứ gì Long, đợi tí :))')
            gaiMess = getGaisImage(4)
            await message.channel.send(gaiMess)
        else:
            gaiMess = getGaisImage(1)
            await message.channel.send(gaiMess)
    if match_11:
        await message.channel.send('Bug cũ rồi bro ạ 🙃')
    if match_12:
        # await message.channel.send('@everyone' + ' gảm thôi các người anh em 🤩 📢')
        await message.channel.send('Bỏ gảm đi nghiện quá 😒')
    if match_13:
        await message.channel.send('@everyone' + ' phim thôi các người anh em 🤩 📢')
    if match_14:
        await message.channel.send('Learn or lủng 😏')
        # await message.channel.send('Bỏ học gảm thôi các người anh em 🎮 😋')
    if match_15:
        funImg = getFunImage()
        await message.channel.send(funImg)
    if message.content.startswith('$fAdd'):
        num = getAllNumber(message.content)
        if len(num) == 1:
            msg = Addfilm(1, num[0])
            await message.channel.send(msg)
        else:
            await message.channel.send('Sai cú pháp rồi bro, Buddy đ đủ thông minh để hiểu 😒')
    if message.content.startswith('$fFix'):
        num = getAllNumber(message.content)
        if len(num) == 1:
            msg = Addfilm(2, num[0])
            await message.channel.send(msg)
        else:
            await message.channel.send('Sai cú pháp rồi bro, Buddy đ đủ thông minh để hiểu 😒')
    if message.content.startswith('$fView'):
        msg = Addfilm(3, 0)
        await message.channel.send(msg)

activate()
client.run('ODc3NTQxMDM1NDkwODIwMTQ4.YR0Hxg.snocV1aD3HJ1a-rWOPUg6w_hiTI')