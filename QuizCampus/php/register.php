<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Récupérer les données depuis le formulaire
    $data = [
        'civilite' => htmlspecialchars($_POST['civilite']),
        'role' => htmlspecialchars($_POST['role']),
        'nom' => htmlspecialchars($_POST['nom']),
        'prenom' => htmlspecialchars($_POST['prenom']),
        'naissance' => $_POST['naissance'],
        'email' => htmlspecialchars($_POST['email']),
        'password' => password_hash($_POST['password'], PASSWORD_DEFAULT) // Hachage du mot de passe
    ];

    // Charger les données existantes dans users.json
    $jsonFile = '../assets/data/users.json';
    $jsonData = file_get_contents($jsonFile);
    $users = $jsonData ? json_decode($jsonData, true) : [];

    // Vérifier si l'e-mail existe déjà
    foreach ($users as $user) {
        if ($user['email'] === $data['email']) {
            die("Erreur : Cet e-mail est déjà enregistré !");
        }
    }

    // Ajouter le nouvel utilisateur
    $users[] = $data;

    // Enregistrer les données mises à jour dans le fichier JSON
    file_put_contents($jsonFile, json_encode($users, JSON_PRETTY_PRINT));
    header("Location: ../pages/connexion.html"); 
    exit();
}
?>
