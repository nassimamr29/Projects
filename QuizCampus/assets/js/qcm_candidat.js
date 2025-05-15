// Récupérer l'index du QCM depuis l'URL
const params = new URLSearchParams(window.location.search);
const index = params.get("index");

// Charger le fichier JSON contenant tous les QCM
fetch("../../assets/data/qcm.json")
  .then((res) => res.json())
  .then((data) => {
    const qcm = data[index];
    if (!qcm) return; 

    // Afficher le titre et la description du QCM
    document.getElementById("qcm-titre").textContent = qcm.titre;
    document.getElementById("qcm-description").textContent = qcm.description;

    const form = document.getElementById("qcm-form");

    // Générer les questions et réponses dynamiquement
    qcm.questions.forEach((q, i) => {
      const div = document.createElement("div");
      div.className = "question";
      const title = document.createElement("h4");
      title.textContent = `${i + 1}. ${q.question}`;
      div.appendChild(title);

      q.reponses.forEach((rep, j) => {
        const label = document.createElement("label");
        label.style.display = "block";
        const input = document.createElement("input");
        input.type = "radio";
        input.name = `q${i}`;
        input.value = rep;

        label.appendChild(input);
        label.append(` ${rep}`);
        div.appendChild(label);
      });

      form.appendChild(div);
    });

    // Gestion de la soumission du QCM
    document.getElementById("submit-qcm").addEventListener("click", () => {
      let score = 0;

      // Calcul du score
      qcm.questions.forEach((q, i) => {
        const selected = document.querySelector(`input[name="q${i}"]:checked`);
        if (selected && q.bonnes.includes(selected.value)) {
          score++;
        }
      });

      const note = `${score} / ${qcm.questions.length}`;
      document.getElementById("resultat").innerHTML = `<h3>Votre score : ${note}</h3>`;

      // Envoyer le score au serveur via un script PHP
      fetch("../../php/save_score.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          qcmTitre: qcm.titre,
          score: note,
          email: "amrouche.nassim@icloud.com"
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log("Score sauvegardé !");
          } else {
            console.error("Erreur lors de la sauvegarde du score");
          }
        })
        .catch(error => {
          console.error("Erreur réseau : ", error);
        });
    });
  });
