import requests
import mysql.connector
from bs4 import BeautifulSoup

l1 = []
l2 = []
conn = mysql.connector.connect(user='root', password='5158', host='localhost', database='site_crawler')
mycursor = conn.cursor()

def scrape_data():
    for item in g_data:
        l1 = []
        a = (item.find("div", {"class": "_3wU53n"})).text.split('(')
        model = a[0]
        l1.append(model)
        try:
            b = (item.find("div", {"class": "OiPjke"})).text.split(' RAM')[0]
            if b is not None:
                l1.append(b)
            else:
                l1.append('0')
        except:
            pass
        try:
            c = (item.find("div", {"class": "_1vC4OE _2rQ-NK"})).text
            l1.append(c)
        except:
            pass
        try:
            color = a[1].split(',')[0]
            l1.append(color)
        except:
            pass
        try:
            rating = (item.find("div", {"class": "hGSR34 _2beYZw"})).text
            if rating is not None:
                l1.append(rating)
            else:
                l1.append('0')
        except:
            pass
        feature = (item.find_all("li", {"class": "tVe95H"}))
        try:
            rom = feature[0].text.split('|')[1].split(' ROM')[0]
            l1.append(rom)
        except:
            pass
        display = feature[1].text.split(' Display')[0]
        l1.append(display)
        rear_c = feature[2].text.split('|')[0].split(' Rear')[0]
        l1.append(rear_c)
        try:
            if 'Front' in feature[2].text:
                front_c = feature[2].text.split('|')[1].split(' Front')[0]
            else:
                front_c = '0'
        except:
            pass
        l1.append(front_c)
        try:
            battery = feature[3].text.split(' Battery')[0]
            l1.append(battery)
        except:
            pass
        try:
            processor = feature[4].text.split(' Processor')[0]
            l1.append(processor)
        except:
            pass
        warranty = feature[len(feature) - 1].text
        l1.append(warranty)
        l2.append(l1)


def insert_mysql():
    for dev in l2:
        try:
            mycursor.execute("""insert into flipkart(device_name, RAM, price, colour, rating, ROM, display, rear_camera, front_camera, battery, processor, warranty) values
                             (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            dev[0], dev[1], dev[2], dev[3], dev[4], dev[5], dev[6], dev[7], dev[8], dev[9], dev[10], dev[11]))
        except:
            pass


for i in range(1,10):
    l2=[]
    url = "https://www.flipkart.com/search?as=on&as-pos=1_1_ic_smartp&as-show=on&otracker=start&page=" + str(i) + "&q=smartphones&sid=tyy%2F4io&viewType=list"
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    g_data = soup.find_all("div", {"class": "col _2-gKeQ"})
    scrape_data()
    insert_mysql()
    conn.commit()

