import requests
import json
import datetime
def getCovidMess():
    covid19 = requests.get("https://api.covid19api.com/dayone/country/vietnam");
    covid19_data = json.loads(covid19.text)
    today = covid19_data[-2]
    yesterday = covid19_data[-3]
    increase = today['Confirmed'] - yesterday['Confirmed']
    increase_mess = "";
    if increase == 0:
        increase_mess = "";
    elif increase > 0:
        increase_mess = 'tăng ' + str(increase) + ' ca so với ngày hôm qua! 😢'
    else:
        increase_mess = 'giảm ' + str(abs(increase)) + ' ca so với ngày hôm qua! 😊'
    confirmed = today['Confirmed']
    recovered = today['Recovered']
    deaths = today['Deaths']

    covid19_mess =  "🦠 𝕊𝔸ℝ𝕊-ℂ𝕠𝕍-𝟚 ⁉️ \n" + "Số ca mắc Covid19 tính đến nay tại Viêt Nam là: " + str(confirmed) +", " + increase_mess + "\nSố ca tử vong là: " + str(deaths) + "\nSố ca phục hồi là: " + str(recovered) + "\nHãy hạn chế ra ngoài, ở nhà học tập trau dồi kiến thức cùng IU xinh đẹp nhé! 😻"
    return covid19_mess
def getWeatherMess():
    now = datetime.datetime.now()
    day = [ "thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "chủ Nhật"];
    day1 = day[now.weekday()]
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Hanoi,10000,VN&units=metric&lang=vi&appid=0407f9d8e492e0998287575717078017')
    weather_data = json.loads(weather.text)
    w_today = weather_data["weather"][0]['description']
    feels_like = weather_data["main"]['feels_like']
    temp_min = weather_data["main"]['temp_min']
    humidity = weather_data["main"]['humidity']

    weather_mess = "🌦 Thời tiết "+ str(day1) + " - " + str(now.date()) + "\nThời tiết hôm nay: " + str(w_today) + "\nNhiệt độ cảm giác: " + str(feels_like) + "°C." + "\nNhiệt độ thấp nhất: " + str(temp_min) + "°C." + "\nĐộ ẩm: " + str(humidity) + "%."
    # print(weather_mess)
    return weather_mess


def getCatMess():
    cat_url = "https://api.thecatapi.com/v1/images/search"
    headers = {'x-api-key': 'DEMO-API-KEY'}
    cat = requests.get(cat_url, headers=headers)
    cat_mess = json.loads(cat.text)[0]['url']
    return cat_mess

def getDogMess():
    dog = requests.get("https://random.dog/woof.json")
    dog_data = json.loads(dog.text)
    dog_mess = dog_data['url']
    return dog_mess

def getStandPL():
	url = "https://api.football-data.org/v2/competitions/2021/standings"
	headers = {
		'X-Auth-Token': 'fd206c7fc72449a199f8b8a2e91ef5f5'
	}
	standing = requests.get(url, headers=headers)
	standing_data = json.loads(standing.text)
	standing_mess = "Premier League Standings ⚽"
	n = len(standing_data['standings'][0]['table'])
	for i in range(n):
		standing_mess +='\n' + str(i+1) + ": " +standing_data['standings'][0]['table'][i]['team']['name']
	return standing_mess

def getGaisImage():
	url = "https://script.google.com/macros/s/AKfycbyjt-OlSu5pIEoMZcjsIpug95qL4kLAhQbZ1w6xqmSovvK3nAf1ba3vX0T4Ng_wpBrR/exec"
	gai = requests.get(url)
	gaiImage = json.loads(gai.text)
	gaiMess = gaiImage["image"]
	return gaiMess
def getFunImage():
	url = "https://script.google.com/macros/s/AKfycby5b5EkTkt3cP3FxiHSESrSHVCxw4KZhIhb4y_ZMcWpKZF0ytalwqwAY4bbDEhGzzxk/exec"
	gai = requests.get(url)
	gaiImage = json.loads(gai.text)
	gaiMess = gaiImage["image"]
	return gaiMess
def Addfilm(q, filmAdd):
    url = "https://script.google.com/macros/s/AKfycbzaPYosnQEdoMLlM5KhFq1riyZmCTZS7A_SksOVosygDAwptbhCWg6lLPvynlSfS2DZ/exec?q=" + str(q) + "&filmAdd=" + str(filmAdd)
    film = requests.get(url)
    film_data = json.loads(film.text)
    film_mess = film_data["msg"]
    return film_mess