# Learn Assistant

**Learn Assistant** is a website designed to help users study new topics effectively through random question testing. Users can upload a list of questions and quiz themselves in a random order, which is more engaging than reading questions sequentially. Future plans include integrating AI to automatically check answers.

---

## Features

* Store questions and answers in the database.
* REST API for creating, reading, updating, and deleting questions.
* Retrieve a random question via API.
* Simple web interface to display random questions and reveal answers.
* Clean and user-friendly design with buttons to show question and answer.

---

## Technology Stack

* Python 3.x
* Django
* Django REST Framework
* HTML, CSS, JavaScript (for frontend)

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/learn-assistant.git
   cd learn-assistant
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. Open in your browser:
   `http://localhost:8000/random/question/` — to access the random question page.

---

## API Endpoints

* `GET /api/random/` — get a random question in JSON format.
* `GET/POST/PUT/DELETE /api/learn/` — full CRUD operations for questions.

---

## Future Plans

* AI integration to automatically evaluate and provide feedback on answers.
* Import/export question lists functionality.
* Enhanced interface for easy question creation and editing.

---

## Contact

If you have any questions or suggestions, feel free to contact me via GitHub or email.

