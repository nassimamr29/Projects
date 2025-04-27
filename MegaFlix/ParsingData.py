import csv

# Ouvrir les fichiers
with open("dataMegaFlix.csv", 'r', encoding='utf-8') as f, open("MegaFlix-data.sql", "a", encoding='utf-8') as fichier:
    
    # Créer un lecteur CSV pour gérer les guillemets doubles et les virgules dans les champs
    reader = csv.reader(f, delimiter=',', quotechar='"')

    # URL de base pour les images
    base_url = "https://image.tmdb.org/t/p/w300"

    # Sauter la première ligne (noms des attributs)
    next(reader)
    
    # Parcourir chaque ligne du fichier CSV
    for items in reader:
        num_attributes = len(items)
        
        # Concaténer le chemin complet pour 'backdrop_path'
        if items[9]:  # Vérifier si 'backdrop_path' n'est pas vide (index 9 correspond à 'backdrop_path')
            items[9] = base_url + items[9]

        # Créer la commande SQL d'insertion
        fichier.write("INSERT INTO MegaFlix VALUES(")

        for i in range(num_attributes):
            item = items[i].replace("'", "''")  # Échapper les guillemets simples pour PostgreSQL
            
            # Si l'élément est vide, on le remplace par NULL
            if item == "":
                item = "NULL"
            # Si l'élément est une date et vide, on le remplace aussi par NULL sans guillemets
            elif i == 6:  # "date_added" est à la position 6 dans les CSV
                if item == "":
                    item = "NULL"
            # Si l'élément contient des guillemets doubles, il faut les doubler pour PostgreSQL
            elif '"' in item:
                item = item.replace('"', '""')

            # Si la colonne est une valeur vide mais que c'est une date, il faut le marquer comme NULL sans guillemets
            if item == "NULL":
                fichier.write("NULL")
            else:
                # Ajouter l'élément entre guillemets simples
                fichier.write(f"'{item}'")
            
            # Ajouter une virgule sauf pour le dernier élément
            if i < num_attributes - 1:
                fichier.write(", ")

        # Fermer la commande SQL
        fichier.write(");\n")

print("Les données ont été insérées avec succès.")
