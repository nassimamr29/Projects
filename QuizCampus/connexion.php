<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Récupérer le rôle depuis la session
    $role = isset($_SESSION['role']) ? $_SESSION['role'] : null;

    if (!$role) {
        header("Location: connexion.html"); // Rediriger si le rôle n'est pas défini
        exit;
    }

    $email = htmlspecialchars($_POST['email']);
    $password = $_POST['password'];

    // Charger les utilisateurs depuis users.json
    $jsonFile = 'users.json';
    $jsonData = file_get_contents($jsonFile);
    $users = $jsonData ? json_decode($jsonData, true) : [];

    foreach ($users as $user) {
        if ($user['email'] === $email && password_verify($password, $user['password'])) {
            if ($user['role'] === $role) {
                $_SESSION['email'] = $email;
                header("Location: " . strtolower($role) . ".html"); // Redirige vers candidat.html ou professeur.html
                exit;
            }
        }
    }

    echo "Identifiants incorrects ou rôle non valide.";
}
?>
