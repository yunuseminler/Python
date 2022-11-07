from colorama import init, Fore
import os
#Konsola renkli yazmak için gerekli satır
init(autoreset=True)

#Ay ismini numaraya döndüren fonksiyon
def mts(gelen):
    switcher = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    return switcher.get(gelen, "-")
#Ay kısaltmasını tam isme döndüren fonksiyon
def ett(gelen):
    switcher = {
        "Jan": "Ocak",
        "Feb": "Şubat",
        "Mar": "Mart",
        "Apr": "Nisan",
        "May": "Mayıs",
        "Jun": "Haziran",
        "Jul": "Temmuz",
        "Aug": "Ağustos",
        "Sep": "Eylül",
        "Oct": "Ekim",
        "Nov": "Kasım",
        "Dec": "Aralık",
    }
    return switcher.get(gelen, "-")
#Tarih formatlamaya yarayan fonksiyonlar
def formatla(gelen):
    try:
        date = ""
        temp = gelen
        temp = temp.split(". ")
        if(len(temp)==1):
            temp = temp[0].split("; ")
            temp = temp[1].split( )
            if(len(temp)==3):
                date = temp[2]+"/"+mts(temp[1])+"/"+temp[0]
            elif(len(temp)==2):
                date = "01/"+mts(temp[1])+"/"+temp[0]

        else:
            temp = temp[1].split(" ")  
            if(len(temp)>=3):
                temp3 = temp[2][:2]
                if(len(temp3)>1):
                    if (temp3[1]==':')or(temp3[1]==';')or(temp3[1]=='-'):
                        temp3="0"+temp3[0]  
                date = temp3+"/"+mts(temp[1])+"/"+temp[0]
                if(mts(temp[1])=="-"):
                    date = "01/01/"+temp[0]
            elif(len(temp)==2):
                date = "01/"+mts(temp[1][:3])+"/"+temp[0]
            elif(len(temp)==1):
                date = "01/01/"+temp[0][:4]
            else:
                date = gelen
        return date
    except:
        return gelen
#Progress barı ekrana yazdır
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'{Fore.YELLOW}\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
#Dosyaların yükleneceği klasörleri kontrol ediyor yok ise oluşturuyor
def dosyaKontrol():
    if not (os.path.exists("./doc")):
        os.mkdir("./doc")
    if not (os.path.exists("./docAdmin")):
        os.mkdir("./docAdmin")
    