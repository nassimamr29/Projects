<?php
$data = json_decode(file_get_contents('php://input'), true);

$index = intval($data['qcmIndex']);  // Convertit l'index en entier
$answers = $data['answers'];  // Récupère les réponses de l'utilisateur

// Charge le fichier JSON contenant tous les QCMs
$qcms = json_decode(file_get_contents('../assets/data/qcm.json'), true);

// Récupère le QCM spécifique en fonction de l'index
$qcm = $qcms[$index];

// Initialise le score de l'utilisateur
$score = 0;

// Calcule le nombre total de questions dans ce QCM
$total = count($qcm['questions']);

foreach ($qcm['questions'] as $i => $question) {
    // Récupère les réponses correctes pour cette question
    $correct = $question['bonnes'];
    
    $user = $answers["q{$i}"] ?? [];  // Si aucune réponse n'est donnée, un tableau vide est utilisé

    sort($correct);
    sort($user);

    if ($correct == $user) {
        $score++;  // Si elles sont identiques, augmente le score
    }
}

$percentage = round(($score / $total) * 100);

// Retourne le score sous forme JSON
echo json_encode(['score' => $percentage]);
?>
