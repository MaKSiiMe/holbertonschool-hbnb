document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');

    // Fonction pour récupérer les lieux depuis l'API
    async function fetchPlaces() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/');
            if (!response.ok) {
                throw new Error('Failed to fetch places');
            }
            const places = await response.json();

            // Afficher les lieux dans le frontend
            places.forEach(place => {
                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <h3 class="place-name">${place.title}</h3>
                    <p class="place-price">$${place.price} per night</p>
                    <button class="details-button" data-id="${place.id}">View Details</button>
                `;
                placesList.appendChild(card);
            });
        } catch (error) {
            console.error('Error fetching places:', error);
        }
    }

    // Appeler la fonction pour récupérer les lieux
    fetchPlaces();

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
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stocker le token JWT dans un cookie
                    document.cookie = `token=${data.access_token}; path=/; secure`;

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

    async function submitReview(placeId, reviewText, rating) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    place_id: placeId,
                    text: reviewText,
                    rating: rating,
                }),
            });

            if (response.ok) {
                console.log('Review submitted successfully');
            } else {
                console.error('Failed to submit review');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
        }
    }
});