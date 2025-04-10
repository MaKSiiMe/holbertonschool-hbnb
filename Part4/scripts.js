document.addEventListener('DOMContentLoaded', () => {
    const places = [
        { name: 'Cozy Apartment', price: 120 },
        { name: 'Beach House', price: 200 },
        { name: 'Mountain Cabin', price: 150 }
    ];

    const placesList = document.getElementById('places-list');

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';

        card.innerHTML = `
            <h3 class="place-name">${place.name}</h3>
            <p class="place-price">$${place.price} per night</p>
            <button class="details-button">View Details</button>
        `;

        placesList.appendChild(card);
    });

    const isLoggedIn = false; // Changez cette valeur pour tester

    const reviewForm = document.getElementById('review-form');
    const loginButton = document.getElementById('login-button');

    if (isLoggedIn) {
        reviewForm.style.display = 'block';
        loginButton.style.display = 'none';
    } else {
        reviewForm.style.display = 'none';
        loginButton.style.display = 'block';
    }

    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Empêche le comportement par défaut du formulaire

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                displayErrorMessage('Email and password are required.');
                return;
            }

            try {
                // Envoi de la requête POST à l'API de connexion
                const response = await fetch('https://your-api-url.com/api/v1/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stocker le token JWT dans un cookie
                    document.cookie = `token=${data.token}; path=/; secure`;

                    // Rediriger vers index.html
                    window.location.href = 'index.html';
                } else {
                    // Afficher un message d'erreur si la connexion échoue
                    displayErrorMessage('Invalid email or password. Please try again.');
                }
            } catch (error) {
                console.error('Error during login:', error);
                displayErrorMessage('An error occurred. Please try again later.');
            }
        });
    }

    // Fonction pour afficher un message d'erreur
    function displayErrorMessage(message) {
        const errorMessage = document.getElementById('error-message');
        if (!errorMessage) {
            const newErrorMessage = document.createElement('p');
            newErrorMessage.id = 'error-message';
            newErrorMessage.textContent = message;
            newErrorMessage.style.color = 'red';
            loginForm.appendChild(newErrorMessage);
        } else {
            errorMessage.textContent = message;
        }
    }
});