# Chatbot with Flask & Docker

This project is a chatbot built using Flask that provides course recommendations based on user queries. The application is containerized using Docker for easy deployment.

## Features
- Chat interface to ask about courses.
- Fetches course details including title, description, price per session, total price, and number of lessons.
- Integrated with a Flask backend.
- Deployed using Docker.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Docker & Docker Compose (optional)

### Clone the Repository
```bash
git clone https://github.com/your-repo/chatbot-flask.git
cd chatbot-flask
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Flask App
```bash
python app.py
```

The app will be accessible at `http://127.0.0.1:5000`.

## Docker Setup

### Build the Docker Image
```bash
docker build -t flask-chatbot .
```

### Run the Docker Container
```bash
docker run -p 5000:5000 flask-chatbot
```

### Run with Docker Compose (Optional)
```bash
docker-compose up -d
```

## API Endpoints

### Query Courses
**Endpoint:** `/search?query=<your_query>`

**Method:** `GET`

**Response Format:**
```json
{
    "results": [
        {
            "title": "Course Title",
            "description": "Short Description",
            "price_per_session": "$30",
            "number_of_lessons": "8",
            "total_price": "$240",
            "course_link": "https://example.com/course"
        }
    ]
}
```

## File Structure
```
chatbot-flask/
│-- app.py
│-- Dockerfile
│-- requirements.txt
│-- static/
│   │-- style.css
│   │-- script.js
│-- templates/
│   │-- index.html
│-- README.md
```

## License
This project is licensed under the MIT License.

---
### Author
Your Name | [GitHub](https://github.com/your-profile) | [LinkedIn](https://linkedin.com/in/your-profile)

