import sqlite3,os #Sqlite import ettik ve sistem aktiviteleri için os import ettik


dosya="kitaplık.db" # Veritabanına vereceğimiz isimi bir değişkene atadık.
db=sqlite3.connect(dosya) #Veritabanına bağlandık.
cursor=db.cursor()  #İmleç oluşturmak için.

#Eğer veritabanında yazarlar adında bir tablo yoksa oluştur
cursor.execute("""CREATE TABLE IF NOT EXISTS yazarlar( 
    yazar_no INTEGER PRIMARY KEY AUTOINCREMENT, 
    yazar_adsoyad VARCHAR(50)
    )""")

#Eğer veritabanında kitaplar adında bir tablo yoksa oluştur
cursor.execute("""CREATE TABLE IF NOT EXISTS kitaplar(
    kitap_no INTEGER PRIMARY KEY AUTOINCREMENT, 
    kitap_adi VARCHAR(50), 
    stok_adet INTEGER,
    yazar VARCHAR(50)
    )""")
db.commit() #veritabanını kaydeder.






    



#Gelen parametreyi veritabanına ekler.
def yazarekle(yazaradsoyad):
    cursor.execute("""INSERT INTO yazarlar(yazar_adsoyad) VALUES (?)""",([yazaradsoyad]))
    db.commit() #kaydet
    menu() # menu fonksiyonunu çağır.

#Gelen parametreleri kitaplar tablosuna ekler.
def kitapgiris(ad,stok,yazarı):
    cursor.execute("""INSERT INTO kitaplar(kitap_adi,stok_adet,yazar) VALUES (?,?,?)""",(ad,stok,yazarı))
    db.commit()
    menu()

#Stoğu 1 azaltır (Hocam parametrenin yanına ve executede (sayi,) parametrenin ve alınacak verinin 
# yanina virgül koymadığım sürece stoğu 1 azaltmadı neden virgül koyunca çalışıyor kod? 
# Virgül koymamı bir tanıdıgım söyledi.Ama Mantığını anlamayamadım.)
def guncelle(sayi,):
    cursor.execute("UPDATE kitaplar SET stok_adet=stok_adet-1 WHERE kitap_no = (?)", (sayi,) )
    db.commit()
    menu()


def menu():  #Menü Fonksiyonu
    print("\nHOSGELDİNİZ.\nLÜTFEN YAPMAK İSTEDİĞİNİZ İŞLEMİN BAŞ HARFİNİ TUŞLAYIN"+
    "\n[Y]azar Girişi       [K]itap Girişi      [A]rama     [S]atış     [Q]uit\n")


    secim=input(str("Lütfen Yapmak İstediğiniz işlemin baş harfini seçin\n : "))#Kullanıcıdan str türünde veri alma

    if (secim=="Q" or secim=="q"):#Kullanıcı q harfine bastığı zaman veritabanını kaydet ve çıkış yap.
        db.commit()
        os._exit(0)


    if(secim=="Y" or secim=="y"):
        try:# Error Handling icin try except bloklarini kullandım.
            yazarisim=input(str("Lütfen İsim Soyisim Giriniz : "))#Kullanıcıdan string veri alındıp değişkene atandı.
            yazarekle(yazarisim)#Kullanıcıdan Alınan kelime yazarekle fonksiyonuna parametre olarak gitti.
        except Exception as hata:#Hata varsa Ekrana basılacak.
            db.rollback()#Veritabanına Girdileri Geri al.
            print("Yazar Girişinde Hata oluştu.Hata kodu = "+str(hata))
        finally:
            db.close()#Veritabanını kapat.
        

    elif(secim =="K" or secim=="k"):
        try:
            kitapadi=input(str("Kitap Adı Giriniz :"))#Kullanıcıdan gerekli bilgiler alınıp değişkenlere atandı.
            stokadet=int(input("Stok Adedi Giriniz :"))
            cursor.execute("SELECT * FROM yazarlar")#Veritabanındaki yazarlar seçildi.
            yazar_adi=cursor.fetchall()#Veritabanındaki seçilen yazarlar değişkeneatandı.
            for i in yazar_adi:#Veritabanındaki yazarlar for döngüsü ile listelendi.
                print(i)
            yazarsecim=int(input("Yazar Numarası Seçiniz :"))#Kullanıcıdan Yazar Numarası istedik.
            cursor.execute("SELECT * FROM yazarlar")#Yazarlar tablosundaki bütün bilgileri aldık.
            yazarlar=cursor.fetchall()#Yazarlar tablosundaki bütün bilgileri aldık ve bir değişkene atadık.
            secilenyazar=yazarlar[yazarsecim-1][1]#Seçimin Düzgün Kaydedilebilmesi İçin Kullanıcıdan aldığım sayiyi 1 azalttım.
            #yazarlar[id][isim] olduğu için id-1 yaptım  Dan Başlıyor Id ler.
            print(secilenyazar)
            kitapgiris(kitapadi,stokadet,secilenyazar)#kitapgiris fonksiyonuna parametreleri yolladım.
        except Exception as hata:#Hata varsa aşağıdaki işlemler uygulanacak bir önceki if blogunda açıkladım.
            db.rollback()
            print("Kitap Girişinde Hata oluştu.Hata kodu = "+str(hata))
        finally:
            db.close()
        


    elif(secim =="S" or secim=="s"):#Secim s ise
        try:    
            print("\t\tNo\t\tKitap Adı\t\tKitap Yazarı\t\tStok\t\t") #Ekrana yazılacaklar.

            cursor.execute("SELECT * FROM kitaplar ORDER by kitap_adi")#Kitaplar tablosundaki bütün bilgileri kitap ismi
            #sıralamasına göre al.
            listele =cursor.fetchall()#Alınan bilgileri fethall() ile değişkene atadım.
            for i in listele:#for döngüsü ile yukarıdaki print sırasına uyacak şekilde yazdııyorum.
                print("\t\t"+str(i[0])+"\t\t"+i[1]+"\t\t"+i[3]+"\t\t"+str(i[2])+"\t\t")

            satilacak=int(input("Satilacak Kitap No Giriniz : "))#Satılacak kitap numarası alıyorum.
            guncelle(satilacak)#Güncelle fonksiyonuna parametre olarak yolluyorum.
        except Exception as hata:#hata varsa...
            db.rollback()
            print("Satış İşleminde Hata oluştu.Hata kodu = "+str(hata))
        finally:
            
            db.close()
        
    
    elif(secim=="A" or secim=="a"):
        try:
            ara=input(str("Kitap Adı veya Yazar Adını Eksiksiz Giriniz : "))#Aranacak kelime alıyorum.
            cursor.execute("SELECT * FROM kitaplar where kitap_adi =(?)",([ara]))#Yapılacak işlemler if bloğunun 
            #içinde de tanımlanabileceğini göstermek için fonksiyon oluşturmadım bu işleme.Burada Girilen kelimeyi
            #Kitaplar tablosunun kitap_adı kolonunda arıyor.
            aramasonucu_kitap=cursor.fetchall()#Bulunan Değerleri değişkene atıyorum.
            for i in aramasonucu_kitap:#for döngüsü ile sonucu yazdırıyorum.
                print(i)
            cursor.execute("SELECT * FROM kitaplar where yazar = (?)",([ara]))#Girlen kelimeyi yazar kolonunda arıyor.
            aramasonucu_yazar=cursor.fetchall()
            for i in aramasonucu_yazar:#Bulunan değerleri for döngüsüne atıp ekrana yazdırıyor.
                print(i)
        except Exception as hata:#Hata varsa...
            db.rollback()
            print("Arama İşleminde Hata oluştu.Hata kodu = "+str(hata))
        finally:
            
            db.close()
            menu()
        

    
        

menu()#Menü Fonksiyonunu çağırıyor.


