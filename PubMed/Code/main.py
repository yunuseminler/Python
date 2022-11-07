from bs4 import BeautifulSoup
from pandas import DataFrame as pd
from pandas import ExcelWriter as pe
from pandas import concat as pc
from datetime import datetime as datet
import requests
import src.mail as mail
import src.fonk as fonk

start = datet.now()#Başlangıç saati alınıyor
fonk.dosyaKontrol()#Dosyaların yükleneceği klasörleri kontrol ediyor

#Ana Program
def program():
    
    #<---Excel Writer tanımlanıyor ve kolon stilleri tanımlanıyor.---->
    writer = pe("./doc/Pubmed_"+fonk.ett(start.strftime("%b"))+"_"+start.strftime("%Y")+".xlsx")
    workbook=writer.book
    worksheet=workbook.add_worksheet('Result')
    writer.sheets['Result'] = worksheet
    writer.sheets['Result'].set_column(2, 2, 40)
    writer.sheets['Result'].set_column(1, 1, 80)
    writer.sheets['Result'].set_column(0, 0, 12)
    bold = workbook.add_format({'bold': True,'valign': 'center'})
    excelindex = 0
    #<---------->
    
    #<---Excel Writer tanımlanıyor ve kolon stilleri tanımlanıyor.---->
    writer1 = pe("./docAdmin/Data_Pubmed_"+fonk.ett(start.strftime("%b"))+"_"+start.strftime("%Y")+".xlsx")
    workbook1=writer1.book
    worksheet1=workbook1.add_worksheet('Data')
    writer1.sheets['Data'] = worksheet1
    writer1.sheets['Data'].set_column(4, 4, 40)
    writer1.sheets['Data'].set_column(3, 3, 80)
    writer1.sheets['Data'].set_column(2, 2, 12)
    writer1.sheets['Data'].set_column(1, 1, 15)
    writer1.sheets['Data'].set_column(0, 0, 12)
    #<---------->
    
    #<---Daha sonra ekleme yapmak için boş dataframe oluşturuluyor.--->
    Datadf = pd(columns=['SendDate','Source','Date','Header','Link','To','CC','BCC'])
    #<---------->
    
    #Her molekül için işlem yapılıyor
    for t in mail.veri["source"]:
        
        #<---İlk sayfaya istek atılıyor--->
        url = "https://pubmed.ncbi.nlm.nih.gov/?term="+t+"&sort=pubdate"
        response = requests.get(url)
        html_icerik = response.content
        soup = BeautifulSoup(html_icerik,"html.parser")
        #<---------->
        
        #<---Log dosyası açılarak en son kaydedilen content pmid bulunuyor.--->
        log = open("./data/log.txt",encoding='utf8')
        logs = log.readlines()
        pmid = ""
        for i in logs:
            h = i.split(",")
            if(h[0]==t):
                pmid = h[1]   
        #<---------->
        
        #<---Sayfa sayısı bulunuyor--->
        pages = soup.find_all("label",attrs={"class":"of-total-pages"})
        page = ""
        for i in pages:
            page = i.text
        page = page.split(" ")
        page = page[1]
        if not(page.find(",")==-1):
            page = page.split(",")
            page = page[0]+page[1]
        #<---------->
        
        #<---Boş df dosyası oluşturuluyor.--->
        df = pd(columns=['Date','Header','Link'])
        #<---------->
      
        m=0
        d=0
        print(fonk.Fore.YELLOW +t+" işleniyor")
        
        #Sayfa sayısı kadar işlem yapılıyor.
        for x in range(int(page)):
            
            #<---x. Sayfaya istek atılıyor--->
            url = "https://pubmed.ncbi.nlm.nih.gov/?term="+t+"&sort=pubdate&page="+str(x+1)
            response = requests.get(url)
            html_icerik = response.content
            soup = BeautifulSoup(html_icerik,"html.parser")
            #<---------->
            
            #<---Başlıklar ve tarihler bulunuyor.--->
            content = soup.find_all("a",attrs={"class":"docsum-title"})
            dates = soup.find_all("span",attrs={"class":"full-journal-citation"})
            sayac = 0
            #<---------->
            
            #Her sayfadaki içerik için işlem yapılıyor
            for y in content:
                
                #<---Pmid alınıyor
                link = y.get("href")
                link = link.replace("\n","")
                #<---------->
                
                #<---Log dosyasından okunan pmid ile karşılaştırıyor. Aynı ise sonlandırılıyor--->
                if((link.strip("/"))==pmid):
                    d = 1
                    break
                #<---------->
                    
                #<---İlk Okumada log dosyasına yeni log yazılıyor.--->
                if(m==0):
                    m = 1
                    date1 = start.strftime("%d")+"/"+start.strftime("%m")+"/"+start.strftime("%Y")
                    dosya = open("./data/log.txt","a",encoding='utf8')
                    dosya.write(t+","+link.strip("/")+","+date1+"\n")
                    dosya.close()
                #<---------->
                
                #<---Dökümana koyulacak link oluşturuluyor.--->
                link = "https://pubmed.ncbi.nlm.nih.gov/"+link
                link = "=HYPERLINK(\""+link+"\")"
                #<---------->
                
                #<---Dökümana koyulacak Content başlığı bulunuyor.--->
                text = y.text.replace("\n","")
                text = text.strip()
                text = text.strip("[")
                text =text.strip("]")
                #<---------->
                
                #<---Döküman Tarihi bulunuyor.--->
                date = fonk.formatla(dates[sayac].text)
                sayac = sayac + 1
                #<---------->
                
                #<---Bulunan tüm içerik df ye ekleniyor--->
                try:
                    df2 = pd([[date,text,link]], columns=['Date','Header','Link'])
                    df = pc((df,df2),ignore_index=True)
                    df3 = pd([[(start.strftime("%d")+"/"+start.strftime("%m")+"/"+start.strftime("%Y")),t,date,text,link,mail.toaddr,mail.cc,mail.bcc]], columns=['SendDate','Source','Date','Header','Link','To','CC','BCC'])
                    Datadf = pc((Datadf,df3),ignore_index=True)
                except:
                    ax=0
                #<---------->
            #<---Log dosyasından okunan pmid ile karşılaştırıldı. Aynı olduğu için sonlandırılıyor.--->
            if(d==1):
                break
            #<---------->
            
            #<---Progress bar her sayfada bir ekrana yazdırılıyor--->    
            try:
                fonk.printProgressBar(x+1, float(page), prefix = 'Progress:', suffix = 'Complete', length = 15)
            except:
                ax = 1
            #<---------->
                
        print(fonk.Fore.GREEN + "--Tamamlandi--")
        
        #<---Df boş değilse excel dosyasına yazılıyor.--->
        if not (df.empty):
            worksheet.write_string(excelindex , 1, t,bold)#Başlık Yazılıyor
            df.to_excel(writer,sheet_name='Result',startrow=excelindex+2 , startcol=0,index=False)#Df yazılıyor
            excelindex = df.shape[0] + excelindex + 5
        #<---------->
        
        log.close()
    #<---Molekül okuması bittiğinde df'nin tamamı data excel dosyasına yazılıyor--->
    Datadf.to_excel(writer1,sheet_name='Data',index=False)       
    #<---------->
      
      
    #<---En son olarak yazılan dosyalar kaydediliyor.--->
    writer1.save()
    writer.save()
    mail.f.close()
#<---------->
    
#Main
def main():  
    program()#Programı başlat
    dosyaAdi = "./doc/Pubmed_"+fonk.ett(start.strftime("%b"))+"_"+start.strftime("%Y")+".xlsx"
    mail.send(fonk.ett(start.strftime("%b")),dosyaAdi)#Dosyaları mail gönder
    print("Geçen Zaman : "+str((datet.now())-start))#Çalışma zamanı hesaplanıyor

main()