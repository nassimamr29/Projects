import sys
import os
import re
import psycopg2
from psycopg2 import sql
from PyQt5.QtWidgets import (
    QApplication, QWidget, QComboBox,QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QLineEdit, QPushButton, QCheckBox ,QMessageBox,QListWidgetItem , QListWidget , QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont ,QPainter, QImage ,QFont, QDesktopServices ,QIcon
from PyQt5.QtCore import Qt, QTimer ,QRectF,QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QDialog ,QListWidget, QListWidgetItem, QMessageBox, QSpacerItem, QSizePolicy, QCompleter , QScrollArea 
from PyQt5.QtCore import Qt, QStringListModel ,QUrl
import requests



class HomePage(QWidget):
    def __init__(self, username, mail, password):
        super().__init__()
        self.username = username
        self.mail = mail
        self.password = password
        self.setWindowTitle("MegaFlix - Accueil")
        self.resize(900, 600)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Ajouter une icône globale en haut de la fenêtre
        app_icon = QLabel()
        app_icon.setPixmap(QPixmap("icons/app_icon.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        app_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_icon)

        profile_layout = QHBoxLayout()

        self.categories_box = QComboBox()
        self.categories_box.addItem("Categories")
        self.categories_box.currentIndexChanged.connect(self.filter_by_category)
        self.categories_box.setStyleSheet("""
QComboBox {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );
    color: white;  /* Texte blanc sur le fond rouge-jaune */
    font-size: 18px;
    font-weight: bold;
    padding: 10px 15px;
    border: 2px solid #E50914;  /* Bordure rouge vif */
    border-radius: 12px;  /* Bordures arrondies pour un look moderne */
    transition: background-color 0.3s ease, color 0.3s ease;  /* Transitions douces */
}

QComboBox:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair au survol */
        stop: 1 #E50914   /* Rouge clair au survol */
    );
    color: #D81F26;  /* Texte rouge foncé lorsqu'on survole */
    border: 2px solid #FFB400;  /* Bordure jaune lors du survol */
}

QComboBox::drop-down {
    border: none;
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #003366,  /* Bleu marine pour la flèche */
        stop: 1 #0A1D3D   /* Bleu très foncé */
    );
    border-radius: 8px;  /* Bordures arrondies pour la flèche */
    transition: background-color 0.3s ease;  /* Transition douce pour la flèche */
}

QComboBox::drop-down:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #0A1D3D,  /* Bleu foncé au survol */
        stop: 1 #003366   /* Bleu marine foncé */
    );
}

QComboBox:editable {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );
    color: white;  /* Texte blanc lors de l'édition */
}
""")
        self.setStyleSheet("""
                        QWidget {
                background: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2f339c,  /* Rouge Netflix */
                    stop: 1 #5436a8   /* Noir */
                );
                color: black; /* Couleur par défaut du texte */
            }
        """)





        self.load_categories()

        profile_button = QPushButton("Profil")
        profile_button.setIcon(QIcon("icons/utilisateur.png"))
        profile_button.setStyleSheet("""
QPushButton {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );
    color: white;  /* Texte en blanc pour bien contraster avec le fond */
    font-size: 18px;
    font-weight: bold;
    padding: 12px 20px;
    border: 2px solid #E50914;  /* Bordure rouge vif de Netflix */
    border-radius: 12px;  /* Bordures plus arrondies pour un look plus moderne */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* Transition fluide pour le fond et la transformation */
}

QPushButton:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair en début de survol */
        stop: 1 #E50914   /* Rouge clair en fin de survol */
    );
    color: #E50914;  /* Texte rouge vif lors du survol */
    transform: scale(1.05);  /* Légère animation d'agrandissement au survol */
}

QPushButton:pressed {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair en début du clic */
        stop: 1 #E50914   /* Rouge clair à la fin du clic */
    );
    color: #FFFFFF;  /* Texte en blanc lorsqu'on clique */
    transform: scale(0.98);  /* Légère réduction lors du clic pour un effet visuel */
}

QPushButton:focus {
    outline: none;  /* Enlever l'indicateur de focus par défaut */
}
    """)

        self.trier_par = QComboBox()
        self.trier_par.addItems([
                "Trier par",
                "Ordre alphabétique",
                "Les plus aimés",
                "Les plus récents",
                "Les plus longs",
                "Les plus vus"
            ])
        self.trier_par.currentIndexChanged.connect(self.filtrer_par_critere)
        self.trier_par.setStyleSheet("""
QComboBox {
    color: white;  /* Texte en blanc pour contraster avec le fond */
    font-size: 18px;  /* Taille de la police */
    font-weight: bold;  /* Texte en gras pour plus de visibilité */
    padding: 10px 15px;  /* Un peu d'espace autour du texte pour plus de confort */
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );  /* Dégradé du rouge au jaune */
    border-radius: 12px;  /* Bordures arrondies pour un effet moderne */
    border: 2px solid #E50914;  /* Bordure rouge vif pour délimiter l'élément */
    transition: background-color 0.3s ease, transform 0.2s ease, color 0.3s ease;  /* Transition fluide pour le fond, la couleur et la transformation */
}

QComboBox:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune vif en début de survol */
        stop: 1 #E50914   /* Rouge vif à la fin du survol */
    );  /* Inverser le dégradé sur hover */
    color: #E50914;  /* Texte rouge vif lors du survol */
    transform: scale(1.05);  /* Légère animation d'agrandissement au survol */
}

QComboBox:pressed {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair au début du clic */
        stop: 1 #E50914   /* Rouge vif à la fin du clic */
    );  /* Inverser le dégradé lors du clic */
    color: #FFFFFF;  /* Texte en blanc lorsqu'on clique */
    transform: scale(0.98);  /* Légère réduction pour un effet visuel lors du clic */
}

QComboBox::drop-down {
    border: none;  /* Enlever la bordure de la flèche */
    background: transparent;  /* Fond transparent pour la flèche */
}


        """)
        # Connecter le bouton à une méthode future pour afficher le menu profil
        profile_button.clicked.connect(self.show_profile_menu)

        self.categories_box.setFixedWidth(250)
        profile_button.setFixedWidth(250)
        self.trier_par.setFixedWidth(250)
        
        profile_layout.addWidget(self.categories_box)
        profile_layout.addStretch(1)
        profile_layout.addStretch(1)
        profile_layout.addWidget(profile_button)
        profile_layout.addStretch(1)
        profile_layout.addStretch(1)
        profile_layout.addWidget(self.trier_par) 

        # Ajouter le layout du profil à la mise en page principale (au-dessus des autres éléments)
        layout.addLayout(profile_layout)

        # Message de bienvenue
        welcome_label = QLabel(f"Bienvenue, {username} !")
        welcome_label.setFont(QFont("Arial", 22, QFont.Bold))
        welcome_label.setStyleSheet("""
QLabel {
    color: white;  /* Texte en blanc pour contraster avec le fond */
    font-size: 24px;  /* Taille de la police */
    font-weight: bold;  /* Texte en gras pour plus de visibilité */
    padding: 12px 25px;  /* Un peu d'espace autour du texte pour plus de confort */
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );  /* Dégradé du rouge au jaune */
    border-radius: 12px;  /* Bordures arrondies pour un effet moderne */
    transition: background-color 0.3s ease, transform 0.2s ease, color 0.3s ease;  /* Transition fluide pour le fond, transformation et couleur */
}
QLabel:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune vif en début de survol */
        stop: 1 #E50914   /* Rouge vif à la fin du survol */
    );  /* Inverser le dégradé sur hover */
    color: #E50914;  /* Texte rouge vif lors du survol */
    transform: scale(1.05);  /* Légère animation d'agrandissement pour un effet visuel */
}

QLabel:pressed {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair au début du clic */
        stop: 1 #E50914   /* Rouge vif à la fin du clic */
    );  /* Inverser le dégradé lors du clic */
    color: #FFFFFF;  /* Texte en blanc lorsqu'on clique */
    transform: scale(0.98);  /* Légère réduction pour un effet visuel lors du clic */
}
""")

        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Layout pour la barre de recherche et le bouton
        search_layout = QHBoxLayout()

        # Ajouter un spacer avant la barre de recherche pour l'espace à gauche
        search_layout.addItem(QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Donnez le titre du film ou un mot-clé")
        self.search_bar.setStyleSheet("""
QLineEdit {
    padding: 12px 15px;  /* Augmenter un peu les espacements pour un meilleur confort visuel */
    font-size: 16px;  /* Augmenter la taille de la police pour une meilleure lisibilité */
    font-weight: bold;  /* Texte en gras pour plus de visibilité */
    border-radius: 10px;  /* Bords arrondis pour un design moderne */
    background-color: #2C3E50;  /* Fond sombre avec une teinte bleue pour s'harmoniser avec l'interface */
    color: #ECF0F1;  /* Texte clair (blanc cassé) pour un bon contraste avec le fond */
    border: 2px solid #2980B9;  /* Bordure bleue pour s'harmoniser avec l'interface et attirer l'attention */
}

QLineEdit:focus {
    border: 2px solid #FFB400;  /* Bordure jaune doré pour indiquer l'état actif */
    background-color: #34495E;  /* Fond légèrement plus clair pour une interaction subtile */
    box-shadow: 0px 0px 15px rgba(255, 180, 0, 0.7);  /* Effet lumineux doré autour au focus */
}

QLineEdit::placeholder {
    color: #BDC3C7;  /* Texte placeholder gris clair pour plus de douceur */
}


""")
        
        # Création du QCompleter pour la liste déroulante
        self.completer = QCompleter(self)
        search_layout.addWidget(self.search_bar)

        # Bouton de recherche
        search_button = QPushButton("Rechercher", self)
        search_button.setIcon(QIcon("icons/search.png"))
        search_button.setStyleSheet("""
QPushButton {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #E50914,  /* Rouge vif de Netflix */
        stop: 1 #FFB400   /* Jaune vif de Netflix */
    );
    color: white;  /* Texte en blanc pour bien contraster avec le fond */
    font-size: 18px;
    font-weight: bold;
    padding: 12px 20px;
    border: 2px solid #E50914;  /* Bordure rouge vif de Netflix */
    border-radius: 12px;  /* Bordures plus arrondies pour un look plus moderne */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* Transition fluide pour le fond et la transformation */
}

QPushButton:hover {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair en début de survol */
        stop: 1 #E50914   /* Rouge clair en fin de survol */
    );
    color: #E50914;  /* Texte rouge vif lors du survol */
    transform: scale(1.05);  /* Légère animation d'agrandissement au survol */
}

QPushButton:pressed {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #FFB400,  /* Jaune clair en début du clic */
        stop: 1 #E50914   /* Rouge clair à la fin du clic */
    );
    color: #FFFFFF;  /* Texte en blanc lorsqu'on clique */
    transform: scale(0.98);  /* Légère réduction lors du clic pour un effet visuel */
}

QPushButton:focus {
    outline: none;  /* Enlever l'indicateur de focus par défaut */
}

""")
        search_button.clicked.connect(self.search_movies)  # Connexion à la méthode search_movies
        search_layout.addWidget(search_button)

        # Ajouter le layout avec la barre de recherche et le bouton à la mise en page principale
        layout.addLayout(search_layout)

        # Liste des résultats de recherche
        self.result_list = QListWidget(self)
        self.result_list.setStyleSheet("""
QListWidget {
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #1C205C,  /* Couleur sombre au début du dégradé */
        stop: 1 #4D2F9C   /* Couleur plus claire à la fin du dégradé */
    );
    color: white;  /* Texte en blanc pour un bon contraste */
    font-size: 14px;
    font-family: Arial, sans-serif;
    border-radius: 10px;  /* Coins arrondis pour un effet plus moderne */
    padding: 10px;
    border: 2px solid transparent;  /* Bordure invisible au départ */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);  /* Ombre pour un effet de profondeur */
}

QListWidget::item {
    padding: 10px;
    border-radius: 8px;  /* Coins arrondis pour chaque élément */
    margin-bottom: 10px;
    background-color: rgba(255, 255, 255, 0.1);  /* Fond semi-transparent */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* Transition fluide */
}

QListWidget::item:hover {
    background-color: rgba(255, 255, 255, 0.2);  /* Effet de survol plus lumineux */
    transform: scale(1.05);  /* Agrandissement léger lors du survol */
}

QListWidget::item:selected {
    background-color: #E50914;  /* Rouge vif de Netflix pour l'élément sélectionné */
    color: white;  /* Texte en blanc */
    border-radius: 8px;  /* Coins arrondis même pour l'élément sélectionné */
    box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);  /* Ombre rouge autour de l'élément sélectionné */
}

QListWidget::item:selected:hover {
    background-color: #FFB400;  /* Jaune vif lors du hover sur l'élément sélectionné */
    transform: scale(1.05);  /* Agrandissement sur le hover de l'élément sélectionné */
}

""")

        self.result_list.itemClicked.connect(self.show_movie_details)
        layout.addWidget(self.result_list)

        # Zone pour afficher les détails du film
        self.details_widget = QWidget(self)
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setAlignment(Qt.AlignTop)
        self.details_widget.setStyleSheet("""
    QWidget {
        background-color: #F8F8F8;  /* Fond clair, légèrement gris */
        padding: 20px;  /* Espacement intérieur */
        border-radius: 10px;  /* Coins arrondis pour une interface douce */
        border: 1px solid #E0E0E0;  /* Bordure subtile pour délimiter la zone */
    }
    QLabel {
        color: #FFFFFF;  /* Texte gris foncé pour une lecture facile */
        font-size: 16px;
        font-weight: bold;
    }
    QVBoxLayout {
        spacing: 15px;  /* Espacement entre les éléments */
    }
""")        
        layout.addWidget(self.details_widget)

        self.setStyleSheet("""
    QPushButton {
        background-color: #E50914;  /* Fond rouge initial */
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;  /* Transition fluide */
    }
    
    QPushButton:hover {
        background-color: #F1F1F1;  /* Fond clair au survol */
        color: #E50914;  /* Texte rouge lors du survol */
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Ombre subtile au survol */
    }
    
    QPushButton:focus {
        outline: none;  /* Enlever le contour bleu au focus */
    }

    QPushButton::icon {
        margin-right: 8px;  /* Espacement entre l'icône et le texte */
    }
""")
             # Ajout de la grille des films
        self.top_movies_widget = TopMoviesGrid()
        layout.addWidget(self.top_movies_widget)
        # Charger les suggestions de films
        self.load_suggestions()

    def filtrer_par_critere(self):
        """Filtrer les films selon le critère sélectionné."""
        critere = self.trier_par.currentText()

        # Requête SQL selon le critère sélectionné
        if critere == "Ordre alphabétique":
            query = "SELECT title FROM MegaFlix ORDER BY title ASC"
        elif critere == "Les plus aimés":
            query = "SELECT title FROM MegaFlix ORDER BY vote_average DESC"
        elif critere == "Les plus récents":
            query = "SELECT title FROM MegaFlix WHERE release_date IS NOT NULL ORDER BY release_date DESC"
        elif critere == "Les plus longs":
            query = "SELECT title FROM MegaFlix ORDER BY runtime DESC"
        elif critere == "Les plus vus":
            query = "SELECT title FROM MegaFlix ORDER BY vote_count DESC"
        else:
            # Si aucun critère valide n'est sélectionné
            self.result_list.clear()
            self.result_list.addItem("Veuillez sélectionner un critère valide.")
            return

        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Exécution de la requête
            cursor.execute(query)
            results = cursor.fetchall()

            # Affichage des résultats
            self.result_list.clear()
            if results:
                for row in results:
                    title = row[0]
                    self.result_list.addItem(QListWidgetItem(title))
            else:
                self.result_list.addItem("Aucun film trouvé pour ce critère.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def load_categories(self):
        """Charger les catégories distinctes de la base de données dans le QComboBox"""
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",       
                user="nassim",         
                password="nassim1234",   
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            query = """
                SELECT DISTINCT TRIM(genre) AS genre
                FROM (
                    SELECT unnest(string_to_array(genres, ',')) AS genre
                    FROM MegaFlix
                ) subquery
                ORDER BY genre;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Ajouter les résultats au QComboBox
            for row in results:
                self.categories_box.addItem(row[0])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les catégories : {e}")

    def filter_by_category(self):
        """Filtrer les films par catégorie sélectionnée."""
        selected_category = self.categories_box.currentText()

        # Ignorer si "Categories" est sélectionné
        if selected_category == "Categories":
            self.result_list.clear()
            self.result_list.addItem("Veuillez sélectionner une catégorie.")
            return

        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Requête pour récupérer les films dans la catégorie sélectionnée
            query = """
                SELECT title, backdrop_path, overview
                FROM MegaFlix
                WHERE genres ILIKE %s
                ORDER BY title
                LIMIT 20;
            """
            cursor.execute(query, (f'%{selected_category}%',))
            results = cursor.fetchall()

            # Afficher les résultats dans le QListWidget
            self.result_list.clear()
            if results:
                for title, backdrop_path, overview in results:
                    item = QListWidgetItem(title)
                    self.result_list.addItem(item)
            else:
                self.result_list.addItem("Aucun film trouvé dans cette catégorie.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()        

    def load_suggestions(self):
        """Charger les suggestions de films pour le QCompleter."""
        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Obtenir les titres des films
            cursor.execute("SELECT title FROM MegaFlix")
            titles = [row[0] for row in cursor.fetchall()]

            # Charger les titres dans le QCompleter
            model = QStringListModel(titles)
            self.completer.setModel(model)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.search_bar.setCompleter(self.completer)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def search_movies(self):
        """Recherche des films par titre ou mot-clé et ajoute à l'historique."""
        query = self.search_bar.text()
        if not query.strip():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un titre ou un mot-clé.")
            return

        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Ajouter la recherche dans la table historique
            user_id = self.get_user_id(conn)
            cursor.execute("""
                INSERT INTO historique (listed_in, id_user, type) 
                VALUES (%s, %s, %s)
            """, (query, user_id, "Recherche"))

            conn.commit()  # Sauvegarder les modifications

            # Exécution de la requête de recherche
            cursor.execute("""
                SELECT title, backdrop_path, overview FROM MegaFlix
                WHERE title ILIKE %s OR keywords ILIKE %s
                LIMIT 10;
            """, (f'%{query}%', f'%{query}%'))

            results = cursor.fetchall()
            self.result_list.clear()  # Vider la liste avant d'ajouter de nouveaux résultats

            if results:
                # Affichage des résultats dans le QListWidget avec image et titre
                for title, backdrop_path, overview in results:
                    item = QListWidgetItem(title)
                    self.result_list.addItem(item)
            else:
                self.result_list.addItem("Aucun film trouvé avec ce titre ou mot-clé.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()



       

    def show_movie_details(self, item):
        """Affiche les détails du film sélectionné dans une petite fenêtre."""
        title = item.text()
        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Recherche des détails du film dans la base de données
            cursor.execute("""
                SELECT title, backdrop_path, vote_average, release_date, revenue, runtime, tagline, genres,
                    production_companies, production_countries, homepage 
                FROM MegaFlix WHERE title = %s;
            """, (title,))
            movie = cursor.fetchone()

            if movie:
                # Afficher les informations dans une nouvelle fenêtre
                self.update_movie_details(movie)
            else:
                QMessageBox.warning(self, "Erreur", "Film non trouvé dans la base de données.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_movie_details(self, movie):
        """Affiche les détails d'un film dans une fenêtre."""
        (title, backdrop_path, vote_average, release_date, revenue, runtime, tagline,
        genres, production_companies, production_countries, homepage) = movie

        # Créer une fenêtre pour afficher les détails
        details_window = QDialog(self)
        details_window.setWindowTitle(title)
        details_window.setFixedSize(500, 700)
        details_layout = QVBoxLayout(details_window)

        # Charger l'image
        pixmap = QPixmap()
        try:
            response = requests.get(backdrop_path)
            pixmap.loadFromData(response.content)
        except Exception:
            pixmap = QPixmap("icons/default_movie.png")

        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(300, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        # Ajouter le titre
        self.title_label = QLabel(title)  # Utilisation de `self.title_label` pour la compatibilité avec `ajouter_aux_fav`
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Ajouter la note
        vote_label = QLabel(f"Note: {vote_average}/10")
        vote_label.setStyleSheet("color: #F39C12; font-size: 14px;")
        vote_label.setAlignment(Qt.AlignCenter)

        # Ajouter la date de sortie
        release_label = QLabel(f"Date de sortie: {release_date}")
        release_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter les revenus
        revenue_label = QLabel(f"Revenus: ${revenue:,}")
        revenue_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter la durée
        runtime_label = QLabel(f"Durée: {runtime} min")
        runtime_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter la tagline
        tagline_label = QLabel(f"Tagline: {tagline}")
        tagline_label.setStyleSheet("color: #FFFFFF; font-size: 14px; font-style: italic;")

        # Ajouter les genres
        genres_label = QLabel(f"Genres: {genres}")
        genres_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter les compagnies de production
        prod_companies_label = QLabel(f"Production: {production_companies}")
        prod_companies_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter les pays de production
        prod_countries_label = QLabel(f"Pays: {production_countries}")
        prod_countries_label.setStyleSheet("color: #e3dfda; font-size: 14px;")

        # Ajouter le bouton "Ajouter aux favoris" avec icône
        add_to_favorites_button = QPushButton("Ajouter aux favoris")
        add_to_favorites_button.setIcon(QIcon("icons/favoris.png"))
        add_to_favorites_button.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b40810;
            }
        """)
        add_to_favorites_button.clicked.connect(self.ajouter_aux_fav)

        # Ajouter les widgets à la fenêtre
        details_layout.addWidget(image_label)
        details_layout.addWidget(self.title_label)
        details_layout.addWidget(vote_label)
        details_layout.addWidget(release_label)
        details_layout.addWidget(revenue_label)
        details_layout.addWidget(runtime_label)
        details_layout.addWidget(tagline_label)
        details_layout.addWidget(genres_label)
        details_layout.addWidget(prod_companies_label)
        details_layout.addWidget(prod_countries_label)
        details_layout.addWidget(add_to_favorites_button)

        details_window.exec_()



        

         

    def ajouter_aux_fav(self):
        """Ajouter un film aux favoris"""
        movie_title = self.title_label.text() 
        user = self.username 

        try:
            # Connexion à la base de données
            conn = psycopg2.connect(
                dbname="MegaFlix", 
                user="nassim", 
                password="nassim1234", 
                host="localhost", 
                port="5432"
            )
            cursor = conn.cursor()

            # Rechercher l'utilisateur et le film dans les tables
            cursor.execute("""
                SELECT l.id AS user_id, m.id AS movie_id
                FROM login l
                INNER JOIN MegaFlix m ON m.title = %s
                WHERE l.username = %s
            """, (movie_title, user))

            result = cursor.fetchone()

            if result:
                user_id = result[0]
                movie_id = result[1]

                # Vérifier si le film est déjà dans les favoris
                cursor.execute("""
                    SELECT id_favoris
                    FROM favoris
                    WHERE id = %s AND id_user = %s
                """, (movie_id, user_id))

                if cursor.fetchone():  # Si une entrée existe
                    QMessageBox.warning(self, "Film déjà ajouté", "Ce film est déjà dans vos favoris!")
                else:
                    # Ajouter le film aux favoris
                    cursor.execute("""
                        INSERT INTO favoris (id, title, id_user)
                        VALUES (%s, %s, %s)
                    """, (movie_id, movie_title, user_id))

                    conn.commit()
                    QMessageBox.information(self, "Succès", "Le film a été ajouté aux favoris avec succès!")
            else:
                QMessageBox.warning(self, "Erreur", "Aucun utilisateur ou film trouvé.")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")



    def show_profile_menu(self):
        """Affiche un menu pour les options du profil."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Profil")
        dialog.setStyleSheet("background-color: #F1F1F1; padding: 20px;")
        dialog.setFixedSize(500, 500)

        layout = QVBoxLayout(dialog)

        # Ajouter une icône de profil
        self.profile_picture = QLabel()
        self.profile_picture.setPixmap(QPixmap("icons/utilisateur.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.profile_picture.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.profile_picture)

        # Ajouter les options du menu
        buttons = [
            ("Historique de recherche", lambda: self.show_history(dialog)),
            ("Paramètres", lambda: self.open_settings(dialog)),
            ("Favoris", lambda: self.open_favorites(dialog)),
            ("réinitialiser l'accueil", lambda: self.go_to_home(dialog)),
            ("Déconnexion", lambda: self.logout(dialog))
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            #print(text)
            button.setIcon(QIcon(f"icons/{text.lower().replace(' ', '_')}.png"))
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;  /* Fond blanc pour le bouton */
        color: black;  /* Texte en noir */
        font-size: 18px;  /* Taille de la police pour le texte */
        font-weight: bold;  /* Texte en gras */
        padding: 20px 30px;  /* Espacement autour du texte */
        border: 2px solid black;  /* Bordure noire pour le bouton */
        border-radius: 10px;  /* Coins arrondis */
        margin-bottom: 15px;  /* Marge en bas pour espacer des autres éléments */
    }
    
    QPushButton:hover {
        background-color: #F5F5F5;  /* Fond gris clair au survol */
    }
    
    QPushButton:focus {
        outline: none;  /* Enlever le contour bleu habituel lors du focus */
    }
""")

            button.clicked.connect(callback)
            layout.addWidget(button)

        dialog.exec_()

   

    def open_settings(self, dialog):
        QMessageBox.information(self, "Paramètres", "Ouverture des paramètres !")
        dialog.close()  # Ferme le dialogue
        self.close()    # Ferme la fenêtre principale
        self.settings_screen = Parametres(self.username, self.mail, self.password)  # Affiche l'écran de connexion
        self.settings_screen.show()

    def open_favorites(self, dialog):
        QMessageBox.information(self, "Favoris", "Ouverture des favoris !")
        dialog.close()  # Ferme le dialogue
        self.close()    # Ferme la fenêtre principale
        self.favoris_screen = Favoris(self.username, self.mail, self.password)  # Affiche l'écran de connexion
        self.favoris_screen.show()

    def go_to_home(self, dialog):
        """Retour à l'accueil."""
        QMessageBox.information(self, "Accueil", "Accueil reinitialisé avec succès !")
        dialog.close()  # Ferme le dialogue
        self.close()    # Ferme la fenêtre principale
        self.__init__(self.username, self.mail, self.password)  # Réinitialise la fenêtre principale
        self.show()

    def logout(self, dialog):
        """Déconnexion."""
        QMessageBox.information(self, "Déconnexion", "Vous êtes maintenant déconnecté !")
        dialog.close()  # Ferme le dialogue
        self.close()    # Ferme la fenêtre principale
        self.login_screen = LoginScreen()  # Affiche l'écran de connexion
        self.login_screen.show()

    def get_user_id(self, conn):
        """Récupérer l'ID de l'utilisateur connecté."""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM login WHERE username = %s", (self.username,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise Exception("Utilisateur introuvable dans la base de données.")
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'ID utilisateur : {e}")

    def show_history(self, dialog):
        """Affiche l'historique des recherches."""
        dialog.close()
        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT listed_in, date_heure 
                FROM historique 
                WHERE id_user = %s 
                ORDER BY date_heure DESC
            """, (self.get_user_id(conn),))

            historique = cursor.fetchall()

            if not historique:
                QMessageBox.information(self, "Historique", "Aucun historique trouvé.")
                return

            history_dialog = QDialog(self)
            history_dialog.setWindowTitle("Historique de recherche")
            history_dialog.setStyleSheet("background-color: #F1F1F1; padding: 20px;")
            history_dialog.setFixedSize(600, 400)

            history_layout = QVBoxLayout(history_dialog)

            # Liste des recherches
            self.history_list = QListWidget()
            for row in historique:
                item_text = f"{row[0]} (recherché le {row[1].strftime('%Y-%m-%d %H:%M:%S')})"
                self.history_list.addItem(item_text)
            history_layout.addWidget(self.history_list)

            # Bouton pour supprimer tout l'historique
            clear_all_button = QPushButton("Tout supprimer")
            clear_all_button.setIcon(QIcon("icons/trash.png"))  # Ajouter une icône
            clear_all_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: darkred;
                }
            """)
            clear_all_button.clicked.connect(lambda: self.clear_all_history(conn, history_dialog))
            history_layout.addWidget(clear_all_button)

            # Bouton pour supprimer les éléments sélectionnés
            clear_selected_button = QPushButton("Supprimer sélection")
            clear_selected_button.setIcon(QIcon("icons/trash.png"))  # Ajouter une icône
            clear_selected_button.setStyleSheet("""
                QPushButton {
                    background-color: orange;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: darkorange;
                }
            """)
            clear_selected_button.clicked.connect(lambda: self.clear_selected_history(conn))
            history_layout.addWidget(clear_selected_button)


            history_dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def clear_all_history(self, conn, history_dialog):
        """Supprimer tout l'historique."""
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historique WHERE id_user = %s", (self.get_user_id(conn),))
            conn.commit()
            QMessageBox.information(self, "Succès", "Tout l'historique a été supprimé.")
            history_dialog.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")

    def clear_selected_history(self, conn):
        """Supprimer les éléments sélectionnés dans l'historique."""
        try:
            cursor = conn.cursor()
            selected_items = self.history_list.selectedItems()
            for item in selected_items:
                movie_title = item.text().split(" (")[0]  # Extraire le titre
                cursor.execute("""
                    DELETE FROM historique 
                    WHERE listed_in = %s AND id_user = %s
                """, (movie_title, self.get_user_id(conn)))
            conn.commit()
            QMessageBox.information(self, "Succès", "Les éléments sélectionnés ont été supprimés.")
            for item in selected_items:
                self.history_list.takeItem(self.history_list.row(item))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")





    


       




class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MegaFlix - Chargement")
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Style et layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges
        layout.setSpacing(0)

        # Ajouter une image de fond couvrant toute la fenêtre
        self.background_label = QLabel(self)
        background_path = os.path.join(os.path.dirname(__file__), "image/megaflix_logo.png")  
        pixmap = QPixmap(background_path)
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        else:
            print(f"Erreur : le fichier {background_path} est introuvable.")
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, self.height() - 50, self.width() - 200, 20)
        self.progress_bar.setStyleSheet("""
          QProgressBar {
    border: 1px solid white;  /* Bordure blanche pour la barre */
    border-radius: 5px;  /* Coins arrondis pour la barre */
    background-color: black;  /* Fond noir pour la barre */
    text-align: center;  /* Centrer le texte à l'intérieur de la barre */
    color: white;  /* Couleur du texte en blanc */
    height: 25px;  /* Hauteur de la barre de progression */
}

QProgressBar::chunk {
    background-color: #E50914;  /* Couleur rouge typique de Netflix pour la barre de progression */
    border-radius: 5px;  /* Coins arrondis pour le morceau de la barre */
}""")
        self.progress_bar.setValue(0)

        self.setLayout(layout)

        # Animation circulaire
        self.angle = 0
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_spinner)
        self.timer.start(20)  # 50 FPS pour plus de fluidité

        self.setStyleSheet("background-color: black;")

    def animate_spinner(self):
        self.angle += 10
        if self.angle >= 360:
            self.angle = 0

        self.progress += 1
        if self.progress > 100:
            self.progress = 100

        self.progress_bar.setValue(self.progress)

        if self.progress == 100:
            self.timer.stop()
            self.open_login_screen()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner le cercle extérieur
        center_x = self.width() // 2
        center_y = self.height() // 2 + 100  # Position ajustée pour laisser de la place au cercle
        radius = 50  # Taille du cercle animé

        rect = QRectF(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

        # Segment animé
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.red)
        start_angle = self.angle * 16
        span_angle = 90 * 16  # Segment de 90°
        painter.drawPie(rect, start_angle, span_angle)

        # Terminer le dessin proprement
        painter.end()

    def open_login_screen(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()





class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MegaFlix - Connexion")
        self.resize(1000, 700)

        # Chemin vers l'image d'arrière-plan
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_image_path = os.path.join(script_dir, "image/login_background.jpg")

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges

        # Ajouter une image de fond avec QLabel
        self.background_label = QLabel(self)
        pixmap = QPixmap(background_image_path)
        if pixmap.isNull():
            print(f"Erreur : Impossible de charger l'image à {background_image_path}")
            self.background_label.setStyleSheet("background-color: black;")
        else:
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Layout pour les champs et boutons (Overlay)
        self.overlay_layout = QVBoxLayout()
        self.overlay_layout.setContentsMargins(40, 80, 40, 40)

        # Titre
        title_label = QLabel("S'identifier")
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)

        # Champ Identifiant
        self.identifier_field = QLineEdit()
        self.identifier_field.setPlaceholderText("Identifiant")
        self.identifier_field.setStyleSheet(self.get_input_style())

        # Champ Mot de passe
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Mot de passe")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet(self.get_input_style())

        # Bouton "S'identifier"
        login_button = QPushButton("S'identifier")
        login_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        login_button.clicked.connect(self.validate_login)

        # Texte "OU"
        or_label = QLabel("OU")
        or_label.setStyleSheet("color: white; font-size: 14px;")
        or_label.setAlignment(Qt.AlignCenter)

        # Bouton "Créer un compte"
        create_account_button = QPushButton("Créer un compte")
        create_account_button.setStyleSheet(self.get_button_style("rgba(255, 255, 255, 0.2)", "rgba(255, 255, 255, 0.4)", True))
        create_account_button.clicked.connect(self.open_create_account_screen)

       

        # Ajouter les widgets au layout d'overlay
        self.overlay_layout.addWidget(title_label)
        self.overlay_layout.addWidget(self.identifier_field)
        self.overlay_layout.addWidget(self.password_field)
        self.overlay_layout.addWidget(login_button)
        self.overlay_layout.addWidget(or_label)
        self.overlay_layout.addWidget(create_account_button)

        # Ligne horizontale pour checkbox
        horizontal_layout = QHBoxLayout()
      
        # Ajout du layout horizontal
        self.overlay_layout.addLayout(horizontal_layout)

        # Ajouter l'overlay au layout principal
        overlay_widget = QWidget(self)
        overlay_widget.setLayout(self.overlay_layout)
        overlay_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.main_layout.addWidget(overlay_widget)

    def validate_login(self):
        identifier = self.identifier_field.text()
        password = self.password_field.text()

        if not identifier or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs !")
            return

        try:
            # Connexion à la base de données PostgreSQL
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Vérification des informations d'identification
            cursor.execute("SELECT username, mail, password FROM login WHERE username = %s AND password = %s", (identifier, password))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, "Succès", "Connexion réussie !")
                self.open_home_page(result[0],result[1],result[2])  # Passer le nom d'utilisateur
            else:
                QMessageBox.critical(self, "Erreur", "Identifiant ou mot de passe incorrect !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def open_home_page(self, username, mail, password):
        """Ouvre la page d'accueil après une connexion réussie."""
        self.close()
        self.home_page = HomePage(username,mail,password)
        self.home_page.show()
    def open_create_account_screen(self):
        try:
            self.close()  # Fermer l'écran de connexion
            self.signup_screen = SignupWindow()  # Créer une nouvelle instance de SignupWindow
            self.signup_screen.show()  # Afficher la fenêtre d'inscription
        except Exception as e:
            print(f"Erreur lors de l'ouverture de l'écran d'inscription : {e}")
            QMessageBox.critical(self, "Erreur", "Impossible d'ouvrir la fenêtre 'Créer un compte'.")


    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """

    def get_button_style(self, color, hover_color, border=False):
        border_style = "border: 1px solid white;" if border else ""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                {border_style}
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def resizeEvent(self, event):
        """Met à jour la taille de l'image de fond si la fenêtre est redimensionnée."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_image_path = os.path.join(script_dir, "image/login_background.jpg")
        pixmap = QPixmap(background_image_path)
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        else:
            self.background_label.setStyleSheet("background-color: black;")
        self.background_label.setGeometry(0, 0, self.width(), self.height())

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer un compte")
        self.resize(900, 600)

        # Layout principal
        layout = QVBoxLayout(self)

        # Titre
        title_label = QLabel("Créer un compte")
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        # Champs de saisie
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nom d'utilisateur")
        self.name_field.setStyleSheet(self.get_input_style())

        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Adresse e-mail")
        self.email_field.setStyleSheet(self.get_input_style())

        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Mot de passe")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet(self.get_input_style()) 

        self.password_confirmation = QLineEdit()
        self.password_confirmation.setPlaceholderText("Confirmez le mot de passe")
        self.password_confirmation.setEchoMode(QLineEdit.Password)
        self.password_confirmation.setStyleSheet(self.get_input_style())

        # Label pour les messages d'erreur
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red; font-size: 14px;")

        # Bouton "S'inscrire"
        signup_button = QPushButton("S'inscrire")
        signup_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        signup_button.clicked.connect(self.validate_signup)

        #bouton Retour_a_la_page_de_connexion
        self.back_button = QPushButton("Aller à la page de connexion")
        self.back_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        self.back_button.clicked.connect(self.open_login_screen)

        # Ajouter les widgets au layout
        layout.addWidget(title_label)
        layout.addWidget(self.name_field)
        layout.addWidget(self.email_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.password_confirmation)
        layout.addWidget(self.error_label)
        layout.addWidget(signup_button)
        layout.addWidget(self.back_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: black;")

    def validate_signup(self):
        name = self.name_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        password_confirm = self.password_confirmation.text()

        # Réinitialiser le label d'erreur
        self.error_label.setText("")

        # Validation des champs vides
        if not name or not email or not password or not password_confirm:
            self.error_label.setText("Veuillez remplir tous les champs !")
            self.shake_widget(self.name_field if not name else self.email_field if not email else self.password_field if not password else self.password_confirmation)
            return

        # Validation de l'email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            self.error_label.setText("Adresse e-mail invalide !")
            self.shake_widget(self.email_field)
            return

        # Validation du mot de passe
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
            self.error_label.setText("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
            self.shake_widget(self.password_field)
            return

        #validation confirm_password
        if password != password_confirm:
            self.error_label.setText("les mots de passe ne correspendent pas !")
            self.shake_widget(self.password_confirmation)
            return


        # Connexion à la base PostgreSQL
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",  
                user="nassim",       
                password="nassim1234",  
                host="localhost",               
                port="5432"                    
            )
            cursor = conn.cursor()

            # Création de la table si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    mail TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

            # Vérification de l'existence du nom d'utilisateur
            cursor.execute("SELECT * FROM login WHERE username = %s", (name,))
            if cursor.fetchone():
                self.error_label.setText("Le nom d'utilisateur existe déjà !")
                self.shake_widget(self.name_field)
                conn.close()
                return

            # Insérer dans la base de données
            cursor.execute(
                "INSERT INTO login (username, mail, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
            success_box = QMessageBox(self)
            success_box.setWindowTitle("Succès")
            success_box.setText("Compte créé avec succès !")
            success_box.setIcon(QMessageBox.Information)
            success_box.setStyleSheet("""
                QMessageBox {
                    background-color: black;
    
                    font-size: 14px;
                }
                QLabel {
                    color: #2cff62;
                }
                QPushButton {
                    background-color: #008000;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color:  #00ff81 ;
                }
            """)
            success_box.exec_()
        except Exception as e:
            self.error_label.setText(f"Une erreur s'est produite : {e}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    def shake_widget(self, widget):
        """Ajoute une animation de secousse au widget donné."""
        animation = QPropertyAnimation(widget, b"geometry")
        original_geometry = widget.geometry()
        animation.setDuration(300)
        animation.setKeyValueAt(0, original_geometry)
        animation.setKeyValueAt(0.25, original_geometry.adjusted(-10, 0, -10, 0))
        animation.setKeyValueAt(0.5, original_geometry.adjusted(10, 0, 10, 0))
        animation.setKeyValueAt(0.75, original_geometry.adjusted(-10, 0, -10, 0))
        animation.setKeyValueAt(1, original_geometry)
        animation.start()

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """

    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """  

    def open_login_screen(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()

class Parametres(QWidget):
    def __init__(self, username, email, password):
        super().__init__()
        self.setWindowTitle("Paramètres")
        self.resize(900, 600)

        self.username = username
        self.email = email
        self.password = password
        self.password_visible = False  # État du mot de passe visible ou masqué

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)  
        password_layout = QHBoxLayout()  

        # Titre
        title_label = QLabel("Paramètres du compte")
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        #nom d'utilisateur
        self.username_label = QLabel("Nom d'utilisateur")
        self.username_label.setFont(QFont("Arial",12))
        self.username_label.setStyleSheet("color : white;")

        self.username_field = QLineEdit()
        self.username_field.setText(self.username)
        self.username_field.setReadOnly(True)
        self.username_field.setStyleSheet(self.get_input_style())

        #mail d'utilisateur
        self.email_label = QLabel("Adresse mail")
        self.email_label.setFont(QFont("Arial",12))
        self.email_label.setStyleSheet("color : white;")

        self.email_field = QLineEdit()
        self.email_field.setText(self.email)
        self.email_field.setReadOnly(True)
        self.email_field.setStyleSheet(self.get_input_style())

        #mot de passe
        self.password_label = QLabel("Mot de passe")
        self.password_label.setFont(QFont("Arial",12))
        self.password_label.setStyleSheet("color : white;")

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setText(self.password)
        self.password_field.setReadOnly(True)
        self.password_field.setStyleSheet(self.get_input_style())

        # Bouton pour afficher/masquer le mot de passe
        self.toggle_password_button = QPushButton("Afficher")
        self.toggle_password_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Bouton pour sauvegarder les modifications
        save_button = QPushButton("Change password")
        save_button.setStyleSheet(self.get_button_style("#008000", "#006600"))
        save_button.setIcon(QIcon("icons/stylo.png"))
        save_button.clicked.connect(self.open_page_modifier_mdp)

        # Bouton pour retourner
        back_button = QPushButton("Retour à l'accueil")
        back_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        back_button.setIcon(QIcon("icons/retour_à_l'accueil.png"))
        back_button.clicked.connect(self.open_page_acceuil)

        # Ajout des widgets au layout
        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.toggle_password_button)

        layout.addWidget(title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_field)
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        layout.addWidget(save_button)
        layout.addWidget(back_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: black;")

    def open_page_acceuil(self):
        self.close()
        self.login_screen = HomePage(self.username, self.email, self.password)
        self.login_screen.show()

    def open_page_modifier_mdp(self):
        self.change_pswd_window = ModifierMotDePasse(self.username)
        self.change_pswd_window.show()    

    def toggle_password_visibility(self):
        """Afficher ou masquer le mot de passe."""
        if self.password_visible:
            self.password_field.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("Afficher")
        else:
            self.password_field.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("Masquer")
        self.password_visible = not self.password_visible

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """

    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

class ModifierMotDePasse(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Modifier le mot de passe")
        self.resize(400, 300)

        # Layout principal
        layout = QVBoxLayout(self)

        # Titre
        title_label = QLabel("Modifier le mot de passe")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        # Champs de saisie
        self.new_password_field = QLineEdit()
        self.new_password_field.setPlaceholderText("Nouveau mot de passe")
        self.new_password_field.setEchoMode(QLineEdit.Password)
        self.new_password_field.setStyleSheet(self.get_input_style())

        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirmez le mot de passe")
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_field.setStyleSheet(self.get_input_style())

        # Label pour les messages d'erreur
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red; font-size: 14px;")

        # Bouton pour confirmer la modification
        confirm_button = QPushButton("Confirmer")
        confirm_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        confirm_button.setIcon(QIcon("icons/verifier.png"))
        confirm_button.clicked.connect(self.update_password)

        # Ajouter les widgets au layout
        layout.addWidget(title_label)
        layout.addWidget(self.new_password_field)
        layout.addWidget(self.confirm_password_field)
        layout.addWidget(self.error_label)
        layout.addWidget(confirm_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: black;")

    def update_password(self):
        new_password = self.new_password_field.text()
        confirm_password = self.confirm_password_field.text()

        # Réinitialiser le label d'erreur
        self.error_label.setText("")

        # Validation des champs
        if not new_password or not confirm_password:
            self.error_label.setText("Veuillez remplir tous les champs !")
            self.shake_widget(self.new_password_field if not new_password else self.confirm_password_field)
            return

        # Validation du mot de passe
        if len(new_password) < 8 or not re.search(r"[A-Z]", new_password) or not re.search(r"\d", new_password):
            self.error_label.setText("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
            self.shake_widget(self.new_password_field)
            return

        # Validation de confirmation du mot de passe
        if new_password != confirm_password:
            self.error_label.setText("Les mots de passe ne correspondent pas !")
            self.shake_widget(self.confirm_password_field)
            return

        # Mise à jour du mot de passe dans la base de données
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",  
                user="nassim",       
                password="nassim1234",  
                host="localhost",               
                port="5432"                    
            )
            cursor = conn.cursor()

            # Mise à jour du mot de passe
            cursor.execute(
                "UPDATE login SET password = %s WHERE username = %s",
                (new_password, self.username)
            )
            conn.commit()

            # Vérifier si la mise à jour a réussi
            if cursor.rowcount == 0:
                self.error_label.setText("Utilisateur introuvable !")
            else:
                success_box = QMessageBox(self)
                success_box.setWindowTitle("Succès")
                success_box.setText("Le mot de passe a été modifié avec succès !")
                success_box.setIcon(QMessageBox.Information)
                success_box.setStyleSheet("""
                    QMessageBox {
                        background-color: black;
                        font-size: 14px;
                    }
                    QLabel {
                        color: #2cff62;
                    }
                    QPushButton {
                        background-color: #008000;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color:  #00ff81 ;
                    }
                """)
                success_box.exec_()
                self.close()

        except Exception as e:
            self.error_label.setText(f"Une erreur s'est produite : {e}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    def shake_widget(self, widget):
        """Ajoute une animation de secousse au widget donné."""
        animation = QPropertyAnimation(widget, b"geometry")
        original_geometry = widget.geometry()
        animation.setDuration(300)
        animation.setKeyValueAt(0, original_geometry)
        animation.setKeyValueAt(0.25, original_geometry.adjusted(-10, 0, -10, 0))
        animation.setKeyValueAt(0.5, original_geometry.adjusted(10, 0, 10, 0))
        animation.setKeyValueAt(0.75, original_geometry.adjusted(-10, 0, -10, 0))
        animation.setKeyValueAt(1, original_geometry)
        animation.start()

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """

    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

class Favoris(QWidget):
    def __init__(self, username, mail, password):
        super().__init__()
        self.username = username
        self.mail = mail
        self.password = password
        self.setWindowTitle("Mes Favoris")
        self.resize(900, 600)

        layout = QVBoxLayout()
        title_label = QLabel("Vos Favoris :")
        title_label.setFont(QFont("Arial"))
        title_label.setStyleSheet("color: white; font-size: 30px; border-radius: 5px; padding: 10px; margin-top: 20px;font-weight: bold;")
        layout.addWidget(title_label)

        self.favoris_list = QListWidget()
        self.favoris_list.setSelectionMode(QListWidget.MultiSelection)  # Permettre la sélection multiple
        self.favoris_list.setStyleSheet("""
QListWidget {
    background: qlineargradient(                SELECT DISTINCT TRIM(genre) AS genre
                FROM (
                    SELECT unnest(string_to_array(genres, ',')) AS genre
                    FROM MegaFlix
                ) subquery
                ORDER BY genre;
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #1C205C,  /* Couleur sombre au début du dégradé */
        stop: 1 #4D2F9C   /* Couleur plus claire à la fin du dégradé */
    );
    color: white;  /* Texte en blanc pour un bon contraste */
    font-size: 14px;
    font-family: Arial, sans-serif;
    border-radius: 10px;  /* Coins arrondis pour un effet plus moderne */
    padding: 10px;
    border: 2px solid transparent;  /* Bordure invisible au départ */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);  /* Ombre pour un effet de profondeur */
}

QListWidget::item {
    padding: 10px;
    border-radius: 8px;  /* Coins arrondis pour chaque élément */
    margin-bottom: 10px;
    background-color: rgba(255, 255, 255, 0.1);  /* Fond semi-transparent */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* Transition fluide */
}

QListWidget::item:hover {
    background-color: rgba(255, 255, 255, 0.2);  /* Effet de survol plus lumineux */
    transform: scale(1.05);  /* Agrandissement léger lors du survol */
}

QListWidget::item:selected {
    background-color: #E50914;  /* Rouge vif de Netflix pour l'élément sélectionné */
    color: white;  /* Texte en blanc */
    border-radius: 8px;  /* Coins arrondis même pour l'élément sélectionné */
    box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);  /* Ombre rouge autour de l'élément sélectionné */
}

QListWidget::item:selected:hover {
    background-color: #FFB400;  /* Jaune vif lors du hover sur l'élément sélectionné */
    transform: scale(1.05);  /* Agrandissement sur le hover de l'élément sélectionné */
} """)

        layout.addWidget(self.favoris_list)

        refresh_button = QPushButton("Chargez les favoris")
        refresh_button.clicked.connect(self.load_favoris)
        refresh_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        refresh_button.setIcon(QIcon("icons/refresh.png"))
        layout.addStretch()
        layout.addWidget(refresh_button)

        delete_button = QPushButton("Supprimer les favoris sélectionnés")
        delete_button.setIcon(QIcon("icons/trash.png"))
        delete_button.clicked.connect(self.supprimer_favoris)
        delete_button.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        layout.addWidget(delete_button)

        retour_bouton = QPushButton("Retour à la page d'accueil")
        retour_bouton.setStyleSheet(self.get_button_style("#E50914", "#b40810"))
        retour_bouton.clicked.connect(self.retour_acceuil)
        retour_bouton.setIcon(QIcon("icons/retour_à_l'accueil.png"))
        layout.addWidget(retour_bouton)

        self.setLayout(layout)
        self.setStyleSheet("background-color: grey;")
        self.load_favoris()

    def get_input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """

    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def retour_acceuil(self):
        """Retour a l'accueil"""
        self.close()
        self.home_page = HomePage(self.username, self.mail, self.password)
        self.home_page.show()

    def load_favoris(self):
        """Charger et afficher les favoris de l'utilisateur"""
        self.favoris_list.clear()
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",       
                user="nassim",         
                password="nassim1234",   
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            query = """SELECT title FROM favoris, login WHERE login.username = %s AND login.id = favoris.id_user ORDER BY title ASC"""
            cursor.execute(query, (self.username,))
            results = cursor.fetchall()

            if results:
                for row in results:
                    self.favoris_list.addItem(row[0])
            else:
                self.favoris_list.addItem("Aucun favoris trouvé !")

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les favoris : {e}")

    def supprimer_favoris(self):
        """Supprimer les favoris sélectionnés de la base de données"""
        selected_items = self.favoris_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucun élément sélectionné", "Veuillez sélectionner au moins un favori à supprimer.")
            return

        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",       
                user="nassim",         
                password="nassim1234",   
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            for item in selected_items:
                title = item.text()
                query = """DELETE FROM favoris 
                           USING login 
                           WHERE favoris.id_user = login.id 
                           AND login.username = %s 
                           AND favoris.title = %s"""
                cursor.execute(query, (self.username, title))

            conn.commit()
            QMessageBox.information(self, "Succès", "Les favoris sélectionnés ont été supprimés.")
            self.load_favoris()  # Recharger la liste des favoris après suppression

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de supprimer les favoris : {e}")


class TopMoviesGrid(QWidget):
    def __init__(self):
        super().__init__()

        # Mise en page principale
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Titre pour la section
        title_label = QLabel("Films les mieux notés")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
    font-size: 20px; 
    font-weight: bold; 
    margin-bottom: 10px; 
    color: white;
    background: qlineargradient(
        spread: pad, x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #007BFF,  /* Dégradé du bleu vif */
        stop: 1 #FF69B4   /* Au rose intense */
    );
    padding: 15px; /* Espace intérieur pour mettre en valeur le texte */
    border: 2px solid transparent; /* Bordure initiale invisible */
    border-radius: 15px; /* Coins très arrondis pour un look fluide */
    background-clip: padding-box; /* Gérer l'arrière-plan dans la bordure */
    box-shadow: 0px 4px 15px rgba(0, 123, 255, 0.5), /* Ombre bleue lumineuse */
                0px 0px 10px rgba(255, 105, 180, 0.6); /* Ombre rose douce */
""")

        # Layout pour la grille
        self.movie_grid = QGridLayout()
        self.layout.addLayout(self.movie_grid)

        # Charger les films
        self.load_top_movies()

    def load_top_movies(self):
        """Charger et afficher les films les mieux notés."""
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Charger les films depuis la base de données
            cursor.execute("""
                SELECT title, backdrop_path, overview
                FROM MegaFlix
                WHERE backdrop_path IS NOT NULL
                ORDER BY vote_average DESC
                LIMIT 9;
            """)
            movies = cursor.fetchall()
            cursor.close()
            conn.close()

            # Afficher les films dans la grille
            self.display_movies(movies)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les films : {e}")

    def display_movies(self, movies):
        """Afficher les films dans la grille."""
        for index, (title, backdrop_path, overview) in enumerate(movies):
            row, col = divmod(index, 3)  # Calculer la position dans la grille

            # Création d'un conteneur pour chaque film
            container = QVBoxLayout()

            # Charger l'image
            pixmap = QPixmap()
            try:
                response = requests.get(backdrop_path)
                pixmap.loadFromData(response.content)
            except Exception:
                pixmap = QPixmap("icons/default_movie.png")

            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(150, 225, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)

            # Ajouter le titre
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF;")

            # Ajouter les widgets au conteneur
            container.addWidget(image_label)
            container.addWidget(title_label)

            # Ajouter un bouton cliquable
            container_widget = QWidget()
            container_widget.setLayout(container)
            container_widget.mousePressEvent = lambda event, movie=(title, backdrop_path, overview): self.show_movie_details(movie)
            self.movie_grid.addWidget(container_widget, row, col)


    def show_movie_details(self, movie):
        """Afficher les détails du film dans une nouvelle fenêtre."""
        title, backdrop_path, overview = movie

        # Afficher une nouvelle fenêtre avec les détails du film
        details_window = QDialog(self)
        details_window.setWindowTitle(title)
        details_window.setFixedSize(400, 600)
        details_layout = QVBoxLayout(details_window)

        # Charger l'image
        pixmap = QPixmap()
        try:
            response = requests.get(backdrop_path)
            pixmap.loadFromData(response.content)
        except Exception:
            pixmap = QPixmap("icons/default_movie.png")

        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(300, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        # Ajouter la description
        description_label = QLabel(overview)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignTop)
        description_label.setStyleSheet("font-size: 14px; color: #4C0000; padding: 10px;")

        # Ajouter un bouton pour ajouter aux favoris
        add_to_favorites_button = QPushButton("Ajouter aux favoris")
        add_to_favorites_button.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b40810;
            }
        """)
        add_to_favorites_button.clicked.connect(lambda: self.add_to_favorites(title, details_window))

        # Ajouter les widgets à la fenêtre
        details_layout.addWidget(image_label)
        details_layout.addWidget(description_label)
        details_layout.addWidget(add_to_favorites_button)

        details_window.exec_()
    
    
    def add_to_favorites(self, title, parent_window):
        """Ajouter un film aux favoris."""
        try:
            conn = psycopg2.connect(
                dbname="MegaFlix",
                user="nassim",
                password="nassim1234",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Récupérer l'ID de l'utilisateur (remplacez `user_id` par votre logique d'utilisateur)
            user_id = 1  # Remplacez par l'ID de l'utilisateur connecté

            # Récupérer l'ID du film
            cursor.execute("SELECT id FROM MegaFlix WHERE title = %s", (title,))
            movie_id = cursor.fetchone()
            if not movie_id:
                QMessageBox.warning(parent_window, "Erreur", "Film introuvable dans la base de données.")
                return
            movie_id = movie_id[0]

            # Vérifier si le film est déjà dans les favoris
            cursor.execute("""
                SELECT id_favoris FROM favoris WHERE id = %s AND id_user = %s
            """, (movie_id, user_id))
            if cursor.fetchone():
                QMessageBox.information(parent_window, "Favoris", "Ce film est déjà dans vos favoris.")
            else:
                # Ajouter le film aux favoris
                cursor.execute("""
                    INSERT INTO favoris (id, title, id_user)
                    VALUES (%s, %s, %s)
                """, (movie_id, title, user_id))
                conn.commit()
                QMessageBox.information(parent_window, "Favoris", "Film ajouté aux favoris avec succès !")

            cursor.close()
            conn.close()
        except psycopg2.IntegrityError as e:
            conn.rollback()
            QMessageBox.critical(parent_window, "Erreur", f"Erreur d'intégrité des données : {e}")
        except Exception as e:
            QMessageBox.critical(parent_window, "Erreur", f"Impossible d'ajouter aux favoris : {e}")
        finally:
            if conn:
                conn.close()





if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer une instance de l'écran de chargement
    loading_screen = LoadingScreen()

    # Une fois que le chargement est terminé, afficher la fenêtre d'inscription
    def show_signup_window():
        signup_window = SignupWindow()
        signup_window.show()
        loading_screen.close()

    # Connecter l'action après chargement
    loading_screen.timer.timeout.connect(lambda: show_signup_window() if loading_screen.progress == 100 else None)

    # Afficher l'écran de chargement
    loading_screen.show()

    # Lancer l'application
    sys.exit(app.exec_())