<?php
session_start();
// Récupérer le rôle depuis les paramètres URL
$role = isset($_GET['role']) ? htmlspecialchars($_GET['role']) : null;

// Vérifier que le rôle est valide
if ($role !== 'Professeur' && $role !== 'Candidat') {
    header("Location: connexion.html"); // Rediriger vers la page principale si le rôle est invalide
    exit;
}

// Sauvegarder le rôle dans une session pour plus de sécurité
$_SESSION['role'] = $role;
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion - <?php echo $role; ?></title>
    <link rel="stylesheet" href="../assets/css/authentification.css">
</head>
<body>
    <header>
        <div class="logo">🎓 QuizCampus</div>
        <nav>
            <a href="../pages/index.html">Accueil</a>
        </nav>
    </header>

    <div class="container">
        <h1>Connexion <?php echo $role; ?> 🔐</h1>
        <form action="connexion.php" method="post">
            <div class="form-group">
                <label for="email">Adresse e-mail</label>
                <input type="email" name="email" id="email" required>
            </div>
            <div class="form-group">
                <label for="password">Mot de passe</label>
                <input type="password" name="password" id="password" required>
            </div>
            <button type="submit" class="btn">Se connecter</button>
        </form>
    </div>

    <footer>
        <p>&copy; 2025 QuizCampus. Tous droits réservés.</p>
    </footer>
</body>
</html>
