<?php
session_start();

// Vérifier si l'utilisateur est connecté
if (!isset($_SESSION['user'])) {
    header("Location: connexion.html"); // Rediriger si non connecté
    exit();
}

// Récupérer les informations de l'utilisateur depuis la session
$user = $_SESSION['user']; // L'utilisateur est stocké dans $_SESSION['user']

// Initialiser les résultats
$resultats = [];
$email = $user['email']; // Récupérer l'email de l'utilisateur pour filtrer les résultats

if (file_exists('../assets/data/resultats.json')) {
    $json = file_get_contents('../assets/data/resultats.json');
    $tous = json_decode($json, true);
    foreach ($tous as $res) {
        if ($res['email'] === $email) {
            $resultats[] = $res;
        }
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mon Compte - QuizCampus</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <style>/* Style pour les infos du compte*/ 
    .compte-container {
      max-width: 800px;
      margin: 50px auto;
      padding: 30px;
      background: rgb(88, 156, 181);
      border-radius: 15px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    h2 {
      text-align: center;
      margin-bottom: 30px;
      color: #2a3b8f;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
p {
    color: rgb(62, 84, 245);
    font-size: 18px;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(62, 84, 245, 0.3);
    line-height: 1.6;
    transition: color 0.3s ease-in-out;
}

p:hover {
    color: rgb(42, 64, 225);
    text-shadow: 2px 2px 5px rgba(42, 64, 225, 0.5);
}
    th, td {
      padding: 12px 18px;
      border: 1px solid #ddd;
      text-align: center;
    }
    th {
      background-color: #a7bdf3;
      color: white;
    }
    tr:nth-child(even) {
      background-color: rgb(74, 174, 161);
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">🎓 QuizCampus</div>
    <nav>
  <a href="mon_compte.php">Mon Compte</a>
  <a href="deconnexion.php">Déconnexion</a>
  <a href="../pages/candidat.html">Mes tests</a>
</nav>

  </header>

  <div class="compte-container">
    <h2>Bienvenue, <?php echo htmlspecialchars($user['prenom'] . ' ' . $user['nom']); ?>!</h2>

    <!-- Affichage des informations utilisateur -->
    <p>Email : <?php echo htmlspecialchars($user['email']); ?></p>
    <p>Date de naissance : <?php echo htmlspecialchars($user['naissance']); ?></p>
    <p>Rôle : <?php echo htmlspecialchars($user['role']); ?></p>

    <!-- Affichage des résultats de QCM -->
    <?php if (empty($resultats)): ?>
    <p>Vous n'avez encore passé aucun QCM.</p>
<?php else: ?>
    <table>
        <thead>
            <tr>
                <th>QCM</th>
                <th>Score</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($resultats as $res): ?>
                <tr>
                    <td><?= htmlspecialchars($res['qcm']) ?></td>
                    <td><?= htmlspecialchars($res['score']) ?></td>
                    <td><?= htmlspecialchars($res['date']) ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php endif; ?>

  </div>

  <footer>
    <p>&copy; 2025 QuizCampus</p>
  </footer>
</body>
</html>
