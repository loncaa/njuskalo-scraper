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
    articles = soup.find_all("article", {"class":"entity-body"})

    if articles.__len__() > 0:
        time_to_message = False

        first_h3_tag = articles[0].find_all("h3", {"class":"entity-title"})
        first_link = first_h3_tag[0].find_all("a")[0].attrs["href"]

        if not first_link in dict: #.keys
            msg = 'Pojavila se nova karta:\n' #poruka za popup

            links = [] #linkovi su junik key za artikl
            prices = [] #cijena artikla
            titles = [] #naziv artikla
            for a in articles:
                h3_tags = a.find_all("h3", {"class":"entity-title"})
                l = h3_tags[0].find_all("a")
                p = a.find_all("strong", {"class": "price price--hrk"})

                #spremanje podataka u niz
                if p.__len__() > 0 and l.__len__() > 0:
                    links.append(l[0].attrs["href"])
                    prices.append(p[0].text)
                    titles.append(l[0].text)

            #nizovi su spojeni po indexu
            for l, p, t in zip(links, prices, titles):
                if not l in dict.keys():
                    time_to_message = True
                    dict[l] = p
                    msg += (t) + ': ' + (p) + '\n'
                    print((t) + ': ' + (p))
                else:
                    break

            if time_to_message:
                message_box = ctypes.windll.user32.MessageBoxW
                message_box(None, msg, "Info", 1)
        else:
            print("--")

    sc.enter(5*60, 1, check_site, (sc,))

check_site(s)
s.run()