import twint
import os
from textblob import TextBlob
from googletrans import Translator
import datetime
import pyodbc
import json

#<---Config dosyası okunuyor--->
with open('./config.json') as f:
    veri = json.load(f)
#<------>

#<---Database tanımlanıyor--->
driver =  "Driver={"+veri["Driver"]+"};"  
server =  "Server={"+veri["Server"]+"};"
database =  "Database={"+veri["Database"]+"};"  
conn = pyodbc.connect(driver+server+database+"Trusted_Connection=yes;")
cursor = conn.cursor()
#<------>

#<---Twitterda kelimeyi arayan fonksiyon--->
def ara(ilaclar):
    c = twint.Config()
    c.Lang = "tr"
    c.Limit = 1000
    c.Store_json = True 
    for ilac in ilaclar:
        c.Search = [ilac]
        dosyaAdi = "./doc/" + "i" + ilac +".json"
        c.Output = dosyaAdi 
        twint.run.Search(c) 

#<---Json formatında gelen verinin istenmeyen değerlerini çıkartıyor. Örneğin anahtar kelime kullanıcı adı olarak verilmiş olabiliyor.
def temizle(ilaclar):
    for ilac in ilaclar:
        if not(os.path.exists("./doc/" + "i" + ilac +".json")):
            first = open("./doc/" + "i" + ilac +".json", "w",encoding='utf8')
            first.close()
        first = open(("./doc/" + "i" + ilac +".json"),encoding='utf8')
        second = open("./doc/T" + ilac +".json", "w",encoding='utf8')
        while True:
            row = first.readline()
            if len(row) == 0:
                 break 
            x = row.find("tweet")
            y = row.find("language");
            if((row.find(ilac,x,y)!=(-1))):
                z = row.find("screen_name")
                if(row.find(ilac,z) == (-1)):
                    second.write(row)
            
        first.close()
        second.close()
        if os.path.exists("./doc/" + "i" + ilac +".json"):
            os.remove("./doc/" + "i" + ilac +".json")
        else:
            print("The file does not exist")           

#Json formatındaki verinin ihtiyacımız olan kısımları çıkartılıp,formatlanıyor ve csv formatında yazılıyor.
def Tclear(ilaclar):
    for ilac in ilaclar:
        dosya = open("./doc/T"+ilac+".json",encoding='utf8')
        first = open("./doc/T" + ilac +".csv", "w",encoding='utf8')
        first.write("content,date\n")
        satirlar = dosya.readlines()
        for x in range(len(satirlar)):
            veriler = satirlar[x].split(",")
            date = veriler[3]
            date = date.strip()
            date = date[8:]
            date = date.strip("\"")
            
            content = " "
            for y in range(len(veriler)):
                if ((veriler[y].find("tweet\":"))!=(-1)):
                    content = veriler[y]
                    break;
            content = content.strip();
            content = content[9:]; 
            content = content.strip("\"")
            temp = content.split(" ")
            temp1 = " "
            for z in temp:
                if(z.find("@")==(-1)):
                    temp1 = temp1 + z + " "
            temp1 = temp1.strip("\"")
            temp1 = duzenle(temp1)
            temp1 = temp1.strip()
                
            if(tarih(ilac)):
                first.write(temp1+","+date+"\n")
                
        first.close()
        dosya.close()
        if os.path.exists("./doc/T"+ilac+".json"):
            os.remove("./doc/T"+ilac+".json")
        else:
            print("The file does not exist")

#Forumdan gelen verinin değerleri formatlanıyor ve yeni dosyaya yazılıyor.
def Eclear(ilaclar):
    for ilac in ilaclar:
        dosya = open("./doc/EK"+ilac+".csv",encoding='utf8')
        first = open("./doc/E" + ilac +".csv", "w",encoding='utf8')
        first.write("content,date\n")
        satirlar = dosya.readlines()
        for x in range(len(satirlar)):
            veriler = satirlar[x].split(",")
            if(veriler[0]=="Entry"):
                continue
            content = " "
            if (len(veriler)>3):
                for y in range((len(veriler)-2)):
                    content = content + veriler[y]
            else:
                content = veriler[0]
            content = content.strip();
            content = content.strip("\"")
            content = duzenle(content)
            content = content.strip() 
            date = veriler[len(veriler)-2]
            if(not(content.find("bkz") == 0)):
                if(tarih(ilac)):
                    first.write(content+","+date+"\n")
            
        first.close()
        dosya.close()
        if os.path.exists("./doc/EK"+ilac+".csv"):
            os.remove("./doc/EK"+ilac+".csv")
        else:
            print("The file does not exist")

#Her satırdaki veriler olumlu/olumsuz/kararsız olarak etiketleniyor ve birleştirilip son hali dosyaya yazılıyor
def etiketle(ilaclar,source):
       
    translator = Translator()
    for ilac in ilaclar:
        dosya = open("./doc/"+source+ilac+".csv",encoding='utf8')
        first = open("./doc/" + ilac +".csv", "a",encoding='utf8')
        if(source == "T"):
            first.write("content,date,resultValue,result,location\n")
        satirlar = dosya.readlines()
        for satir in satirlar:
            veriler = satir.split(",")
            if(veriler[0] == "content"):
                continue
            if(translator.detect(veriler[0]).lang=='tr'):
                temp=" "
                if(len(veriler[0])>1000):
                    temp = veriler[0][0:999]
                example = translator.translate(temp).pronunciation
                blob1 = TextBlob(example)
                sonuc = blob1.sentiment.polarity
                status = " "
                if(sonuc > 0):
                    status="olumlu"
                elif(sonuc <0):
                    status="olumsuz"
                else:
                    status="kararsız"
                harf = " "
                if(source=="T"):
                    harf= "twitter"
                else:
                    harf = "forum"
                veriler[1] = veriler[1].replace("\n","")
                first.write(veriler[0] + "," + veriler[1] +","+str(sonuc)+"," + status + ","+harf+"\n")
        dosya.close()
        first.close()
        if os.path.exists("./doc/"+source+ilac+".csv"):
            os.remove("./doc/"+source+ilac+".csv")
        else:
            print("The file does not exist")

#Gelen veriyi noktalama işaretlerinden ve istenmeyen karakterlerden ayırıyor.
def duzenle(gelen):
    temp1 = gelen.replace("."," ")
    temp1 = temp1.replace(";"," ")
    temp1 = temp1.replace(":"," ")
    temp1 = temp1.replace("'","")
    temp1 = temp1.replace("..."," ")
    temp1 = temp1.replace("-"," ")
    temp1 = temp1.replace("?"," ")
    temp1 = temp1.replace("!"," ")
    temp1 = temp1.replace("_"," ")
    temp1 = temp1.replace("("," ")
    temp1 = temp1.replace(")"," ")
    temp1 = temp1.replace("\""," ")
    temp1 = temp1.replace("*"," ")
    temp1 = temp1.replace("  "," ")
    temp1 = temp1.replace("   "," ")
    return temp1

#Verinin son halini veritabanına gönderiyor.
def databaseSend(ilaclar):
    
    date = datetime.datetime.now()
    date = date.strftime("%x")
    date = date.split("/")
    date = "20"+date[2]+"-"+date[0]+"-"+date[1]
    
    for ilac in ilaclar:
        temp = "insert into dbo.SocialLogs(Date, Name) values ('"+date+"','"+ilac+"')"
        cursor.execute(temp)
        dosya = open("./doc/"+ilac+".csv",encoding='utf8')
        satirlar = dosya.readlines()
        for x in range(len(satirlar)):
            if(x == 0):
                continue
            veriler = satirlar[x].split(",")
            veriler[4] = veriler[4].replace("\n","")
            if(len(veriler[1])>16):
                veriler[1] = veriler[1][:16]
            temp = "insert into dbo.SocialComments(Date, Name, Content, Status, Rate, Source) values ('"+veriler[1]+"','"+ilac+"','"+veriler[0]+"','"+veriler[3]+"','"+veriler[2]+"','"+veriler[4]+"')"
            try:
                cursor.execute(temp)
            except:
                temp = 0
                
        dosya.close()
    conn.commit()     
    conn.close()

#Gönderilen ilaç isminin dataframedeki son log tarihini getiririyor.
def tarih(ilac):
    date = datetime.datetime.now()
    date = date.strftime("%x")
    date = date.split("/")
    cursor.execute("SELECT * FROM dbo.SocialLogs where Name='"+ilac+"'")
    for i in cursor:
        date1 = i[1]
    date1 = date1.split("-")
    if(date1[0][2] == date[2]):
        if(date1[1] == date[0]):
            if(date1[2]> date[1]):
                return True
            else:
                return False
        elif(date1[1] > date[0]):
            return True
        else:
            return False
    elif(date1[0][2] > date[2]):
        return True
    else:
        return False