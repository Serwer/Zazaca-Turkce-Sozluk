# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import (QMainWindow,QApplication,QLineEdit,QPushButton,QLabel,QMenuBar,QMenu,QStatusBar,QAction,QMessageBox,QVBoxLayout,QWidget,QButtonGroup,QListWidget)
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon,QPixmap
import sys
import sqlite3

class Dimili(QMainWindow):

    def baslat(self, anaPencere):
        anaPencere.resize(600, 400)
        anaPencere.setWindowTitle("Dimili-Türkçe Sözlük")
        anaPencere.setFixedSize(600,400)

        icon =QIcon()
        icon.addPixmap(QPixmap("Dictionary.png"),QIcon.Normal,QIcon.Off)
        anaPencere.setWindowIcon(icon)
        zemin=QWidget(anaPencere)
        zemin.setGeometry(QRect(0,30,600,390))
        zemin.setStyleSheet("background-color:rgb(167, 196, 233);")
        self.araKutu = QLineEdit(anaPencere)
        self.araKutu.setGeometry(QRect(10, 50, 200, 20))

        self.araKutu.textChanged.connect(self.benzerKelimeler)


        self.kelimeGir = QLabel("Kelimeler:",anaPencere)
        self.kelimeGir.setGeometry(QRect(10, 110, 141, 21))

        self.kelimeGor = QLabel("Kelime Ara",anaPencere)
        self.kelimeGor.setGeometry(QRect(10, 30, 91, 16))

        self.DilGrup=QButtonGroup(anaPencere)
        self.Dil1 = QPushButton("Zazaca-Türkçe",anaPencere)
        self.Dil1.setGeometry(QRect(230, 50, 91, 23))
        self.Dil1.setCheckable(True)
        self.Dil1.setAutoExclusive(True)
        self.Dil1.setChecked(True)
        self.Dil1.setStyleSheet("background-color: rgb(102, 255, 0);")

        self.Dil2 = QPushButton("Türkçe-Zazaca",anaPencere)
        self.Dil2.setGeometry(QRect(330, 50, 91, 23))
        self.Dil2.setCheckable(True)
        self.Dil2.setAutoExclusive(True)
        self.Dil2.setStyleSheet("background-color: rgb(255, 94, 105);")

        self.DilGrup.addButton(self.Dil1,1)
        self.DilGrup.addButton(self.Dil2,2)
        self.DilGrup.buttonClicked[int].connect(self.dilSecme)
        self.kelimeListesi=QListWidget(anaPencere)
        self.kelimeListesi.setGeometry(QRect(10, 130, 191, 231))

        self.kelimeListesi.itemClicked.connect(self.kelimeAcikla)
        self.kelimeAnlam = QLabel("Kelimenin Anlamı:",anaPencere)
        self.kelimeAnlam.setGeometry(QRect(230, 110, 131, 21))

        self.cumleList1 = QListWidget(anaPencere)
        self.cumleList1.setGeometry(QRect(230, 130, 351, 51))

        self.ornekCumle1 = QLabel("Örnek Zazaca Cümle:",anaPencere)
        self.ornekCumle1.setGeometry(QRect(230, 200, 101, 21))

        self.cumleList2 = QListWidget(anaPencere)
        self.cumleList2.setGeometry(QRect(230, 220, 351, 51))

        self.ornekCumle2 = QLabel("Örnek Türkçe Cümle:",anaPencere)
        self.ornekCumle2.setGeometry(QRect(230, 290, 111, 16))

        self.cumleList3 = QListWidget(anaPencere)
        self.cumleList3.setGeometry(QRect(230, 310, 351, 51))




        self.anaMenu = QMenuBar(anaPencere)
        self.anaMenu.setGeometry(QRect(0, 0, 600, 21))

        self.menuDosya = QMenu("Dosya",self.anaMenu)

        self.menuDuzenle = QMenu("Düzenle",self.anaMenu)

        self.menuYardim = QMenu("Yardım",self.anaMenu)

        anaPencere.setMenuBar(self.anaMenu)

        self.durum = QStatusBar(zemin)
        anaPencere.setStatusBar(self.durum)
        self.durum.setStyleSheet("background-color:white")
        self.durum.showMessage("Hazır")

        self.cikis= QAction(QIcon("Exit.ico"),"&Çıkış",anaPencere)
        self.cikis.setShortcut("Ctrl+X")

        self.cikis.triggered.connect(anaPencere.close)

        self.actionHakkinda = QAction("Hakkında",anaPencere)
        self.actionHakkinda.triggered.connect(self.hakkinda)
        self.actionSecenekler = QAction("Seçenekler",anaPencere)

        self.menuDosya.addAction(self.cikis)
        self.menuDuzenle.addAction(self.actionSecenekler)
        self.menuYardim.addAction(self.actionHakkinda)
        self.anaMenu.addAction(self.menuDosya.menuAction())
        self.anaMenu.addAction(self.menuDuzenle.menuAction())
        self.anaMenu.addAction(self.menuYardim.menuAction())

    def kelimeAcikla(self):
        if self.DilGrup.checkedId()==1:
            self.cumleList1.clear()
            self.cumleList2.clear()
            self.cumleList3.clear()
            itemtext= [str(x.text()) for x in self.kelimeListesi.selectedItems()]
            for it in itemtext:
                itemtext=it
            self.im.execute("select Tur from DimTur where Zazaca=?",[itemtext])
            turliste=[tur[0] for tur in self.im.fetchall()]
            for tura in turliste:
                turliste=tura
            self.im.execute("select Turkce from DimTur where Zazaca=?",[itemtext])
            turkAnlam=[tur[0] for tur in self.im.fetchall()]
            for tr in turkAnlam:
                self.cumleList1.addItem(itemtext+"("+turliste+")"+" : "+tr)
            self.im.execute("select OrnekZazacaCumle from DimTur where Zazaca=?",[itemtext])
            ornekZaza=[zaza[0] for zaza in self.im.fetchall()]
            for za in ornekZaza:
                ornekZaza=za
            self.cumleList2.addItem(ornekZaza)
            self.im.execute("select OrnekTurkceCumle from DimTur where Zazaca=?",[itemtext])
            ornekTurk=[turk[0] for turk in self.im.fetchall()]
            for orn in ornekTurk:
                ornekTurk=orn
            self.cumleList3.addItem(ornekTurk)
        if self.DilGrup.checkedId()==2:
            self.cumleList1.clear()
            self.cumleList2.clear()
            self.cumleList3.clear()
            itemtext= [str(x.text()) for x in self.kelimeListesi.selectedItems()]
            for it in itemtext:
                itemtext=it
            self.im.execute("select Tur from DimTur where Turkce=?",[itemtext])
            turliste=[tur[0] for tur in self.im.fetchall()]
            for tura in turliste:
                turliste=tura
            self.im.execute("select Zazaca from DimTur where Turkce=?",[itemtext])
            zazaAnlam=[tur[0] for tur in self.im.fetchall()]
            for tr in zazaAnlam:
                self.cumleList1.addItem(itemtext+"("+turliste+")"+" : "+tr)
            self.im.execute("select OrnekZazacaCumle from DimTur where Turkce=?",[itemtext])
            ornekTurk=[turk[0] for turk in self.im.fetchall()]
            for orn in ornekTurk:
                ornekTurk=orn
            self.cumleList2.addItem(ornekTurk)
            self.im.execute("select OrnekTurkceCumle from DimTur where Turkce=?",[itemtext])
            ornekZaza=[zaza[0] for zaza in self.im.fetchall()]
            for za in ornekZaza:
                ornekZaza=za
            self.cumleList3.addItem(ornekZaza)




    def benzerKelimeler(self):
        if self.DilGrup.checkedId()==1:
            self.VT=sqlite3.connect("DimiliVT.sqlite")
            self.im=self.VT.cursor()
            self.kelimeListesi.clear()
            kelime=self.araKutu.text()
            if kelime=="" or kelime==None:
                self.kelimeListesi.clear()
            else:
                self.im.execute("select Zazaca from DimTur where Zazaca like ? order by Zazaca ",[kelime+'%'])
                zazaListe=[za[0] for za in self.im.fetchall()]
                for i in zazaListe:
                 self.kelimeListesi.addItem(i)

        if self.DilGrup.checkedId()==2:
            self.VT=sqlite3.connect("DimiliVT.sqlite")
            self.im=self.VT.cursor()
            kelime=self.araKutu.text()
            self.kelimeListesi.clear()
            if kelime=="" or kelime==None:
                self.kelimeListesi.clear()
            else:
                self.im.execute("select Turkce from DimTur where Turkce like ? ",[kelime+'%'])
                turkListe=[tu[0] for tu in self.im.fetchall()]
                for i in turkListe:
                  self.kelimeListesi.addItem(i)

    def dilSecme(self,ind):
        if ind==1:
            self.araKutu.setText("")
            self.kelimeListesi.clear()
            self.cumleList1.clear()
            self.cumleList2.clear()
            self.cumleList3.clear()
            self.Dil1.setStyleSheet("background:#66FF00")
            self.Dil2.setStyleSheet("background-color:#E41841")
        if ind==2:
            self.araKutu.setText("")
            self.kelimeListesi.clear()
            self.cumleList1.clear()
            self.cumleList2.clear()
            self.cumleList3.clear()
            self.Dil2.setStyleSheet("background:#66FF00")
            self.Dil1.setStyleSheet("background-color:#E41841")
    def hakkinda(self):
        QMessageBox.about(self, "Program Hakkında",
                "Bu program <b>bla bla</b> tarafından programlanmıştır. 2015")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    anaPencere=QMainWindow()
    uygulama = Dimili()
    uygulama.baslat(anaPencere)
    anaPencere.show()
    sys.exit(app.exec_())
