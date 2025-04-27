import spacy
from difflib import SequenceMatcher

# Charger le modèle spaCy pour le français
nlp = spacy.load("fr_core_news_sm")

# Base de données FAQ (questions et réponses)
FAQ = {
    "bonjour": "Salut grand chef !",
    "salut": "Wesh !",
    "comment tu t'appelles": "Je suis un chatbot simple.",
    "comment ça va": "Je vais très bien ! Comment puis-je vous aider ?",
    "que peux-tu faire": "Je peux répondre à des questions simples pour l'instant.",
    "quelle heure est-il": "Je suis désolé, je ne peux pas encore donner l'heure.",
    "où suis-je": "Je ne peux pas déterminer votre position pour l'instant.",
    "quel est ton but": "Mon but est de répondre aux questions simples que l'on me pose.",
    "qui t'a créé": "J'ai été créé par un développeur pour vous aider.",
    "quel âge as-tu": "Je n'ai pas d'âge, je suis un programme !",
    "comment tu fonctionnes": "Je fonctionne en utilisant l'intelligence artificielle pour analyser et répondre.",
    "où habites-tu": "Je n'ai pas de maison, je suis un programme informatique.",
    "que puis-je te demander": "Vous pouvez me poser toutes sortes de questions, tant qu'elles sont simples.",
    "as-tu une personnalité": "Je suis un chatbot, donc ma personnalité est celle que vous me donnez à travers vos questions.",
    "qui est ton créateur": "Mon créateur est un développeur spécialisé en IA et chatbot.",
    "est-ce que tu peux m'aider": "Oui, je suis là pour ça ! Comment puis-je vous aider ?",
    "quel temps fait-il aujourd'hui": "Je suis désolé, je ne peux pas vérifier la météo.",
    "peux-tu m'aider à trouver des informations": "Je peux essayer ! Posez-moi une question et je ferai de mon mieux.",
    "as-tu des hobbies": "Non, je n'ai pas de hobbies, mais j'adore répondre aux questions !",
    "quelles langues parles-tu": "Je parle français et anglais pour le moment.",
    "peux-tu m'apprendre à coder": "Oui, je peux vous aider à apprendre à coder, si vous avez des questions !",
    "quel est ton film préféré": "Je n'ai pas de préférences, mais je peux vous recommander des films si vous voulez.",
    "quel est ton livre préféré": "Je n'ai pas de livres préférés, mais je peux vous conseiller des livres.",
    "qui a écrit Harry Potter": "Harry Potter a été écrit par J.K. Rowling.",
    "quel est ton plat préféré": "Je n'ai pas de préférences alimentaires, je suis un programme !",
    "que penses-tu de l'intelligence artificielle": "L'intelligence artificielle est fascinante et elle permet de résoudre de nombreux problèmes.",
    "peux-tu me donner des conseils sur le développement web": "Oui, je peux vous aider ! Posez-moi des questions spécifiques sur le développement web.",
    "qu'est-ce que le machine learning": "Le machine learning est une méthode où les ordinateurs apprennent à partir des données, sans être explicitement programmés.",
    "comment fonctionnent les réseaux neuronaux": "Les réseaux neuronaux sont des systèmes informatiques inspirés du cerveau humain, utilisés dans l'intelligence artificielle.",
    "qu'est-ce que le cloud computing": "Le cloud computing permet d'accéder à des ressources informatiques (serveurs, stockage, etc.) via internet.",
    "qu'est-ce qu'un chatbot": "Un chatbot est un programme conçu pour simuler une conversation avec des utilisateurs humains."
}

# Fonction pour calculer la similarité en cas de fautes de frappe
def calculate_similarity(input_text, stored_text):
    return SequenceMatcher(None, input_text, stored_text).ratio()

# Fonction pour trouver la question la plus similaire
def get_most_similar_question(user_input):
    user_doc = nlp(user_input.lower())
    max_similarity = 0
    best_match = None

    for question in FAQ.keys():
        question_doc = nlp(question)
        spaCy_similarity = user_doc.similarity(question_doc)
        text_similarity = calculate_similarity(user_input.lower(), question.lower())
        combined_similarity = (spaCy_similarity + text_similarity) / 2

        if combined_similarity > max_similarity:
            max_similarity = combined_similarity
            best_match = question

    # Réduction du seuil pour inclure les fautes de frappe ou formulations similaires
    if max_similarity > 0.45:
        return best_match
    else:
        return None

# Fonction principale pour obtenir une réponse
def get_response(user_input):
    best_question = get_most_similar_question(user_input)
    if best_question:
        return FAQ[best_question]
    else:
        return "Désolé, je ne comprends pas. Essayez de reformuler votre question ou vérifiez votre orthographe."

