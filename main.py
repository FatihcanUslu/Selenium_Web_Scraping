from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import json

website='https://www.8notes.com/piano/classical/sheet_music/'
plain='https://www.8notes.com'
path='webdriver/chromedriver.exe'

def driver_create():

    service=Service(path)
    chrome_options = Options()#açılan web sitede iş bittikten sonra kapanmama hatası olduğu için kullanıldı
    chrome_options.add_experimental_option("detach", True)
    driver=webdriver.Chrome(service=service,options=chrome_options)
    return driver

def General_Info_CSV():
    driver=driver_create()
    driver.get(website)#istenilen web site adresine git

    tbody=driver.find_element(By.TAG_NAME, 'tbody')#isterleri karşılayan ilk objeyi döndür
    matches=tbody.find_elements(By.TAG_NAME, 'tr')#isterleri karşılayan objeleri döndür
    print(type(matches)) # <class 'list'>
    print(matches) # elemanlar listesi

    artist=[]
    title=[]
    difficulty=[]
    link=[]

    for match in matches:
        #For artist
        artistinfo=match.find_element("xpath", './td[2]').text#xpath nitelendirmelerde kullanılır (//tbody/tr[3]/td[3]). Bir elementi nitelendirirken kullanılır. indis 1'den başlar.
        #print(artistinfo)#for the sake of debugging
        artist.append(artistinfo)
        #For title
        title.append(match.find_element("xpath", './td[3]').text)
        #For difficulty
        temp = match.find_element("xpath", './td[4]')
        difficultyinfo=temp.find_element(By.TAG_NAME,"img").get_attribute('title')
        difficulty.append(difficultyinfo)
        #For link
        linkinfo = match.get_attribute('onclick')
        print("all link info:",linkinfo)
        linkinfo = linkinfo[19:]#link infonun ilk 19 karakterini sil
        linkinfo = linkinfo[:-1]#link infonun son karakterini sil
        linkinfo=plain + linkinfo
        link.append(linkinfo)
        #print(linkinfo)
        #print(type(linkinfo))
    driver.quit()
    df=pd.DataFrame({'artist':artist,'title':title,'difficulty':difficulty,'link':link})#making datafreame
    df.to_csv('8notes.csv',index=True)#odevin amacı bu formatta tutmak olmasada önce csv formatında kayıt alındı.
    #df.to_json('8notes.json',index=True)
    #print(df)
    print("csv dosyasi oluşturuldu")
    return df



def JSON_Info(df):
    driver=driver_create()
    #df = pd.read_csv('8notes.csv')
    print(df.head())
    link = df["link"].tolist()
    imglink = []
    midilink = []
    about = []
    difficulty = df["difficulty"].tolist()
    final=[]
    for x in range(len(df)):
        website=link[x]
        driver.get(website)

        #For midilink
        midi = driver.find_element("xpath", '//li/a[@class="midi_list"]').get_attribute('href')
        midilink.append(midi)
        #print(midi)

        fullabout = ""
        aboutinfo=driver.find_elements("xpath", '//div[@id="infobox"]/table')
        for aboutinfo1 in aboutinfo:
            aboutinfo2 = aboutinfo1.find_elements(By.TAG_NAME, 'td')
            for aboutinfo3 in aboutinfo2:
                fullabout = fullabout + aboutinfo3.text#bulunan her td içerisinde yazı text olarak fullabout'a eklenir
        about.append(fullabout)

        #For imagelink
        fullimage=[]#if it has more than 1 photo takes all of their links
        imageinfo=driver.find_elements("xpath",'// main / div / div[ @class ="img-container"]')
        for imagetemp in imageinfo:
            imagelinkinfo = imagetemp.find_element(By.TAG_NAME, "img").get_attribute('src')
            fullimage.append(imagelinkinfo)
        imglink.append(fullimage)
        #print(fullimage)
        print("belirtilen web site tamamlandi: ",website)
        #print("1",link[x])
        #print("2",imglink[x])
        #print("3",midilink[x])
        #print("4",about[x])
        #print("5",difficulty[x])
        final.append([link[x],imglink[x],midilink[x],about[x],difficulty[x]])
    driver.quit()
    print(final)
    finaljson = json.dumps(final)
    with open("8notes.json", "w") as outfile:
        outfile.write(finaljson)

df = General_Info_CSV()
JSON_Info(df)
























