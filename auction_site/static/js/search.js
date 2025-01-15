const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const searchResults = document.querySelector('.search-results');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

// Function to clear and populate search results
const renderSearchResults = (data) => {
    // Clear existing results
    searchResults.innerHTML = '';

    if (data.length > 0) {
        data.forEach(result => {
            const itemHTML = `
                <div id="item" class="item">
                    <a class="title" href="${result.url}">${result.title}</a>
                    ${result.image ?
                `<p><img src="${result.image}" alt="${result.title}" style="max-width: 100%;"></p>` :
                `<p><img src="/static/images/default_image.jpg" alt="No image available" style="max-width: 100%;"></p>`
            }
                    <p class="description">${result.description}</p>
                    <div class="price-end-date">
                        <p id="price">Current Price: <span class="amount">&#8364; ${result.current_price}</span></p>
                        <p class="end_date">Ends: ${result.auction_end_date}</p>
                    </div>
                </div>`;
            searchResults.innerHTML += itemHTML;
        });
    } else {
        searchResults.innerHTML = '<p>No results found.</p>';
    }
};
