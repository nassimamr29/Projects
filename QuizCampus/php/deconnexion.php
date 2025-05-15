<?php
// Démarre la session
session_start();

// Supprime toutes les variables de session
session_unset();

// Détruit la session
session_destroy();

// Redirige l'utilisateur vers la page d'accueil ou une autre page
header("Location: ../pages/index.html"); // Change l'URL si nécessaire
exit();
?>
