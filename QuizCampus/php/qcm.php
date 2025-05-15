<?php
// Définit le type de contenu de la réponse HTTP comme étant JSON
header("Content-Type: application/json");

// Définit le chemin du fichier JSON où les données des QCM sont stockées
$jsonFile = "../assets/data/qcm.json";

// Vérifie si le fichier JSON existe, sinon crée un fichier vide avec un tableau JSON vide
if (!file_exists($jsonFile)) {
    file_put_contents($jsonFile, json_encode([]));  // Crée un fichier vide contenant un tableau JSON vide
}

// Charge et décode le contenu du fichier JSON dans une variable PHP
$qcmData = json_decode(file_get_contents($jsonFile), true);

// Récupère la méthode HTTP utilisée pour la requête
$method = $_SERVER["REQUEST_METHOD"];

// Si la méthode est GET, on renvoie les données des QCM sous forme JSON
if ($method === "GET") {
    echo json_encode($qcmData, JSON_PRETTY_PRINT);  // Affiche les données des QCM avec une mise en forme lisible
    exit;  // On arrête l'exécution du script après l'envoi de la réponse
}

// Si la méthode est POST, on ajoute un nouveau QCM
if ($method === "POST") {
    // Récupère et décode les données envoyées en POST
    $input = json_decode(file_get_contents("php://input"), true);
    
    // Vérifie si toutes les informations nécessaires sont présentes (titre, description, questions)
    if (!isset($input["titre"]) || !isset($input["description"]) || !isset($input["questions"])) {
        echo json_encode(["error" => "Données incomplètes"]);  // Si des données sont manquantes, renvoie une erreur
        exit;  
    }

    // Ajoute le nouveau QCM aux données existantes
    $qcmData[] = $input;

    // Sauvegarde les données mises à jour dans le fichier JSON
    file_put_contents($jsonFile, json_encode($qcmData, JSON_PRETTY_PRINT));
    
    // Renvoie une confirmation du succès de l'ajout du QCM
    echo json_encode(["message" => "QCM ajouté avec succès"]);
    exit;  // Arrête le script après la réponse
}
?>
