import json
import random
import datetime


class uyelikSistemi():

    def __init__(self):
        self.timeout = []
        self.timeoutUye = []
        self.uyeler = []
        self.durum = True

    def menu(self):
        print("""
    ***** Local Kayıt Sistemi ****
    
1-) Giriş Yap
2-) Kayıt Ol
3-) Şifremi Unuttum
4-) Çıkış


        """)
        while True:
            try:
                secim = int(input("Seçiminizi giriniz: "))
                if secim < 1 or secim > 4:
                    raise ValueError
                break
            except:
                print("Hatalı giriş yaptınız lütfen tekrar deneyin...")

        if secim == 1:
            self.girisYap()
        if secim == 2:
            self.kayıtOl()
        if secim == 3:
            self.sifremiUnuttum()
        if secim == 4:
            print("Program sonlandırıldı...")
            self.durum = False

    def girisYap(self):
        hak = 3
        user = input("Kullanıcı Adı: ")
        password = input("Şifre: ")
        while True:
            girisDurum = self.kontrolEt(user, password)
            if girisDurum == "True":
                print(f"Giriş başarılı...\nHoşgeldiniz {user}")
                self.menu()
            elif girisDurum == "HataliSifre":
                hak -= 1
                if hak == 0:
                    print("1 saat sonra tekrar deneyiniz.")
                    self.timeoutUye.append(user)
                    an = datetime.datetime.now()
                    self.timeout.append(str(an.hour + 1) + ":" + str(an.minute))

                    print("Devredışı hesaplar: {}".format(list(zip(self.timeoutUye, self.timeout))))
                    self.menu()
                print("Hatalı şifre girdiniz!\nKalan hakkınız: {}".format(hak))
                password = input("Şifre: ")
            elif girisDurum == "Bulunamadi":
                print("Böyle bir kullanıcı sistemde kayıtlı değil!")
                self.girisYap()
            elif girisDurum == "timeout":
                print(f"Saat {self.timeout} olunca aktifleşecek!")
                self.menu()
            elif girisDurum == "aktifdegil":
                print("Hesabınız aktif değildir...")
            else:
                self.menu()

    def kontrolEt(self, user, password):
        for i in self.timeoutUye:
            if i == user:
                return "timeout"
        with open("data.json", "r", encoding="utf-8") as dosya:
            uyeler = json.load(dosya)
            for uye in uyeler["users"]:
                if uye["kadi"] == user:
                    if uye["sifre"] == password:
                        return "True"
                    else:
                        return "HataliSifre"
            return "Bulunamadi"

    def kayıtOl(self):
        # Username -> Kulanıcı adı sistemde varsa yeniden giriş istiyor
        while True:
            d = True
            user = input("Kullanıcı Adı: ")
            # Sistemde girilen kullanıcı adı var mı kontrol ediliyor
            with open("data.json", "r", encoding="utf-8") as dosya:
                kontroluyeler = json.load(dosya)
                for uye in kontroluyeler["users"]:
                    if uye["kadi"] == user:
                        print("Bu kullanıcı adı zaten kayıtlı!\nFarklı bir kullanıcı adı giriniz...")
                        d = False
                        break
            if d == True:
                break

        # Password -> Döngü eşleşen şifre girene kadar çalışır
        while True:
            password = input("Şifre: ")
            password2 = input("Şifre Tekrar: ")
            if password == password2:
                break
            else:
                print("Şifreler eşleşmiyor!\nYeniden giriniz...")

        # Mail
        while True:
            mail = input("Mail:")
            with open("OnayKodu.txt", "w") as dosya:
                kod = random.randint(100000, 1000000)
                dosya.write(f"{mail}\nMail onay kodu: {kod}")

            girilenKod = input(f"{mail} adresine gelen onay kodunu giriniz: ")

            if girilenKod == str(kod):
                with open("data.json", "r", encoding="utf-8") as dosya:
                    uyeler = json.load(dosya)
                    uyeler["users"].append({"kadi": user, "sifre": str(password), "mail": mail})
                with open("data.json", "w", encoding="utf-8") as dosya:
                    json.dump(uyeler, dosya)

                print(f"Kayıt başarılı!\n{user}")
                print(uyeler)
                break
            else:
                print("Hatalı kod!\nLütfen tekrar deneyiniz...")
        self.menu()

    def sifremiUnuttum(self):
        try:
            while True:
                kod = 0
                yaz = False
                mail = input("Mail adresinizi giriniz: ")
                # Sistemde girilen kullanıcı adı var mı kontrol ediliyor
                with open("data.json", "r", encoding="utf-8") as dosya:
                    kontroluyeler = json.load(dosya)
                    for uye in kontroluyeler["users"]:
                        if uye["mail"] == mail:
                            with open("OnayKodu.txt", "w") as dosya:
                                kod = random.randint(100000, 1000000)
                                dosya.write(f"{mail}\nMail onay kodu: {kod}")

                            girilenKod = input(f"{mail} adresine gelen onay kodunu giriniz: ")
                            if girilenKod == str(kod):
                                while True:
                                    password = input("Yeni şifre: ")
                                    password2 = input("Yeni şifre tekrar: ")
                                    if password == password2:
                                        break
                                    else:
                                        print("Şifreler eşleşmiyor!\nYeniden giriniz...")
                                uye["sifre"] = password
                                print("Kullanıcı: {} şifresi yenilendi.".format(uye["kadi"]))
                                yaz = True
                            else:
                                print("Hatalı kod!")
                                self.menu()
                if yaz == True:
                    with open("data.json", "w", encoding="utf-8") as dosya1:
                        json.dump(kontroluyeler, dosya1)
                    self.menu()
                print("Böyle bir mail adresi bulunamadı!\nLütfen tekrar deneyiniz...")
        except:
            self.menu()


uyelik = uyelikSistemi()
while uyelik.durum:
    uyelik.menu()
