import sys
import psycopg2
from PyQt5.QtWidgets import QFrame, QHeaderView,QTableWidgetItem, QTableWidget, QCompleter, QGridLayout, QApplication, QWidget, QLineEdit, QSizePolicy, QSpacerItem, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400,400)
        font = QFont("Arial", 12, QFont.Bold)
        self.setStyleSheet("""
            QLabel { color: #333; }
            QLineEdit { padding: 8px; border: 1px solid #333; border-radius: 5px; }
            QPushButton { background-color: #008CBA; color: white; padding: 8px; border-radius: 5px; }
            QPushButton:hover { background-color: #007BB5; }
        """)
        recherche_layout = QGridLayout()
        #barre de recherche
        self.recherche_label = QLineEdit()
        self.recherche_label.setPlaceholderText("entrez votre recherche ...")
        self.recherche_label.setFont(font)
        #bouton de recherche par SHOW 
        recherche_bouton = QPushButton("GOOO !!",font = font)
        recherche_bouton.setIcon(QIcon("icons/search.png"))
        recherche_bouton.clicked.connect(self.search)
        #layout de la barre de recherche
        recherche_layout.addWidget(self.recherche_label,0,0)
        recherche_layout.addWidget(recherche_bouton,0,1)
        #categories
        self.categories_box = QComboBox()
        self.categories_box.setEditable(True)
        self.categories_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.categories_box.setInsertPolicy(QComboBox.NoInsert)
        self.categories_box.addItems(['Categories'])
        self.categories_box.setFont(font)
        #bouton de recherche pour les categories
        self.cat_recherche_bouton = QPushButton("GOOO !!",font = font)
        self.cat_recherche_bouton.setIcon(QIcon("icons/search.png"))
        self.cat_recherche_bouton.clicked.connect(self.search)
        #filtrer par
        self.filtrer_par = QComboBox()
        self.filtrer_par.setEditable(False)
        self.filtrer_par.setFont(font)
        self.filtrer_par.addItems(['filtrer par','ordre alphabetique','les plus recents','les plus longs'])
        #ajouter un layout horizontale pour separer recherche par SHOW ou par CATEGORIES
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)  # Ligne horizontale
        horizontal_line.setFrameShadow(QFrame.Sunken)  # Style enfoncé 
        #bouton favoris
        favoris_bouton = QPushButton("Favoris",font = font)
        favoris_bouton.setIcon(QIcon("icons/star.png"))
        favoris_bouton.setStyleSheet("background-color : green; color : white; padding : 5px;")
        #bouton profile
        profile_bouton = QPushButton("Profile",font=font)
        profile_bouton.setIcon(QIcon("icons/utilisateur.png"))
        #table
        self.tableWidget = QTableWidget()
        #layout des categories/filtrer par/rechercher par categorie
        layout_categories = QHBoxLayout()
        layout_categories.addWidget(self.categories_box)
        layout_categories.addWidget(self.filtrer_par)
        layout_categories.addWidget(self.cat_recherche_bouton)
        #layout principale 
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Recherche par SHOW :",font = font))
        main_layout.addLayout(recherche_layout)
        main_layout.addWidget(horizontal_line)
        main_layout.addWidget(QLabel("Recherche par CATEGORIES:",font = font))
        main_layout.addLayout(layout_categories)
        main_layout.addWidget(self.tableWidget)
        main_layout.addStretch()
        main_layout.addWidget(favoris_bouton)
        main_layout.addWidget(profile_bouton)
        self.setLayout(main_layout) 
        self.DataBaseManager()   

    def DataBaseManager(self):
        #connexion a la base de données
        self.connection = psycopg2.connect(database="MegaFlix", user="nassim", host="127.0.0.1", password="nassim1234")
        self.cursor = self.connection.cursor()

        #requette pour completer categories :
        self.cursor.execute("""SELECT DISTINCT TRIM(UNNEST(string_to_array(genres, ','))) AS category FROM megaflix ORDER BY category""")
        self.connection.commit()
        rows = self.cursor.fetchall()
        for row in rows:
            self.categories_box.addItem(str(row[0]))

        #requette pour completer la barre de recherche :    
        rows = []
        self.cursor.execute("""SELECT DISTINCT title FROM megaflix""")
        self.connection.commit()
        rows = self.cursor.fetchall()
        titles = [row[0] for row in rows]
        completer = QCompleter(titles, self)
        completer.setCaseSensitivity(False)  # Insensible à la casse
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.recherche_label.setCompleter(completer)  

    def search(self):
        #pour traiater la recherche par cetegories :
        self.tableWidget.clearContents()
        _categories_search = str(self.categories_box.currentText())
        _filtre = str(self.filtrer_par.currentText())
        match _filtre :
            case 'ordre alphabetique' : _lefiltre = 'title'
            case 'les plus recents' : _lefiltre = 'release_year'
            case 'les plus longs' : _lefiltre = 'duration'
        rows = []
        if _categories_search == 'Categories' : 
            QMessageBox.warning(self,"Erreur", "Veuillez entrez une categorie valide !!!!")
        if _filtre == 'filtrer par':
            self.cursor.execute(""f"SELECT title FROM MegaFlix WHERE listed_in LIKE '%{_categories_search}%' LIMIT 20""")
        else:
            if _lefiltre == 'title':
                self.cursor.execute(""f"SELECT title FROM MegaFlix WHERE listed_in LIKE '%{_categories_search}%' ORDER BY {_lefiltre} ASC LIMIT 20""")
            elif _lefiltre == 'release_year' or _lefiltre == 'duration':
                self.cursor.execute(""f"SELECT title, {_lefiltre} FROM MegaFlix WHERE listed_in LIKE '%{_categories_search}%' ORDER BY {_lefiltre} DESC LIMIT 20""")            
        self.connection.commit()
        rows += self.cursor.fetchall()
        if len(rows) == 0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return
        
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[-1]))

        i = 0 
        for row in rows :
            j = 0 
            for col in row :
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < len(rows[-1]) :
            header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()        

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
     main()