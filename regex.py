import re
import datetime
sayhi = re.compile('(xin\s(chào|chao)|hi|hello|chào|chao|yo|hey)(.+)*buddy', re.IGNORECASE)
bodyshaming = re.compile('(b(\W+|\d+)*é(\W+|\d+)*(o|0))|(l(\W+|\d+)*ợ(\W+|\d+)*n)', re.IGNORECASE)
badWord = re.compile('(([^a-z]+|(^))(d|đ)(\W+)*m)|((đ|d)(i|ị)t)|đĩ', re.IGNORECASE)
covid = re.compile('((th(ô|o)ng(\s+|\w+|\W+|)tin)|(infor(\w+)?))(\s+|\w+\|\W+|)(.+)?covid', re.IGNORECASE)
weather = re.compile('((info(w+)*|th(o|ô)ng(.+)*tin))(.+)*((weather)|((thoi|thời)(.+)*(tiet|tiết)))|((weather)|((thoi|thời)(.+)*(tiet|tiết)))(.+)*((today|h(o|ô)m(.+)*(nay)))', re.IGNORECASE)
cat = re.compile('(ả|a)nh(.+)*(meo|mèo)', re.IGNORECASE)
dog = re.compile('(ả|a)nh(.+)*(cho|chó)', re.IGNORECASE)
ny = re.compile('ny', re.IGNORECASE)
alive = re.compile('(c(ò|o)n|co)(.+)*(s(o|ô|ố)ng)', re.IGNORECASE)
plstand = re.compile('(bxh|(b(a|ả)ng(.+)*(x(e|ế)p)(.+)*))(.+)*(nha|(ngo(a|ạ)i(.+)*(h(a|ạ)ng)))', re.IGNORECASE)
anhgai = re.compile('(a|ả)nh(.+)*(g(a|á)i|xinh)', re.IGNORECASE)
old = re.compile('edm', re.IGNORECASE)
game = re.compile('lol|game|gảm|gaming|dst', re.IGNORECASE)
film = re.compile('phim|film|phỉm', re.IGNORECASE)
learn = re.compile('học', re.IGNORECASE)

now = datetime.datetime.now().strftime("%H:%M")
print(now)
if now == "21:03":
    print("Good night")