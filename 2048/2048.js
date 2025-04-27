let grille = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
];
let score = 0;
let nbVide = 16;
/* Ici pn va transforme le tableau JavaScript grille en
   un tableau HTML visuel donc ça va génèrer du code HTML
   qui est ensuite inséré */

function construitGrille() {
    let code_html = "<table>";
    let valeur;

    /* on doit parcourir chaque ligne de la grille
    en ajoutant une nouvelle ligne au tab*/

    for (let i = 0; i < 4; i++) {
        code_html = code_html + "<tr>";
        for (let j = 0; j < 4; j++) {

            // si la case est 0 on mets "vide" sinon la vraie valeur 
            if (grille[i][j] === 0) {
                valeur = "";
            } else {
                valeur = grille[i][j];
            }
            /*  cette partie du code elle repond à al QST 7 + fonction changeColor(value)
            on regarde le nombre dans la case puis grace a la fonction elle aura une couleur*/
            let bgColor = ChangeColor(grille[i][j]);
            /*on applique a la cellule du style avec bgColor qui appel la fonction*/
            code_html += `<td style="background-color: ${bgColor};">${valeur}</td>`;
                
        }
        code_html = code_html + "</tr>";
    }
    code_html = code_html + "</table>";
    /* one close le tableau ici avec </table>  et on l'insere */
    document.getElementById("grille").innerHTML = code_html;
}
document.addEventListener("DOMContentLoaded", () => {
    construitGrille();
});

function afficheScore() {
    document.getElementById("score").innerHTML = score;
}

function caseVide(i, x) {
    let compteur = 0;
    
    // on cherche dans la grille pour trouver les cases vides
    // si c'est le cas on incremente le compteur
    for (let l = 0; l < 4; l++) {
        for (let  k = 0; k < 4; k++) {
            if (grille[l][k] === 0) {
                if (compteur === i) {
                    grille[l][k] = x;
                    nbVide = nbVide-1; 
                    return;
                }
                compteur++;
            }
        }
    }
}

function nouvelle() {

    score = 0;
    afficheScore();

    
    grille = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ];


    nbVide = 16;

    // on place 2 deux entiers aléatoires de 2 dans deux cases vides
    for (let i = 0; i < 2; i++) {
        let caseIndex = Math.floor(Math.random() * nbVide); 
        caseVide(caseIndex, 2); 
        }

    // on reaffiche la grille 
    construitGrille();
}

document.addEventListener("DOMContentLoaded", () => {
    nouvelle(); 
    document.getElementById("nouvelle-partie-btn").addEventListener("click", nouvelle); // Associer au bouton pour démarrer une nouvelle partie
});

document.getElementById("nv-game").addEventListener("click", nouvelle);
document.addEventListener("DOMContentLoaded", nouvelle);


function glisse(direction) {
    if (direction === 'g') {
        for (let i = 0; i < 4; i++) {
            // on utiise un tab temporaire pour la ligne pour enlever les zéros de la ligne
            let ligne = grille[i].filter(val => val !== 0); 
            // on utlise aussi un taableau pour suivre les fusions
            let fusion = [false, false, false, false]; 

            // on deplace et on fusionne les cases de meme valeur
            for (let j = 0; j < ligne.length - 1; j++) {
                if (ligne[j] === ligne[j + 1] && !fusion[j] && !fusion[j + 1]) {
                    
                    ligne[j] = ligne[j] * 2; 
                    score += ligne[j]; // ici on ajoute au score
                    fusion[j] = true; // si la fusion est ok !!
                    ligne.splice(j + 1, 1); // enlever la deuxième case fusionnée
                }
            }

            while (ligne.length < 4) {
                ligne.push(0);
            }

            grille[i] = ligne;
        }
    }

    nbVide = grille.flat().filter(val => val === 0).length;

    // Affichage de la grille et le score
    construitGrille();
    afficheScore();
}

function gameOver() {
    // Afficher un message "Game Over" après le score
    let gameOverMessage = document.createElement('div');
    gameOverMessage.style.textAlign = 'center';
    gameOverMessage.textContent = `Game Over! Ton score est ${score}`;

    // Ajouter le message à la page html
    document.getElementById("grille").appendChild(gameOverMessage);

    }

document.addEventListener("keydown", function(event) {
    // tant que la partie est toujours en cours
    // et si aucune case est vide bah c'est fini et on retourne rien
    if (nbVide === 0) {
        gameOver(); 
        return; 
    }

    // un switch pour les touches  
    switch (event.keyCode) {
        case 37: //  gauche
            glisse('g');
            break;
        case 38: //  haut
            glisse('h');
            break;
        case 39: //  droite
            glisse('d');
            break;
        case 40: //  bas
            glisse('b');
            break;
    }

    // Après chaque mouvement, placer 2 dans une case vide aléatoire
    if (nbVide > 0) {
        let caseIndex = Math.floor(Math.random() * nbVide); // Choisir une case vide aléatoire
        caseVide(caseIndex, 2); // on place 2 dans cette case vide
    }

    // affichage du score et de la grille tjrs
    construitGrille();
    afficheScore();
});


// Fonction pour obtenir la couleur de fond en fonction de la valeur de la case
function ChangeColor(value) {
    let color;
    switch(value) {
        case 2: color = "#e0e0e0"; break;  
        case 4: color = "#d3d3d3"; break;  
        case 8: color = "#ffbb33"; break;  
        case 16: color = "#ff9933"; break;  
        case 32: color = "#ff6600"; break;  
        case 64: color = "#ff3300"; break;  
        case 128: color = "#cc0000"; break;  
        case 256: color = "#990000"; break;  
        case 512: color = "#660000"; break;  
        case 1024: color = "#ff0000"; break;  
        case 2048: color = "#cc0000"; break;  
        default: color = " #BBDDDD"; break; // Blanc si la case est vide ou une valeur plus haute
    }
    return color;
}


