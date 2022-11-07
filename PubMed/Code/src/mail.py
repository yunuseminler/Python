from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import json

with open('./data/config.json') as f:
    veri = json.load(f)

#<---Mail--->
toaddr = veri["mail"]["to"]         #Kime atılıyor
cc = veri["mail"]["cc"]             #Kime bilgi gidecek
bcc = veri["mail"]["bcc"]           #Gizli Alıcılar
fromaddr = veri["mail"]["fromaddr"] #Kim tarafından
host = veri["smtp"]["host"]         #smtp Hostname
portD = veri["smtp"]["port"]        #smtp port number
#<------>

def send(month,dosyaAdi):

    #<---Mail içeriği--->
    mail_content = "Merhabalar,\n\nIstemis oldugunuz "+month+" ayi Pubmed makale listesi ekte yer almaktadir.\n\nBilginize."
    #<------>
    
    #<---Mail bilgileri--->
    message = MIMEMultipart()
    message['From'] = fromaddr                          #Kim tarafından atıldığı
    message['To'] = ", ".join(toaddr)                   #Mailin kime gittiği
    message['CC'] = ", ".join(cc)                       #Kime bilgi maili gönderildiği
    message['Subject'] = "Pubmed " +month+ " ayi ozeti" #Konusu
    #<------>
    
    #<---Mailde gönderilecek dosya tanımlaması--->
    message.attach(MIMEText(mail_content, 'plain'))
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(dosyaAdi, "rb").read())
    encoders.encode_base64(part)
    temp = dosyaAdi[6:]
    temp = 'attachment; filename="'+temp+'"'
    part.add_header('Content-Disposition', temp)
    message.attach(part)
    #<------>
    
    #<---Mailin gönderilmesi--->
    toaddrs = [toaddr] + cc + bcc
    smtp = smtplib.SMTP(host, port=portD)
    smtp.sendmail(fromaddr, toaddrs, message.as_string())
    #<------>
    smtp.quit() 