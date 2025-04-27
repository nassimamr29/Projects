# app.py
from flask import Flask, render_template, request, jsonify
import psycopg2
from chatbot import get_response

app = Flask(__name__)

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="chatbot",
    user="nassim",
    password="nassim1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Créer la table si elle n'existe pas déjà
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT
)
""")
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_response = get_response(user_message)

    # Enregistrer dans la base
    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_response) VALUES (%s, %s)",
        (user_message, bot_response)
    )
    conn.commit()

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
