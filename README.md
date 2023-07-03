# Auction Site

This is an online auction site built with Django. Users can create listings for various items, place bids on listings, add listings to their watchlist, and interact through comments.

## Features

- User registration and authentication system
- Creating, viewing, and closing listings
- Placing bids on active listings
- Adding listings to the watchlist
- Commenting on listings
- Categorizing listings
- Viewing listings by category
- Viewing a personal watchlist

## Installation

1. Clone the repository:

```shell
git clone https://github.com/your-username/commerce.git
```

2. Change into the project directory:

```shell
cd commerce
```

3. Create a virtual environment (optional but recommended):

```shell
python3 -m venv env
source env/bin/activate
```

4. Install the dependencies:

```shell
pip install -r requirements.txt
```

5. Apply the database migrations:

```shell
python manage.py migrate
```

6. Run the development server:

```shell
python manage.py runserver
```

7. Open your web browser and visit `http://localhost:8000` to access the site.

## Usage

- Create an account or login if you already have one.
- Browse the active listings on the homepage.
- Click on a listing to view its details, place bids, or add it to your watchlist.
- Use the navigation menu to access your watchlist or view listings by category.
- Create your own listings by clicking on "Create Listing" in the navigation menu.
- Interact with other users through comments on listings.
