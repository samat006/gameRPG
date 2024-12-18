document.getElementById('newGameForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const player1Name = document.getElementById('player1').value;
    const player2Name = document.getElementById('player2').value;
    window.location.href="http://127.0.0.1:5000/plat"

    // Appel à l'API pour créer une nouvelle partie
    fetch('/new-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player1_name: player1Name,
            player2_name: player2Name
        })
    })
    .then(response => response.json())

    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        

        // Afficher l'interface de jeu
        document.getElementById('gameSetup').style.display = 'none';
        document.getElementById('gameDisplay').style.display = 'block';
        
        // Mettre à jour les informations des joueurs
        updatePlayerInfo('player1Card', data.player1);
        updatePlayerInfo('player2Card', data.player2);
        
        // Ajouter le message au journal
        addToGameLog(data.message);
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Une erreur est survenue');
    });
});

function updatePlayerInfo(cardId, playerData) {
    const card = document.getElementById(cardId);
    card.querySelector('.player-name').textContent = playerData.name;
    card.querySelector('.player-life').textContent = playerData.life;
    card.querySelector('.player-position').textContent = playerData.position;
}

function addToGameLog(message) {
    const gameLog = document.getElementById('gameLog');
    const entry = document.createElement('p');
    entry.textContent = `${new Date().toLocaleTimeString()} - ${message}`;
    gameLog.appendChild(entry);
    gameLog.scrollTop = gameLog.scrollHeight;
}

function checkStatus() {
    const player1Name = document.querySelector('#player1Card .player-name').textContent;
    fetch(`/player-status/${player1Name}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addToGameLog(`Erreur: ${data.error}`);
                return;
            }
            addToGameLog(`Status mis à jour`);
        })
        .catch(error => {
            console.error('Erreur:', error);
            addToGameLog('Erreur lors de la vérification du status');
        });
}

function resetGame() {
    document.getElementById('gameSetup').style.display = 'block';
    document.getElementById('gameDisplay').style.display = 'none';
    document.getElementById('gameLog').innerHTML = '';
    document.getElementById('newGameForm').reset();
}
