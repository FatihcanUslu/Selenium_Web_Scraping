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
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver=webdriver.Chrome(service=service,options=chrome_options)
    return driver

def General_Info_CSV():
    driver=driver_create()
    driver.get(website)

    tbody=driver.find_element(By.TAG_NAME, 'tbody')
    matches=tbody.find_elements(By.TAG_NAME, 'tr')


    artist=[]
    title=[]
    difficulty=[]
    link=[]

    for match in matches:
        #For artist
        artistinfo=match.find_element("xpath", './td[2]').text
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
        linkinfo = linkinfo[19:]
        linkinfo = linkinfo[:-1]
        linkinfo=plain + linkinfo
        link.append(linkinfo)
        #print(linkinfo)
        #print(type(linkinfo))
    driver.quit()
    df=pd.DataFrame({'artist':artist,'title':title,'difficulty':difficulty,'link':link})#making datafreame
    df.to_csv('8notes.csv',index=True)
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
                fullabout = fullabout + aboutinfo3.text
        about.append(fullabout)

        #For imagelink
        fullimage=[]#if it has more than 1 photo takes all of their links
        imageinfo=driver.find_elements("xpath",'// main / div / div[ @class ="img-container"]')
        for imagetemp in imageinfo:
            difficultyinfo = imagetemp.find_element(By.TAG_NAME, "img").get_attribute('src')
            fullimage.append(difficultyinfo)
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
























