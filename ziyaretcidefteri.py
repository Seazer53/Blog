from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = "çok gizli"


@app.route("/", methods=["GET", "POST"])
def girisyap():
    return render_template("girisyap.html")


@app.route("/kontrol", methods=["GET", "POST"])
def kontrol():
    kullanici_adi = request.form["email"]
    sifre = request.form["password"]

    dosya = open("veri.txt", "r", encoding="utf-8")
    tum_dosya = dosya.readlines()
    dosya.close()

    sifre_dogru = False
    liste_bilgi = []

    for x in tum_dosya:
        suanki_satir = x[0:len(x) - 1]
        liste_bilgi.append(suanki_satir)

    print(liste_bilgi)

    for i in range(len(liste_bilgi)):
        if liste_bilgi[i] == kullanici_adi:
            if sifre == liste_bilgi[i + 1]:
                sifre_dogru = True
                break

    if sifre_dogru != True:
        error = "Kullanıcı adı ya da şifre hatalı"
        return render_template("girisyap.html", error=error)

    else:
        session["kullanici_adi"] = kullanici_adi
        email = session["kullanici_adi"]
        return render_template("anasayfa.html", email=email)


@app.route("/home", methods=["GET", "POST"])
def anasayfa():
    return render_template("anasayfa.html")


@app.route("/kaydet", methods=["GET", "POST"])
def mesaj_kaydet():
    mesaj = request.form["msj"]
    dosya = open("mesajlar.txt", "a", encoding="utf-8")
    dosya.write(mesaj)
    dosya.write("\n")
    dosya.close()
    return redirect("/mesajlar")


@app.route("/mesajlar/<sayfano>", methods=["GET", "POST"])
def mesaj_listele(sayfano):
    max_kayit = 10
    dosya = open("mesajlar.txt", "r", encoding="utf-8")
    tum_dosya = dosya.readlines()
    dosya.close()
    mesajlar = tersini_bul(tum_dosya)

    baslangic = (int(sayfano) - 1) * max_kayit
    busayfa = mesajlar[baslangic:baslangic + max_kayit]

    i = 0

    for m in busayfa:
        mesajr = []
        mesajr.append(str(((int(sayfano) - 1) * max_kayit) + i + 1))
        mesajr.append(m)
        busayfa[i] = mesajr
        i = i + 1

    sayfa_sayisi = (len(mesajlar) // max_kayit) + 1
    return render_template("mesaj.html", mesajlar=busayfa, sayfasayisi=sayfa_sayisi)


def tersini_bul(liste):
    ters_liste = []
    for x in range(len(liste)-1, -1, -1):
        ters_liste.append(liste[x])

    return ters_liste


@app.route("/aramasonuclari", methods=["GET", "POST"])
def arama():
    aranan = request.form['aranan']
    print(aranan)

    dosya = open("mesajlar.txt", "r", encoding='utf-8')
    mesajlar = tersini_bul(dosya.readlines())
    dosya.close()
    bulunanlar = []

    for m in mesajlar:
        if aranan in m:
            liste = []
            ilkbulunanyer = m.find(aranan, 0)
            kaldigimizyer = 0

            while ilkbulunanyer > -1:
                if ilkbulunanyer > kaldigimizyer:
                    liste.append(m[kaldigimizyer:ilkbulunanyer])

                liste.append(aranan)

                kaldigimizyer = ilkbulunanyer + len(aranan)
                ilkbulunanyer = m.find(aranan, kaldigimizyer)

            liste.append(m[kaldigimizyer:len(m)])

            bulunanlar.append(liste)
    return render_template("aramasonucu.html", mesajlar=bulunanlar, aranan=aranan)


@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    return render_template("kayitol.html")


@app.route("/kayitkontrol", methods=["GET", "POST"])
def kayitkontrol():
    email = request.form["email"]
    sifre = request.form["pwd"]
    sifre2 = request.form["pwd2"]

    if sifre == sifre2:
        dosya = open("veri.txt", "a", encoding="utf-8")
        dosya.write(email)
        dosya.write("\n")
        dosya.write(sifre)
        dosya.write("\n")
        dosya.close()
        basarili = email + " email adresli hesabınız başarıyla oluşturuldu"
        return render_template("girisyap.html", basarili=basarili)

    else:
        hata = "Şifreler eşleşmiyor!"
        return render_template("kayitol.html", hata=hata)


@app.route('/tekmesajgoster/<satirno>/<mesaj>', methods=["GET"])
def tek_mesaj_goster(satirno, mesaj):
    return render_template("tekmesaj.html", satirno=satirno, mesajr=mesaj)

@app.route('/guncelle', methods=["POST"])
def guncelle():
    satirno = request.form["satirno"]
    mesaj = request.form["mesaj"]

    dosya = open("mesajlar.txt", "r")
    tum_dosya = tersini_bul(dosya.readlines())

    dosya.close()

    yeni_dosya = open("mesajlar2.txt", "w")
    satir = 1

    for x in tum_dosya:
        if satir == int(satirno):
            tum_dosya.insert(satir - 1, mesaj + "\n")
            tum_dosya.remove(x)
            break

        else:
            satir += 1

    duz_tum_dosya = tersini_bul(tum_dosya)
    yeni_dosya.writelines(duz_tum_dosya)
    yeni_dosya.close()

    sonuc = "Mesajınız " + "'" + mesaj + "'" + " olarak düzenlenmiştir"

    os.remove("mesajlar.txt")
    os.rename("mesajlar2.txt", "mesajlar.txt")

    return render_template("tekmesaj.html", sonuc=sonuc)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
