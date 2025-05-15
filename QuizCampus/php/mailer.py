import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Lire les données depuis le fichier JSON
try:
    with open("../assets/data/resultats.json", "r", encoding="utf-8") as f:
        resultats = json.load(f)
        if not resultats:
            print("Le fichier JSON est vide.")
            exit(1)
        resultat = resultats[0]
        to_email = resultat["email"]
        qcm = resultat["qcm"]
        score = resultat["score"]
except Exception as e:
    print("Erreur lors de la lecture du fichier JSON :", e)
    exit(1)

# Configuration SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
your_email = "nassim.amrouche03@gmail.com"
your_password = "osbzzprpixqlvbhy"  
alias_from = "QuizCampus <quizcampus@noreply.com>"

# Création du message
msg = MIMEMultipart()
msg["From"] = alias_from
msg["To"] = to_email
msg["Subject"] = f"Résultat de votre QCM : {qcm}"

body = f"""Bonjour,

Vous avez obtenu la note suivante au QCM « {qcm} » : {score}.

Merci de votre participation sur QuizCampus.

Cordialement,
L'équipe QuizCampus
"""
msg.attach(MIMEText(body, "plain"))

# Envoi
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(your_email, your_password)
    server.sendmail(your_email, to_email, msg.as_string())
    server.quit()
    print("Email envoyé avec succès à", to_email)
except Exception as e:
    print("Erreur lors de l'envoi de l'email :", e)
    exit(1)
