document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                await loginUser(email, password);
            } catch (error) {
                console.error('Login error:', error);
                alert('Login failed: Invalid email or password.');
                alert('Login failed. Please check your credentials and try again.');
            }
        });
    }

    document.getElementById('price-filter').addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const priceText = card.querySelector('p').textContent;
            const price = parseInt(priceText.replace('Price per night: $', ''), 10);

            if (selectedPrice === 'All' || price <= parseInt(selectedPrice, 10)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    populatePriceFilter(); // Charge les options du filtre
    checkAuthentication(); // Vérifie l'authentification de l'utilisateur
});

async function loginUser(email, password) {
    const response = await fetch('https://127.0.0.1:5000/api/v1/login', { // Remplacez par l'URL de votre API
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`; // Stocke le token JWT dans un cookie
        window.location.href = 'index.html'; // Redirige vers la page principale
    } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token); // Fetch places if the user is authenticated
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places); // Affichez les lieux récupérés
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Effacez le contenu actuel

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function populatePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    const options = [10, 50, 100, 'All'];

    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        priceFilter.appendChild(opt);
    });
}