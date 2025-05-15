document.getElementById('loadQCMButton').addEventListener('click', loadQCMs);

function loadQCMs() {
    fetch('../../php/get_qcm.php')

        .then(response => response.json())
        .then(data => {
            const qcmList = document.getElementById('qcmList');
            qcmList.innerHTML = ''; // on vide le contenu

            data.forEach(qcm => {
                const qcmItem = document.createElement('div');
                qcmItem.classList.add('qcm-item');
                qcmItem.innerHTML = `
                    <h3>${qcm.titre}</h3>
                    <p><strong>Description:</strong> ${qcm.description}</p>
                    <ul>
                        ${qcm.questions.map(question => `
                            <li>
                                <strong>Question:</strong> ${question.question}<br>
                                <strong>Réponses possibles:</strong> ${question.reponses.join(', ')}
                            </li>
                        `).join('')}
                    </ul>
                `;
                qcmList.appendChild(qcmItem);
            });
        })
        .catch(error => console.error('Erreur lors du chargement des QCM:', error));
}
