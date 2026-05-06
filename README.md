# AI-Powered Job Application Tracker API

A robust, RESTful backend API designed to track job applications and provide AI-driven interview preparation. Built with Flask and SQLAlchemy, this system features secure JWT authentication, dynamic relational database mapping, and a fully integrated AI coach that generates customized interview questions, technical answers, and downloadable PDF cover letters.

##  Core Features

*   **Secure Authentication:** End-to-end JWT (JSON Web Token) protection. All application and AI routes are locked behind Bearer token authorization.
*   **Production-Grade Relational Database:** Transitioned from local SQLite to a highly scalable **PostgreSQL** database hosted via **Supabase**. Implements a "Find or Create" pattern where users pass a `company_name` string, and the backend silently handles the relational `company_id` mapping to prevent duplicate entries.
*   **Clean RESTful AI Architecture:** Powered by Google's Gemini API, the AI engine is contextualized by the user's specific job role, interview round, and personal notes. The AI features are cleanly split into dedicated, isolated endpoints for maximum API discoverability:
    *   `POST /ai/questions`: Generates 5 highly specific technical questions.
    *   `POST /ai/answers`: Provides deep-dive technical answers to provided questions.
    *   `POST /ai/cover-letter`: Generates a professional, dynamically formatted PDF cover letter instantly saved to the server and downloaded to the client.
*   **Interactive Documentation:** Fully documented using Flasgger (Swagger UI), allowing front-end developers or recruiters to test the API directly from the browser.

##  Tech Stack

*   **Language:** Python 3
*   **Framework:** Flask
*   **Database:** PostgreSQL (Hosted via Supabase)
*   **ORM:** Flask-SQLAlchemy
*   **Authentication:** Flask-JWT-Extended
*   **AI Integration:** google-generativeai (Gemini 2.5 Flash)
*   **PDF Generation:** fpdf2
*   **Documentation:** Flasgger (Swagger)
*   **Production Server:** Gunicorn

##  Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/ananya-1-a/job-app-tracker.git>
   cd job-application-tracker