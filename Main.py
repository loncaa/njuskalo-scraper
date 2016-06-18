import sched, time #odgadanje zadatka
import requests #dohvacanje podataka
import ctypes #popup
from datetime import datetime #prikazivanje vremena
from threading import Thread
from bs4 import BeautifulSoup

s = sched.scheduler(time.time, time.sleep)
site_http = "http://www.njuskalo.hr/index.php?ctl=search_ads&keywords=inmusic&sort=new"
dict = dict() #dictionary ili samo {}

def show_message(msg):
    message_box = ctypes.windll.user32.MessageBoxW
    message_box(None, msg, "Info", 1)

def check_site(sc):
    r = requests.get(site_http)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article", {"class":"entity-body"})

    if articles.__len__() > 0:
        time_to_message = False

        first_h3_tag = articles[0].find_all("h3", {"class":"entity-title"})
        first_link = first_h3_tag[0].find_all("a")[0].attrs["href"]

        if not first_link in dict: #.keys
            msg = 'Pojavila se nova karta:\n' #poruka za popup
            for a in articles:
                time_to_break = False
                h3_tags = a.find_all("h3", {"class":"entity-title"})
                link = h3_tags[0].find_all("a")
                price = a.find_all("strong", {"class": "price price--hrk"})

                #spremanje podataka u niz
                if price.__len__() > 0 and link.__len__() > 0:
                    l = link[0].attrs["href"] #link
                    p = price[0].text #price
                    t = link[0].text #title

                    if not l in dict.keys():
                        time_to_message = True
                        dict[l] = p
                        msg += t + ': ' + p + '\n'
                        print("++ New ticke: " + t + ': ' + p + "\n\t++link: " + l)
                    else:
                        time_to_break = True
                        break
                #if time_to_break is True:
                #   break

            if time_to_message:
                thread = Thread(target=show_message, args=(msg,))
                thread.start()
                #DODATI ZVUK
                #thread.join() #čeka nit da zavrsi s radom
        else:
            print("-- Not new tickets at " + datetime.now().strftime("%Y-%m-%d in %H:%M:%S") + "--")

    sc.enter(3*60, 1, check_site, (sc,))

check_site(s)
s.run()