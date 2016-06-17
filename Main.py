import sched, time
import requests
import ctypes
from bs4 import BeautifulSoup

s = sched.scheduler(time.time, time.sleep)
link = "http://www.njuskalo.hr/index.php?ctl=search_ads&keywords=inmusic&sort=new"
dict = dict() #dictionary ili samo {}

def check_site(sc):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article")

    if articles.__len__() > 0:
        first_article = articles[0]
        first_key = first_article.find_all("h3", {"class":"entity-title"})

        if not first_key[0].text in dict.keys():
            msg = 'Pojavila se nova karta:\n' #poruka za popup

            for a in articles:
                h3s = a.find_all("h3", {"class":"entity-title"})
                prices = a.find_all("strong", {"class":"price price--hrk"})
                #poveze varijable iz h i p - h[0] - p[0]
                for h, p in zip(h3s, prices):
                    if not h.text in dict.keys():
                        dict[h.text] = p.text
                        msg += (h.text) + ': ' + (p.text) + '\n'
                        print((h.text) + ': ' + (p.text))
                    else:
                        return

            message_box = ctypes.windll.user32.MessageBoxW
            message_box(None, msg, "Info", 1)
        else:
            print("--")

    sc.enter(7*60, 1, check_site, (sc,))

check_site(s)
s.run()