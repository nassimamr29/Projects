<?php
// Définit le chemin du fichier JSON contenant les QCM
$file = "../assets/data/qcm.json";

// Vérifie si le fichier existe. Si oui, il charge son contenu et le décode en un tableau PHP. 
// Sinon, il initialise une variable $qcms avec un tableau vide.
$qcms = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

// Définit l'en-tête de la réponse HTTP pour indiquer que la réponse sera au format JSON
header("Content-Type: application/json");

// Encode le tableau PHP $qcms en JSON et l'envoie comme réponse
echo json_encode($qcms);
?>
