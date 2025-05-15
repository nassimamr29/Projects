<?php
session_start();

// Récupération des données envoyées
$data = json_decode(file_get_contents('php://input'), true);
if (!$data || !isset($data['qcmTitre']) || !isset($data['score'])) {
    http_response_code(400);
    echo json_encode(["error" => "Données invalides"]);
    exit;
}

$email = $_SESSION['email'];
$qcmTitre = htmlspecialchars($data['qcmTitre']);
$score = intval($data['score']);

// Sauvegarde JSON
$resultatsFile = __DIR__ . '../../assets/data/resultats.json';

$resultats[] = [
    'email' => "amrouche.nassim@icloud.com",// pas reussi a stocker l'adresse mail donc on utilise la notre (une adresse perso)
    'qcm' => $qcmTitre,
    'score' => $score,
    'date' => date('Y-m-d H:i:s')
];

// Enregistrement sécurisé des résultats
if (file_put_contents($resultatsFile, json_encode($resultats, JSON_PRETTY_PRINT)) === false) {
    echo json_encode(["error" => "Erreur lors de l'enregistrement du fichier"]);
    exit;
}

// Envoi du mail via script Python
$pythonScript = __DIR__ . '/mailer.py';
$email_safe = escapeshellarg($email);
$qcm_safe = escapeshellarg($qcmTitre);
$score_safe = escapeshellarg($score);
$output = shell_exec("python3 $pythonScript $email_safe $qcm_safe $score_safe 2>&1");

// Vérification de l'envoi du mail
$response = ["success" => true, "email_sent" => !str_contains($output, "Erreur")];
echo json_encode($response);
?>
