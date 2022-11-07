import fonk
import eksi_scraper
#Programın ayağa kalktığı dosyadır. Fonksiyonlar sırasıyla çalıştırılır.


ilac = open("./source.txt")
ilaclar = ilac.readline()
ilaclar = ilaclar.split(",")

for x in ilaclar:
    eksi_scraper.search(x)
    
fonk.ara(ilaclar)
fonk.temizle(ilaclar)
fonk.Tclear(ilaclar)
fonk.Eclear(ilaclar)
fonk.etiketle(ilaclar,"T")
fonk.etiketle(ilaclar,"E")
fonk.databaseSend(ilaclar)

print("Başarili")
ilac.close()
