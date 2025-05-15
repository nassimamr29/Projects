<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Récupérer le rôle depuis la session
    $role = isset($_SESSION['role']) ? $_SESSION['role'] : null;

    if (!$role) {
        header("Location: connexion.html"); // Rediriger si le rôle n'est pas défini
        exit;
    }

    // Récupération des données du formulaire de connexion
    $email = htmlspecialchars($_POST['email']);
    $password = $_POST['password'];

    // Charger les utilisateurs depuis le fichier users.json
    $jsonFile = '../assets/data/users.json';
    $jsonData = file_get_contents($jsonFile);
    $users = $jsonData ? json_decode($jsonData, true) : [];

    // Vérification des identifiants et du rôle
    $userFound = false;
    foreach ($users as $user) {
        if ($user['email'] === $email && password_verify($password, $user['password'])) {
            // Vérification du rôle
            if ($user['role'] === $role) {
                // On enregistre l'utilisateur dans la session
                $_SESSION['user'] = $user; // On stocke toutes les infos de l'utilisateur
                $_SESSION['role'] = $user['role']; // Rôle de l'utilisateur
                
                // Redirection vers la page appropriée en fonction du rôle
                if ($role === 'Candidat') {
                    header("Location: ../pages/candidat.html");
                } elseif ($role === 'Professeur') {
                    header("Location: ../pages/professeur.html");
                }
                exit;
            }
        }
    }

    // Si aucun utilisateur n'est trouvé ou le rôle est incorrect
    echo "Identifiants incorrects ou rôle non valide.";
}
?>
