# AI-Powered Job Application Tracker API

A robust, RESTful backend API designed to track job applications and provide AI-driven interview preparation. Built with Flask and SQLAlchemy, this system features secure JWT authentication, dynamic relational database mapping, and a fully integrated AI coach that generates customized interview questions, technical answers, and downloadable PDF cover letters.

## 🚀 Core Features

*   **Secure Authentication:** End-to-end JWT (JSON Web Token) protection. All application and AI routes are locked behind Bearer token authorization.
*   **Smart Relational Database:** Implements a "Find or Create" pattern. Users simply pass a `company_name` string, and the backend silently handles the relational `company_id` mapping to prevent duplicate database entries.
*   **Integrated AI Interview Coach:** Powered by Google's Gemini API, contextualized by the user's specific job role, current interview round, and personal notes.
    *   `initial_questions` / `more_questions`: Generates 5 highly specific technical questions.
    *   `answers`: Provides deep-dive technical answers to provided questions.
    *   `cover_letter`: Generates a professional, dynamically formatted PDF cover letter instantly saved to the server and downloaded to the client.
*   **Interactive Documentation:** Fully documented using Flasgger (Swagger UI), allowing front-end developers or recruiters to test the API directly from the browser.

## 🛠️ Tech Stack

*   **Language:** Python 3
*   **Framework:** Flask
*   *   **Database:** SQLite (MVP / Local Development)
*   **ORM:** Flask-SQLAlchemy
*   **Authentication:** Flask-JWT-Extended
*   **AI Integration:** google-generativeai (Gemini 2.5 Flash)
*   **PDF Generation:** fpdf2
*   **Documentation:** Flasgger (Swagger)
*   **Server:** Gunicorn

## ⚙️ Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/ananya-1-a/job-app-tracker.git>
   cd job-application-tracker