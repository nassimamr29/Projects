document.getElementById("qcmForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const qcm = {
    titre: document.getElementById("titre").value,
    description: document.getElementById("description").value,
    questions: []
  };

  // Récupérer les questions
  for (let i = 1; i <= 5; i++) {
    const questionText = document.getElementById(`question-${i}-input`)?.value;
    const type = document.getElementById(`type-${i}`)?.value;
    const reponses = document.getElementById(`reponses-${i}`)?.value.split(",").map(rep => rep.trim()).filter(Boolean);
    const bonnes = document.getElementById(`bonnes-${i}`)?.value.split(",").map(rep => rep.trim()).filter(Boolean);

    if (questionText) {
      qcm.questions.push({
        question: questionText,
        type: type,
        reponses: reponses,
        bonnes: bonnes
      });
    }
  }

  if (!qcm.titre || !qcm.description || qcm.questions.length === 0) {
    alert("Merci de remplir tous les champs !");
    return;
  }

  // Envoi des données
  fetch("../../php/qcm.php", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(qcm)
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "QCM ajouté !");
      document.getElementById("qcmForm").reset();
    })
    .catch(err => {
      console.error("Erreur :", err);
      alert("Erreur lors de l'enregistrement du QCM.");
    });
});

document.getElementById("addQuestionBtn").addEventListener("click", function () {
  const questionCount = document.querySelectorAll(".question-group").length;
  
  if (questionCount >= 5) {
    alert("Vous ne pouvez pas ajouter plus de 5 questions.");
    return;
  }

  const questionGroup = document.createElement("div");
  questionGroup.classList.add("question-group");
  const questionIndex = questionCount + 1;

  questionGroup.id = `question-${questionIndex}`;
  questionGroup.innerHTML = `
    <label for="question-${questionIndex}-input">Question ${questionIndex}</label>
    <input type="text" id="question-${questionIndex}-input" required>

    <label for="type-${questionIndex}">Type</label>
    <select id="type-${questionIndex}" required>
      <option value="choix_multiple">Choix multiple</option>
      <option value="vrai_faux">Vrai / Faux</option>
      <option value="texte">Réponse texte</option>
    </select>

    <label for="reponses-${questionIndex}">Réponses possibles (séparées par des virgules)</label>
    <input type="text" id="reponses-${questionIndex}">

    <label for="bonnes-${questionIndex}">Bonnes réponses (séparées par des virgules)</label>
    <input type="text" id="bonnes-${questionIndex}">
  `;

  document.getElementById("questionsContainer").appendChild(questionGroup);
});
