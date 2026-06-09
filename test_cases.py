# test_cases.py

test_cases = [
    {
        "question": "How many customers are there?",
        "expected_sql": "SELECT COUNT(*) FROM customer;",
    },
    {
        "question": "List all film titles",
        "expected_sql": "SELECT title FROM film;",
    },
    {
        "question": "How many films are in the Action category?",
        "expected_sql": """
            SELECT COUNT(*) FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE c.name = 'Action';
        """,
    },
    {
        "question": "Who are the top 5 customers by total payments?",
        "expected_sql": """
            SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total
            FROM customer c
            JOIN payment p ON c.customer_id = p.customer_id
            GROUP BY c.customer_id
            ORDER BY total DESC
            LIMIT 5;
        """,
    },
    {
        "question": "List all actors with last name JONES",
        "expected_sql": """
            SELECT first_name, last_name
            FROM actor
            WHERE last_name = 'JONES';
        """,
    },
    {
        "question": "How many films are there per category?",
        "expected_sql": """
            SELECT c.name, COUNT(*) AS total
            FROM category c
            JOIN film_category fc ON c.category_id = fc.category_id
            GROUP BY c.name;
        """,
    },
    {
        "question": "Which store has more customers?",
        "expected_sql": """
            SELECT store_id, COUNT(*) AS total
            FROM customer
            GROUP BY store_id
            ORDER BY total DESC
            LIMIT 1;
        """,
    },
    {
        "question": "List all films longer than 2 hours",
        "expected_sql": """
            SELECT title, length
            FROM film
            WHERE length > 120;
        """,
    },
    {
        "question": "What is the average film rental duration?",
        "expected_sql": """
            SELECT AVG(rental_duration)
            FROM film;
        """,
    },
    {
        "question": "List all cities in India",
        "expected_sql": """
            SELECT city
            FROM city
            JOIN country ON city.country_id = country.country_id
            WHERE country.country = 'India';
        """,
    },
]