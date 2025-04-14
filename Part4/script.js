document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        // Add an event listener to handle the login form submission.
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

    // Add an event listener to handle changes in the price filter dropdown.
    document.getElementById('price-filter').addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const priceText = card.querySelector('.place-price').textContent;
            const price = parseInt(priceText.replace('Price per night: $', ''), 10);

            if (selectedPrice === 'All' || price <= parseInt(selectedPrice, 10)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    populatePriceFilter();
    checkAuthentication();

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error('Place ID not found in URL');
        return;
    }

    const token = checkAuthentication();
    fetchPlaceDetails(token, placeId);

    const detailButtons = document.querySelectorAll('.details-button');

    // Add event listeners to handle clicks on the details buttons for each place.
    detailButtons.forEach(button => {
        button.addEventListener('click', () => {
            const placeId = '123';
            window.location.href = `place.html?place_id=${placeId}`;
        });
    });

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        // Add an event listener to handle the review form submission.
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            try {
                await submitReview(token, placeId, reviewText, rating);
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Failed to submit review. Please try again.');
            }
        });
    }
});

// This function handles the login process by sending user credentials to the server and storing the authentication token in a cookie.
async function loginUser(email, password) {
    const response = await fetch('https://127.0.0.1:5000/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
    }
}

// This function retrieves a specific cookie value by its name.
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// This function checks if the user is authenticated by verifying the presence of a token cookie.
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

// This function fetches a list of places from the server and displays them on the page.
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
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// This function fetches detailed information about a specific place and displays it on the page.
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// This function dynamically displays a list of places on the page.
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3 class="place-name">${place.name}</h3>
            <p class="place-price">Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

// This function dynamically displays detailed information about a specific place on the page.
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';

    const detailsHTML = `
        <h2>${place.title}</h2>
        <p class="place-info">Description: ${place.description}</p>
        <p class="place-info">Price: $${place.price} per night</p>
        <p class="place-info">Location: (${place.latitude}, ${place.longitude})</p>
        <h3>Amenities:</h3>
        <ul>
            ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
        </ul>
        <h3>Reviews:</h3>
        <div id="reviews">
            ${place.reviews.map(review => `
                <div class="review-card">
                    <p>User: ${review.user}</p>
                    <p>Rating: ${review.rating}/5</p>
                    <p>${review.text}</p>
                </div>
            `).join('')}
        </div>
    `;

    placeDetails.innerHTML = detailsHTML;
}

// This function populates the price filter dropdown with predefined options.
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

// This function extracts the place ID from the URL query parameters.
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

// This function submits a review for a specific place to the server.
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating, 10)
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
        } else {
            const errorData = await response.json();
            alert(`Failed to submit review: ${errorData.error || response.statusText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while submitting the review.');
    }
}