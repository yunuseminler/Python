#32 den kısa uzunluklu binary verinin uzunluğunu 32 bit yapan fonksiyon
def checklenght(n):
    if(len(n)<32):
        for x in range(32-len(n)):
            n = "0" + n
    return n
#Binary verinin modulo 2^32 ile hesaplanması
def check(s):
    while(s > (4294967296)):
        s = s - 4294967296
    n = format(s, '08b')
    return checklenght(n)
#32 bitlik  binary veriyi not operatoru  ile hesaplayan fonksiyon
def ournot(x):
    s=""
    for z in range(len(x)):
        if(int(x[z],2) == 1):
            s = s + format(0,'01b')
        else:
            s = s + format(1,'01b')
    return s
#32 bitlik 2 binary veri arasında  xor hesaplayan fonksiyon
def ourxor(x,y):
    s=""
    for i in range(32):
        a = int(x[i])
        b = int(y[i])
        if(a == 1 and b == 1):
            s = s + "0" 
        elif(a == 0 and b == 0):
            s = s + "0"
        elif(a == 1 and b == 0):
            s = s + "1"
        elif(a == 0 and b == 1):
            s = s + "1"     
    return s
#32 bitlik 2 binary veri arasında and operatoru hesaplayan fonksiyon
def ourand(x,y):
    s=""
    for z in range(32):
        s = s + format(int(x[z],2)& int(y[z],2),'01b')
    return s
#Kendi oluşturduğumuz righRotate fonksiyonu
def rightRotate(lists, num):
    output_list = []
    temp = list(lists)
    for item in range(len(temp) - num, len(temp)):
        output_list.append(temp[item])
 
    for item in range(0, len(temp) - num):
        output_list.append(temp[item])
    
    s1=""
    for x in range(32):
        s1 = s1 + output_list[x]
    return s1

#Sabitler
h = ["0x6a09e667",
    "0xbb67ae85",
    "0x3c6ef372",
    "0xa54ff53a",
    "0x510e527f",
    "0x9b05688c",
    "0x1f83d9ab",
    "0x5be0cd19"]
constsK = ("0x428a2f98", "0x71374491", "0xb5c0fbcf", "0xe9b5dba5", "0x3956c25b", "0x59f111f1", "0x923f82a4", "0xab1c5ed5",
   "0xd807aa98", "0x12835b01", "0x243185be", "0x550c7dc3", "0x72be5d74", "0x80deb1fe", "0x9bdc06a7", "0xc19bf174",
   "0xe49b69c1", "0xefbe4786", "0x0fc19dc6", "0x240ca1cc", "0x2de92c6f", "0x4a7484aa", "0x5cb0a9dc", "0x76f988da",
   "0x983e5152", "0xa831c66d", "0xb00327c8", "0xbf597fc7", "0xc6e00bf3", "0xd5a79147", "0x06ca6351", "0x14292967",
   "0x27b70a85", "0x2e1b2138", "0x4d2c6dfc", "0x53380d13", "0x650a7354", "0x766a0abb", "0x81c2c92e", "0x92722c85",
   "0xa2bfe8a1", "0xa81a664b", "0xc24b8b70", "0xc76c51a3", "0xd192e819", "0xd6990624", "0xf40e3585", "0x106aa070",
   "0x19a4c116", "0x1e376c08", "0x2748774c", "0x34b0bcb5", "0x391c0cb3", "0x4ed8aa4a", "0x5b9cca4f", "0x682e6ff3",
   "0x748f82ee", "0x78a5636f", "0x84c87814", "0x8cc70208", "0x90befffa", "0xa4506ceb", "0xbef9a3f7", "0xc67178f2")



#Girdi alınıyor ve binary dönüştürülüyor
text = input("Şifrelemek istediğiniz metni giriniz: ")
textBinary = ''.join(format(ord(i), '08b') for i in text)

#Binary sonuna 1 ekleniyor
textBinary = textBinary+"1"

#Uzunluğu 512 bit sayısına tam bölünecek şekilde 0 ile dolduruluyor.
temp = 448-(len(textBinary)%512)
for x in range(temp):
    textBinary = textBinary + "0"

#Son satıra girilen karakter uzunluğu yazılıyor
textLenBinary = ''.join(format((len(text)*8), '08b'))
temp1 = 64-(len(textLenBinary))
for y in range(temp1):
    textLenBinary = "0" + textLenBinary
textBinary = textBinary + textLenBinary

#Girilen verinin son hali 512 bitlik parçalara bölünüyor.
chunks = []
temp= ""
for k in range(len(textBinary)):
    temp = temp + textBinary[k]
    if((k+1)%512 == 0):
        chunks.append(temp)
        temp = "" 

words = []
#Her 512 bitlik parça için işlem yapılıyor
for y in range(len(chunks)):
    #512 bitlik parça 32 bitlik alt parçalara bölünüyor ve 16 alt parça elde ediliyor.
    for k in range(512):
        temp = temp + chunks[y][k]
        if((k+1)%32 == 0):
            words.append(temp)
            temp = ""
    #16 alt parça 64'e tamamlanmak için 48 adet 32 bitlik 0 lar ile dolduruluyor
    for k in range(48):
        words.append("00000000000000000000000000000000")
        
    #16 dan 64 e kadar doldurduğumuz 0 lara işlem yapıyoruz.
    for i in range(16,64):
        #s0 Hesaplanması
        s0= ourxor(ourxor(checklenght(rightRotate(words[i-15],7)),checklenght(rightRotate(words[i-15],18))),checklenght(format(int(words[i-15],2) >> 3,'08b')))
        #S1 Hesaplanması
        s1= ourxor(ourxor(checklenght(rightRotate(words[i-2],17)),checklenght(rightRotate(words[i-2],19))),checklenght(format(int(words[i-2],2) >> 10,'08b')))
        #words[i] hesaplaması
        result = int(words[i-16],2) + int(s0,2) + int(words[i-7],2) + int(s1,2)
        words[i] = check(result)
    #H sabitlerinin binary dönüştürülmesi
    hList = []
    for kk in range(8):
        hList.append(checklenght(format((int(h[kk], base=16)), '08b')))

    #0'lara işlem yapıldıktan sonra bütün parçalara işlem yapılıyor.
    for i in range(64):
        #S1 Hesaplanması
        s1 = ourxor(ourxor((checklenght(rightRotate(hList[4],6))),(checklenght(rightRotate(hList[4],11)))),(checklenght(rightRotate(hList[4],25))))
        #CH Hesaplaması
        ch = ourxor(ourand(hList[4],hList[5]),(ourand(ournot(hList[4]) , hList[6])))
        #temp1 Hesaplaması
        temp1 = int(check(int(hList[7],2) + int(s1,2) + int(ch,2) + int(constsK[i],base=16) + int(words[i],2)),2)
        #S0 Hesaplaması
        s0 = ourxor(ourxor((checklenght(rightRotate(hList[0],2))),(checklenght(rightRotate(hList[0],13)))),(checklenght(rightRotate(hList[0],22))))
        #maj Hesaplaması
        maj = int((ourand(hList[0],hList[1])),2) ^ int(ourand(hList[0],hList[2]),2) ^int(ourand(hList[1],hList[2]),2)
        #temp2 Hesaplaması
        temp2 = int(check(int(s0,2) + maj),2)

        #H sabitlerinin listesi kopyalanıyor.
        hList_ = hList.copy()
        #H sabitlerinin yeni değerleri hesaplanıyor
        hList[0] = check(temp1 + temp2)
        hList[1] = hList_[0]
        hList[2] = hList_[1]
        hList[3] = hList_[2]
        hList[4] = check(int(hList_[3],2) + temp1)
        hList[5] = hList_[4]
        hList[6] = hList_[5]
        hList[7] = hList_[6]

    #H sabitlerinin her 512 parça için son değerlerinin hesaplanması
    for kk in range(8):
        h[kk] = hex(int(check(int(h[kk], base=16) + int(hList[kk],2)),2))
    words = []

#Şifrelenmis Hash kodunun birleştirililerek ortaya çıkarılması
hash = ""
for kk in range(8):
    hash = hash + h[kk][2::]
print("Şifrelenmiş Hash Kodu: " + hash)

k = input("Program Sonlandi kapatmak için bir tusa basin")