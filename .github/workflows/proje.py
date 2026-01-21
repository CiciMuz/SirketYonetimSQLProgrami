from operator import truediv
from time import strftime
from tkinter.constants import INSERT
from datetime import datetime

import flet as ft
import pyodbc
from flet import Alignment

def main(page:ft.Page):
    print("naber")
    page.title = "Proje Yönetim Merkezi"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"

    baglanti_cumlesi = (
        'DRIVER={ODBC Driver 17 for SQL Server};'  
        'SERVER=.;'  
        'DATABASE=SirketYonetimDB;'  
        'Trusted_Connection=yes;'
    )

    conn = pyodbc.connect(baglanti_cumlesi)
    cursor = conn.cursor()




    def anaEkranYap():
        page.clean()
        baslik=ft.Text(value="Proje Yönetim Merkezi",text_align=ft.TextAlign.CENTER,size=30)
        calisan=ft.ElevatedButton(text="Çalışanları Görüntüle",on_click=calisan_yap)
        proje = ft.ElevatedButton(text="Projeleri Görüntüle", on_click=proje_yap )
        atama = ft.ElevatedButton(text="Atamaları Görüntüle", on_click=atama_yap)
        departman = ft.ElevatedButton(text="Departmanları Görüntüle", on_click=departman_yap)
        col = ft.Column(controls=[baslik,calisan,proje,departman,atama], alignment=ft.MainAxisAlignment.CENTER)
        row = ft.Row(controls=[col],alignment=ft.MainAxisAlignment.CENTER)
        page.add(row)

    def anaEkranYap_handler(e:None):
        anaEkranYap()


    ana_ekran_butonu = ft.ElevatedButton(text="Ana Ekran", on_click=lambda e:anaEkranYap_handler(e))



    def calisanProjeleri(e:None,ad,id):
        page.clean()
        yazi=ft.Text(value=ad+" altındaki projeler\n",max_lines=3,size=40,color="white")

        üst_row = ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje Adı"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Başlangıç Tarihi"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Planlanan Bitiş"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
        ))

        ust_container = ft.Container(content=üst_row, border=ft.border.all(width=3, color=ft.Colors.BLUE))

        def geriHandler(e: None):
            calisan_yap()

        geri_butonu = ft.ElevatedButton(text="Geri Git", bgcolor="yellow", on_click=lambda e: geriHandler(e))

        page.add(ana_ekran_butonu,geri_butonu,yazi,ust_container)

        cursor.execute("SELECT * FROM GorevAtamalari WHERE CalisanID=?",(id,))
        atamalar=cursor.fetchall()

        for veri in atamalar:
            cursor.execute("SELECT * FROM Projeler WHERE ProjeID=?",(veri[2],))
            temp=cursor.fetchone()

            id=temp[0]
            ad=temp[1]
            baslangic = temp[2].strftime("%Y-%m-%d")
            bitis = temp[3].strftime("%Y-%m-%d")

            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=baslangic), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=bitis), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ))

            page.add(temp_row)



    def projeCalisanları(e:None,ad,id):
        page.clean()
        yazi=ft.Text(value=ad+" projesi altındaki çalışanlar\n",size=20,max_lines=3,color="white")

        cursor.execute("SELECT * FROM GorevAtamalari WHERE ProjeID=?",(id,))
        atamalar=cursor.fetchall()

        üst_row = ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Çalışan ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Ad"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Soyad"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Pozisyon"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Maaş(TL)"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Departman Adı"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
        ))

        ust_container = ft.Container(content=üst_row, border=ft.border.all(width=3, color=ft.Colors.BLUE))

        def geriHandler(e: None):
            proje_yap()

        geri_butonu = ft.ElevatedButton(text="Geri Git", bgcolor="yellow", on_click=lambda e: geriHandler(e))

        page.add(ana_ekran_butonu, geri_butonu, ust_container)

        for veri in atamalar:
            cursor.execute("SELECT * FROM Calisanlar WHERE CalisanID=?",(veri[1],))
            calisanlar=cursor.fetchone()

            id=calisanlar[0]
            ad=calisanlar[1]
            soyad=calisanlar[2]
            pozisyon=calisanlar[3]
            maas=calisanlar[4]
            departmanadi=calisanlar[5]

            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=soyad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=pozisyon), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=maas), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=departmanadi), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ))

            temp_container = ft.Container(content=temp_row, border=ft.border.all(width=2, color="grey"), height=50)

            page.add(temp_container)







    def calisan_duzenleyici(e: None,CalisanID,Ad,Soyad,Pozisyon,Maas,Key):
        page.clean()
        def calisan_duzenleyici_handler(e: None, kontrol):
            if kontrol is True:
                if adKutusu.value == "" or soyadKutusu.value == "" or pozisyonKutusu.value == "" or maasKutusu.value == "" or departmanSecici.value == None:
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("UPDATE Calisanlar SET Ad=?, Soyad=?, Pozisyon=?,Maas=? WHERE CalisanID=?",
                               (adKutusu.value, soyadKutusu.value, pozisyonKutusu.value, int(maasKutusu.value),
                                CalisanID))
                conn.commit()
                calisan_yap()
            else:
                calisan_yap()

        uyarıMetni = ft.Text(value="Kutulardan biri ya da daha fazlası boş.", visible=False,color="red")
        adKutusu = ft.TextField(hint_text="Ad",value=Ad)
        soyadKutusu = ft.TextField(hint_text="Soyad",value=Soyad)
        pozisyonKutusu = ft.TextField(hint_text="Pozisyon",value=Pozisyon)
        maasKutusu = ft.TextField(hint_text="Maaş",value=Maas, input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string=""
        ))


        departmanSecici = ft.Dropdown(
            hint_text="Bir departman seçiniz",
            options=[],
            width=300,

        )

        cursor.execute("SELECT * FROM Departmanlar")
        departman_tablo = cursor.fetchall()

        for veri in departman_tablo:
            temp_secenek = ft.DropdownOption(key=str(veri.DeptID), text=veri.DepartmanAdi)
            departmanSecici.options.append(temp_secenek)

        departmanSecici.value=str(Key)

        eklemeButonu = ft.ElevatedButton(text="Ekle", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: calisan_duzenleyici_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="iptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: calisan_duzenleyici_handler(e, kontrol))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            soyadKutusu,
            pozisyonKutusu,
            maasKutusu,
            departmanSecici,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)

    def calisan_ekleyici(e:None):
        page.clean()
        def calisan_ekleyici_handler(e:None,kontrol):
            if kontrol is True:
                if adKutusu.value == "" or soyadKutusu.value == "" or pozisyonKutusu.value == "" or maasKutusu.value == "" or departmanSecici.value == None:
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("INSERT INTO Calisanlar (Ad, Soyad, Pozisyon, Maas, DeptID) VALUES (?, ?, ?, ?, ?)", (adKutusu.value,soyadKutusu.value,pozisyonKutusu.value,int(maasKutusu.value),departmanSecici.value))
                conn.commit()
                calisan_yap()
            else:
                calisan_yap()


        uyarıMetni=ft.Text(value="Kutulardan biri ya da daha fazlası boş.",visible=False,color="red")
        adKutusu=ft.TextField(hint_text="Ad")
        soyadKutusu=ft.TextField(hint_text="Soyad")
        pozisyonKutusu=ft.TextField(hint_text="Pozisyon")
        maasKutusu=ft.TextField(hint_text="Maaş",input_filter=ft.InputFilter(
        allow=True,
        regex_string=r"[0-9]",
        replacement_string=""
    ))


        departmanSecici=ft.Dropdown(
            hint_text="Bir departman seçiniz",
            options=[],
            width=300
        )

        cursor.execute("SELECT * FROM Departmanlar")
        departman_tablo = cursor.fetchall()

        for veri in departman_tablo:
            temp_secenek=ft.DropdownOption(key=str(veri.DeptID),text=veri.DepartmanAdi)
            departmanSecici.options.append(temp_secenek)

        eklemeButonu=ft.ElevatedButton(text="Ekle",bgcolor="green",color="white",on_click=lambda e,kontrol=True:calisan_ekleyici_handler(e,kontrol))
        iptalButonu = ft.ElevatedButton(text="iptal", bgcolor="red", color="white",on_click=lambda e,kontrol=False:calisan_ekleyici_handler(e,kontrol))

        anaColumn=ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            soyadKutusu,
            pozisyonKutusu,
            maasKutusu,
            departmanSecici,
            eklemeButonu,
            iptalButonu
        ])

        ana_container=ft.Container(content=anaColumn,visible=False)
        ana_container.visible=True
        page.add(ana_container)



    def calisan_silici(e:None,id):
        cursor.execute("DELETE FROM GorevAtamalari WHERE CalisanID = ?", (id,))
        conn.commit()

        cursor.execute("DELETE FROM Calisanlar WHERE CalisanID = ?", (id,))
        conn.commit()
        calisan_yap()

    def calisan_yap(e=None):
        page.clean()
        cursor.execute("SELECT * FROM Calisanlar")
        calisan_tablo=cursor.fetchall()
        cursor.execute("SELECT * FROM Departmanlar")
        departman_tablo = cursor.fetchall()

        ekle_butonu=ft.ElevatedButton(text="Çalışan Ekle",bgcolor="green",color="white",on_click=lambda e:calisan_ekleyici(e))


        üst_row=ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Çalışan ID"),width=100),
            ft.Container(width=1,height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Ad"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Soyad"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Pozisyon"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Maaş(TL)"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Departman Adı"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
        ))

        ust_container=ft.Container(content=üst_row,border=ft.border.all(width=3, color=ft.Colors.BLUE))


        page.add(ana_ekran_butonu,ekle_butonu, ust_container)

        for veri in calisan_tablo:
            id=veri[0]
            ad=veri[1]
            soyad=veri[2]
            pozisyon=veri[3]
            maas=veri[4]
            departman=cursor.execute("SELECT * FROM Departmanlar WHERE DeptID=?",(veri[5],)).fetchall()
            departmanadi=departman[0].DepartmanAdi if departman else "NULL"
            calisan_sil=ft.ElevatedButton(text="Çalışanı Sil",bgcolor="red",color="white",on_click=lambda e,gonder=id: calisan_silici(e,gonder))


            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=soyad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=pozisyon), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=maas), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=departmanadi), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                calisan_sil,
                ft.ElevatedButton(text="Çalışanı düzenle",bgcolor="blue",on_click=lambda e,CalisanID=id,Ad=ad,Soyad=soyad,Pozisyon=pozisyon,Maas=maas,Key=veri[5]: calisan_duzenleyici(e,CalisanID,Ad,Soyad,Pozisyon,Maas,Key)),
                ft.ElevatedButton(text="Çalışanın Projeleri",bgcolor="yellow",on_click=lambda e,Ad=ad,ID=id: calisanProjeleri(e,Ad,ID))
            ))

            temp_container=ft.Container(content=temp_row,border=ft.border.all(width=2, color="grey"), height=50)

            page.add(temp_container)

    def proje_duzenleyici(e: None,ProjeID,Ad,BaslangicTarihi,BitisTarihi):
        page.clean()

        baslangic_objesi = BaslangicTarihi
        bitis_objesi = BitisTarihi

        def proje_duzenleyici_handler(e: None, kontrol):
            if kontrol is True:
                if adKutusu.value == "" or baslangicKutusu.value == "" or bitisKutusu.value == "":
                    uyarıMetni.value = "Kutulardan biri ya da daha fazlası boş."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                try:
                    baslangic_objesi = datetime.strptime(baslangicKutusu.value, "%d.%m.%Y").date()
                    bitis_objesi = datetime.strptime(bitisKutusu.value, "%d.%m.%Y").date()
                except ValueError:
                    uyarıMetni.value = "Tarih formatını hatalı girdiniz. Örnek: 01.01.2000"
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("UPDATE Projeler SET ProjeAdi=?, BaslangicTarihi=?, BitisTarihi=? WHERE ProjeID=?",
                               (adKutusu.value, baslangic_objesi, bitis_objesi, ProjeID))
                conn.commit()
                proje_yap()
            else:
                proje_yap()

        uyarıMetni = ft.Text(value="Kutulardan biri ya da daha fazlası boş.", visible=False, color=ft.Colors.RED)
        adKutusu = ft.TextField(hint_text="Proje Adı",value=Ad)
        baslangicKutusu = ft.TextField(hint_text="Başlangıç Tarihi",value= baslangic_objesi.strftime("%d.%m.%Y"))
        bitisKutusu = ft.TextField(hint_text="Bitiş Tarihi",value= bitis_objesi.strftime("%d.%m.%Y"))

        eklemeButonu = ft.ElevatedButton(text="Ekle", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: proje_duzenleyici_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="iptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: proje_duzenleyici_handler(e, kontrol))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            baslangicKutusu,
            bitisKutusu,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)



    def proje_ekleyici(e:None):
        page.clean()

        baslangic_objesi = datetime.strptime("01.01.2000", "%d.%m.%Y").date()
        bitis_objesi = datetime.strptime("01.01.2000", "%d.%m.%Y").date()

        def proje_ekleyici_handler(e:None,kontrol):
            if kontrol is True:
                if adKutusu.value == "" or baslangicKutusu.value == "" or bitisKutusu.value == "" :
                    uyarıMetni.value = "Kutulardan biri ya da daha fazlası boş."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                try:
                    baslangic_objesi = datetime.strptime(baslangicKutusu.value, "%d.%m.%Y").date()
                    bitis_objesi = datetime.strptime(bitisKutusu.value, "%d.%m.%Y").date()
                except ValueError:
                    uyarıMetni.value = "Tarih formatını hatalı girdiniz. Örnek: 01.01.2000"
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("INSERT INTO Projeler (ProjeAdi, BaslangicTarihi, BitisTarihi) VALUES (?, ?, ?)", (adKutusu.value,baslangic_objesi,bitis_objesi))
                conn.commit()
                proje_yap()
            else:
                proje_yap()


        uyarıMetni=ft.Text(value="Kutulardan biri ya da daha fazlası boş.",visible=False,color=ft.Colors.RED)
        adKutusu=ft.TextField(hint_text="Proje Adı")
        baslangicKutusu=ft.TextField(hint_text="Başlangıç Tarihi")
        bitisKutusu=ft.TextField(hint_text="Bitiş Tarihi")

        departmanSecici=ft.Dropdown(
            hint_text="Bir departman seçiniz",
            options=[],
            width=300
        )

        cursor.execute("SELECT * FROM Departmanlar")
        departman_tablo = cursor.fetchall()

        for veri in departman_tablo:
            temp_secenek=ft.DropdownOption(key=str(veri.DeptID),text=veri.DepartmanAdi)
            departmanSecici.options.append(temp_secenek)

        eklemeButonu=ft.ElevatedButton(text="Ekle",bgcolor="green",color="white",on_click=lambda e,kontrol=True:proje_ekleyici_handler(e,kontrol))
        iptalButonu = ft.ElevatedButton(text="iptal", bgcolor="red", color="white",on_click=lambda e,kontrol=False:proje_ekleyici_handler(e,kontrol))

        anaColumn=ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            baslangicKutusu,
            bitisKutusu,
            eklemeButonu,
            iptalButonu
        ])

        ana_container=ft.Container(content=anaColumn,visible=False)
        ana_container.visible=True
        page.add(ana_container)



    def proje_silici(e:None,id):
        cursor.execute("DELETE FROM GorevAtamalari WHERE ProjeID = ?", (id,))
        conn.commit()

        cursor.execute("DELETE FROM Projeler WHERE ProjeID = ?", (id,))
        conn.commit()
        calisan_yap()




    def proje_yap(e=None):
        page.clean()
        cursor.execute("SELECT * FROM Projeler")
        proje_tablo=cursor.fetchall()

        ekle_butonu=ft.ElevatedButton(text="Proje Ekle",bgcolor="green",color="white",on_click=lambda e:proje_ekleyici(e))


        üst_row=ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje ID"),width=100),
            ft.Container(width=1,height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje Adı"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Başlangıç Tarihi"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Planlanan Bitiş"),width=100),
            ft.Container(width=1, height=30,border=ft.border.all(width=1, color="grey")),
        ))

        ust_container=ft.Container(content=üst_row,border=ft.border.all(width=3, color=ft.Colors.BLUE))


        page.add(ana_ekran_butonu,ekle_butonu, ust_container)

        for veri in proje_tablo:
            id=veri[0]
            ad=veri[1]
            baslangic=veri[2]
            bitis=veri[3]
            proje_sil=ft.ElevatedButton(text="Projeyi Sil",bgcolor="red",color="white",on_click=lambda e,gonder=id: proje_silici(e,gonder))


            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=baslangic), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=bitis), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                proje_sil,
                ft.ElevatedButton(text="Projeyi düzenle", bgcolor="blue",
                                  on_click=lambda e, ProjeID=id, ProjeAdi=ad, BaslagicTarihi=baslangic, BitisTarihi=bitis: proje_duzenleyici(e, ProjeID, ProjeAdi, BaslagicTarihi, BitisTarihi)),
                ft.ElevatedButton(text="Projenin Çalışanları",bgcolor="yellow",color="black", on_click=lambda e, AD=ad,ID=id:projeCalisanları(e,AD,ID))

            ))

            temp_container=ft.Container(content=temp_row,border=ft.border.all(width=2, color="grey"), height=50)

            page.add(temp_container)

    def departman_duzenleyici(e: None,DeptID,Ad):
        page.clean()

        def departman_duzenleyici_handler(e: None, kontrol):
            if kontrol is True:
                if adKutusu.value == "":
                    uyarıMetni.value = "Ad kutusu boş olamaz."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("UPDATE Departmanlar SET DeptAdi=? WHERE DeptID=?",
                               (adKutusu.value, DeptID))
                conn.commit()
                departman_yap()
            else:
                departman_yap()

        uyarıMetni = ft.Text(value="Ad kutusu boş olamaz.", visible=False, color=ft.Colors.RED)
        adKutusu = ft.TextField(hint_text="Departman Adı",value=Ad)

        eklemeButonu = ft.ElevatedButton(text="Kaydet", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: departman_duzenleyici_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="İptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: departman_duzenleyici_handler(e, kontrol))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)

    def departman_ekleyici(e: None):
        page.clean()

        def departman_ekleyici_handler(e: None, kontrol):
            if kontrol is True:
                if adKutusu.value == "":
                    uyarıMetni.value = "Ad boş olamaz."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("INSERT INTO Departmanlar (DepartmanAdi) VALUES (?)",
                               (adKutusu.value))
                conn.commit()
                departman_yap()
            else:
                departman_yap()

        uyarıMetni = ft.Text(value="Ad boş olamaz.", visible=False, color=ft.Colors.RED)
        adKutusu = ft.TextField(hint_text="Departman Adı")


        eklemeButonu = ft.ElevatedButton(text="Ekle", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: departman_ekleyici_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="iptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: departman_ekleyici_handler(e, kontrol))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            adKutusu,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)

    def departman_silici(e: None, id):


        cursor.execute("UPDATE Calisanlar SET DeptID = ? WHERE DeptID=?", (None,id,))
        conn.commit()

        cursor.execute("DELETE FROM Departmanlar WHERE DeptID = ?", (id,))
        conn.commit()
        calisan_yap()

    def departman_yap(e=None):
        page.clean()
        cursor.execute("SELECT * FROM Departmanlar")
        departman_tablo = cursor.fetchall()

        ekle_butonu = ft.ElevatedButton(text="Departman Ekle", bgcolor="green", color="white",
                                        on_click=lambda e: departman_ekleyici(e))

        üst_row = ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Departman ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Departman Adı"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
        ))

        ust_container = ft.Container(content=üst_row, border=ft.border.all(width=3, color=ft.Colors.BLUE))

        page.add(ana_ekran_butonu, ekle_butonu, ust_container)

        for veri in departman_tablo:
            id = veri[0]
            ad = veri[1]
            departman_sil = ft.ElevatedButton(text="Departmanı Sil", bgcolor="red", color="white",
                                          on_click=lambda e, gonder=id: departman_silici(e, gonder))

            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                departman_sil,
                ft.ElevatedButton(text="Departmanı düzenle", bgcolor="blue",
                                  on_click=lambda e, DeptID=id, DepartmanAdi=ad: departman_duzenleyici(e, DeptID, DepartmanAdi))

            ))

            temp_container = ft.Container(content=temp_row, border=ft.border.all(width=2, color="grey"), height=50)

            page.add(temp_container)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def atama_ekleyici_id(e: None):
        page.clean()

        def atama_ekleyici_id_handler(e: None, kontrol):
            if kontrol is True:
                if calisanIDkutusu.value == "" or projeSecici.value == None:
                    uyarıMetni.value = "Kutular boş olamaz."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("INSERT INTO GorevAtamalari (CalisanID,ProjeID) VALUES (?,?)",
                               (calisanIDkutusu.value, projeSecici.value))
                conn.commit()
                atama_yap()
            else:
                atama_yap()

        uyarıMetni = ft.Text(value="Kutular boş olamaz.", visible=False, color=ft.Colors.RED)

        calisanIDkutusu=ft.TextField(hint_text="Çalışanın ID'sini yazınız")

        projeSecici = ft.Dropdown(
            hint_text="Bir proje seçiniz",
            options=[],
            width=300
        )

        cursor.execute("SELECT * FROM Projeler")
        proje_tablo = cursor.fetchall()

        for veri in proje_tablo:
            temp_secenek = ft.DropdownOption(key=str(veri.ProjeID), text=veri.ProjeAdi)
            projeSecici.options.append(temp_secenek)

        eklemeButonu = ft.ElevatedButton(text="Ekle", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: atama_ekleyici_id_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="İptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: atama_ekleyici_id_handler(e, kontrol))

        degistirButonu=ft.ElevatedButton(text="Bunun yerine çalışan ismi seçerek ekleyin...", bgcolor="blue", color="white",on_click=lambda e: atama_ekleyici(e))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            degistirButonu,
            calisanIDkutusu,
            projeSecici,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)



    def atama_ekleyici(e: None):
        page.clean()

        def atama_ekleyici_handler(e: None, kontrol):
            if kontrol is True:
                if calisanSecici.value == None or projeSecici.value == None:
                    uyarıMetni.value = "Kutular boş olamaz."
                    uyarıMetni.visible = True
                    ana_container.update()
                    return
                cursor.execute("INSERT INTO GorevAtamalari (CalisanID,ProjeID) VALUES (?,?)",
                               (calisanSecici.value, projeSecici.value))
                conn.commit()
                atama_yap()
            else:
                atama_yap()

        uyarıMetni = ft.Text(value="Kutular boş olamaz.", visible=False, color=ft.Colors.RED)

        calisanSecici = ft.Dropdown(
            hint_text="Bir çalışan seçiniz",
            options=[],
            width=300
        )

        cursor.execute("SELECT * FROM Calisanlar")
        calisan_tablo = cursor.fetchall()

        for veri in calisan_tablo:
            temp_secenek = ft.DropdownOption(key=str(veri.CalisanID), text=veri.Ad + " " + veri.Soyad)
            calisanSecici.options.append(temp_secenek)

        projeSecici = ft.Dropdown(
            hint_text="Bir proje seçiniz",
            options=[],
            width=300
        )

        cursor.execute("SELECT * FROM Projeler")
        proje_tablo = cursor.fetchall()

        for veri in proje_tablo:
            temp_secenek = ft.DropdownOption(key=str(veri.ProjeID), text=veri.ProjeAdi)
            projeSecici.options.append(temp_secenek)

        degistirButonu = ft.ElevatedButton(text="Bunun yerine çalışan ID'si girerek ekleyin...", bgcolor="blue",
                                           color="white", on_click=lambda e: atama_ekleyici_id(e))

        eklemeButonu = ft.ElevatedButton(text="Ekle", bgcolor="green", color="white",
                                         on_click=lambda e, kontrol=True: atama_ekleyici_handler(e, kontrol))
        iptalButonu = ft.ElevatedButton(text="İptal", bgcolor="red", color="white",
                                        on_click=lambda e, kontrol=False: atama_ekleyici_handler(e, kontrol))

        anaColumn = ft.Column(controls=[
            uyarıMetni,
            degistirButonu,
            calisanSecici,
            projeSecici,
            eklemeButonu,
            iptalButonu
        ])

        ana_container = ft.Container(content=anaColumn, visible=False)
        ana_container.visible = True
        page.add(ana_container)

    def atama_silici(e: None, id):
        cursor.execute("DELETE FROM GorevAtamalari WHERE AtamaID = ?", (id,))
        conn.commit()
        atama_yap()

    def atama_yap(e=None):
        page.clean()
        cursor.execute("SELECT * FROM GorevAtamalari")
        atama_tablo = cursor.fetchall()

        cursor.execute("SELECT * FROM Calisanlar")
        calisan_tablo = cursor.fetchall()

        cursor.execute("SELECT * FROM Projeler")
        proje_tablo = cursor.fetchall()

        ekle_butonu = ft.ElevatedButton(text="Görev Ataması Ekle", bgcolor="green", color="white",
                                        on_click=lambda e: atama_ekleyici(e))

        üst_row = ft.Row(controls=(
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Atama ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Çalışan Adı"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Çalışan ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje Adı"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
            ft.Container(content=ft.Text(value="Proje ID"), width=100),
            ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
        ))

        ust_container = ft.Container(content=üst_row, border=ft.border.all(width=3, color=ft.Colors.BLUE))

        page.add(ana_ekran_butonu, ekle_butonu, ust_container)

        for veri in atama_tablo:
            id = veri[0]
            calisanID = veri[1]
            projeID = veri[2]

            cursor.execute("SELECT * FROM Calisanlar WHERE CalisanID=?", (calisanID,))
            calisan = cursor.fetchone()
            cursor.execute("SELECT * FROM Projeler WHERE ProjeID=?", (projeID,))
            proje = cursor.fetchone()

            atama_sil = ft.ElevatedButton(text="Atamayı Kaldır", bgcolor="red", color="white",
                                          on_click=lambda e, gonder=id: atama_silici(e, gonder))

            temp_row = ft.Row(controls=(
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=id), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=calisan.Ad), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=calisan.CalisanID), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=proje.ProjeAdi), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                ft.Container(content=ft.Text(value=proje.ProjeID), width=100),
                ft.Container(width=1, height=30, border=ft.border.all(width=1, color="grey")),
                atama_sil

            ))

            temp_container = ft.Container(content=temp_row, border=ft.border.all(width=2, color="grey"), height=50)

            page.add(temp_container)

    anaEkranYap()

ft.app(target=main)