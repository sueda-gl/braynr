## Overview

Our project is is a full-stack application featuring a modern web interface built with React and TypeScript, and a robust Python backend powered by FastAPI. A key capability of the platform is the dynamic generation of educational animated videos from math formualas using Manim. 

## Features

*   **Interactive Frontend:** A user-friendly interface built with React, TypeScript, and Vite for a smooth learning experience.
*   **Powerful Backend API:** A FastAPI-based backend serving data and logic for the platform.
*   **Automated Video Generation:** Creates educational animations using the Manim library (e.g., explanations of concepts like OCR).
*   **AI Integration:** Multi agentic system
*   **Database Management:** Uses PostgreSQL with SQLAlchemy for data storage and Alembic for database migrations.
*   **Real-time Capabilities:** Includes WebSocket support for interactive features.
*   **Static Content Serving:** Serves static assets, including generated Manim videos.

## Technology Stack

*   **Frontend:**
    *   React
    *   TypeScript
    *   Vite
    *   CSS
*   **Backend:**
    *   Python 3
    *   FastAPI
    *   Uvicorn (ASGI Server)
    *   SQLAlchemy (ORM)
    *   Pydantic (Data Validation)
    *   Alembic (Database Migrations)
    *   WebSockets
*   **Video Generation:**
    *   Manim
*   **Optical Character Recognition (Library):**
    *   EasyOCR (listed as a dependency, for processing content for video generation or other tasks)
*   **Database:**
    *   PostgreSQL
*   **API:**
    *   RESTful API with auto-generated OpenAPI documentation.

## Project Structure

The project is organized into two main parts:

*   `app/frontend/`: Contains the React/TypeScript frontend application.
*   `app/backend/`: Contains the FastAPI Python backend application, including API routes, services, database models, and Manim video generation scripts.

The root directory also contains project-level configurations like `package.json` (likely for workspace management or scripts) and this README.

## Setup and Running

### Prerequisites

*   Node.js and npm (for frontend)
*   Python 3.8+ and pip (for backend)
*   PostgreSQL server running

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd app/backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Create a `.env` file in the `app/backend` directory by copying from a potential `.env.example` or by setting the following:
    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    GEMINI_API_KEY=your_gemini_api_key # Optional
    CORS_ORIGINS="http://localhost:5173,http://yourfrontenddomain.com" # Adjust as needed
    PROJECT_NAME="EdTech Platform"
    DEBUG=True # For development
    ```
    Ensure your PostgreSQL database is running and accessible with the credentials provided.

5.  **Run database migrations (if using Alembic and migrations are set up):**
    *(This step might require specific Alembic commands, typically `alembic upgrade head`)*
    For development, tables might be created on startup if `DEBUG=True` as seen in `main.py`.

6.  **Start the backend server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will typically be available at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd app/frontend  # Relative from project root, or ../frontend if already in app/backend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend will typically be available at `http://localhost:5173` (Vite's default).

## API Documentation

Once the backend server is running, API documentation (Swagger UI) is typically available at `http://localhost:8000/docs` and OpenAPI schema at `http://localhost:8000/api/v1/openapi.json`.

## Manim Video Generation

*   Manim scripts for generating videos are located in directories like `app/backend/static_content/manim_videos/<video_id>/script/`.
*   These scripts can be rendered using the Manim library. The output videos are served by the backend.

---

# EdTech Platform

## Overview

The EdTech Platform is a full-stack application designed to provide educational content and services. It features a modern web interface built with React and TypeScript, and a robust Python backend powered by FastAPI. A key capability of the platform is the dynamic generation of educational animated videos using Manim. It also appears to integrate AI functionalities via the Gemini API and utilizes a PostgreSQL database for data persistence.

## Features

*   **Interactive Frontend:** A user-friendly interface built with React, TypeScript, and Vite for a smooth learning experience.
*   **Powerful Backend API:** A FastAPI-based backend serving data and logic for the platform.
*   **Automated Video Generation:** Creates educational animations using the Manim library (e.g., explanations of concepts like OCR).
*   **AI Integration:** Leverages the Gemini API for potential AI-driven educational features.
*   **Database Management:** Uses PostgreSQL with SQLAlchemy for data storage and Alembic for database migrations.
*   **Real-time Capabilities:** Includes WebSocket support for interactive features.
*   **Static Content Serving:** Serves static assets, including generated Manim videos.

## Technology Stack

*   **Frontend:**
    *   React
    *   TypeScript
    *   Vite
    *   CSS
*   **Backend:**
    *   Python 3
    *   FastAPI
    *   Uvicorn (ASGI Server)
    *   SQLAlchemy (ORM)
    *   Pydantic (Data Validation)
    *   Alembic (Database Migrations)
    *   WebSockets
*   **Video Generation:**
    *   Manim
*   **Optical Character Recognition (Library):**
    *   EasyOCR (listed as a dependency, potentially for processing content for video generation or other tasks)
*   **Database:**
    *   PostgreSQL
*   **API:**
    *   RESTful API with auto-generated OpenAPI documentation.

## Project Structure

The project is organized into two main parts:

*   `app/frontend/`: Contains the React/TypeScript frontend application.
*   `app/backend/`: Contains the FastAPI Python backend application, including API routes, services, database models, and Manim video generation scripts.

The root directory also contains project-level configurations like `package.json` (likely for workspace management or scripts) and this README.

## Setup and Running

### Prerequisites

*   Node.js and npm (for frontend)
*   Python 3.8+ and pip (for backend)
*   PostgreSQL server running

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd app/backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Create a `.env` file in the `app/backend` directory by copying from a potential `.env.example` or by setting the following:
    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    GEMINI_API_KEY=your_gemini_api_key # Optional
    CORS_ORIGINS="http://localhost:5173,http://yourfrontenddomain.com" # Adjust as needed
    PROJECT_NAME="EdTech Platform"
    DEBUG=True # For development
    ```
    Ensure your PostgreSQL database is running and accessible with the credentials provided.

5.  **Run database migrations (if using Alembic and migrations are set up):**
    *(This step might require specific Alembic commands, typically `alembic upgrade head`)*
    For development, tables might be created on startup if `DEBUG=True` as seen in `main.py`.

6.  **Start the backend server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will typically be available at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd app/frontend  # Relative from project root, or ../frontend if already in app/backend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend will typically be available at `http://localhost:5173` (Vite's default).

## API Documentation

Once the backend server is running, API documentation (Swagger UI) is typically available at `http://localhost:8000/docs` and OpenAPI schema at `http://localhost:8000/api/v1/openapi.json`.

## Manim Video Generation

*   Manim scripts for generating videos are located in directories like `app/backend/static_content/manim_videos/<video_id>/script/`.
*   These scripts can be rendered using the Manim library. The output videos are served by the backend.

---

# EdTech Platform

## Overview

The EdTech Platform is a full-stack application designed to provide educational content and services. It features a modern web interface built with React and TypeScript, and a robust Python backend powered by FastAPI. A key capability of the platform is the dynamic generation of educational animated videos using Manim. It also appears to integrate AI functionalities via the Gemini API and utilizes a PostgreSQL database for data persistence.

## Features

*   **Interactive Frontend:** A user-friendly interface built with React, TypeScript, and Vite for a smooth learning experience.
*   **Powerful Backend API:** A FastAPI-based backend serving data and logic for the platform.
*   **Automated Video Generation:** Creates educational animations using the Manim library (e.g., explanations of concepts like OCR).
*   **AI Integration:** Leverages the Gemini API for potential AI-driven educational features.
*   **Database Management:** Uses PostgreSQL with SQLAlchemy for data storage and Alembic for database migrations.
*   **Real-time Capabilities:** Includes WebSocket support for interactive features.
*   **Static Content Serving:** Serves static assets, including generated Manim videos.

## Technology Stack

*   **Frontend:**
    *   React
    *   TypeScript
    *   Vite
    *   CSS
*   **Backend:**
    *   Python 3
    *   FastAPI
    *   Uvicorn (ASGI Server)
    *   SQLAlchemy (ORM)
    *   Pydantic (Data Validation)
    *   Alembic (Database Migrations)
    *   WebSockets
*   **Video Generation:**
    *   Manim
*   **Optical Character Recognition (Library):**
    *   EasyOCR (listed as a dependency, potentially for processing content for video generation or other tasks)
*   **Database:**
    *   PostgreSQL
*   **API:**
    *   RESTful API with auto-generated OpenAPI documentation.

## Project Structure

The project is organized into two main parts:

*   `app/frontend/`: Contains the React/TypeScript frontend application.
*   `app/backend/`: Contains the FastAPI Python backend application, including API routes, services, database models, and Manim video generation scripts.

The root directory also contains project-level configurations like `package.json` (likely for workspace management or scripts) and this README.

## Setup and Running

### Prerequisites

*   Node.js and npm (for frontend)
*   Python 3.8+ and pip (for backend)
*   PostgreSQL server running

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd app/backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Create a `.env` file in the `app/backend` directory by copying from a potential `.env.example` or by setting the following:
    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    GEMINI_API_KEY=your_gemini_api_key # Optional
    CORS_ORIGINS="http://localhost:5173,http://yourfrontenddomain.com" # Adjust as needed
    PROJECT_NAME="EdTech Platform"
    DEBUG=True # For development
    ```
    Ensure your PostgreSQL database is running and accessible with the credentials provided.

5.  **Run database migrations (if using Alembic and migrations are set up):**
    *(This step might require specific Alembic commands, typically `alembic upgrade head`)*
    For development, tables might be created on startup if `DEBUG=True` as seen in `main.py`.

6.  **Start the backend server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will typically be available at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd app/frontend  # Relative from project root, or ../frontend if already in app/backend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend will typically be available at `http://localhost:5173` (Vite's default).

## API Documentation

Once the backend server is running, API documentation (Swagger UI) is typically available at `http://localhost:8000/docs` and OpenAPI schema at `http://localhost:8000/api/v1/openapi.json`.

## Manim Video Generation

*   Manim scripts for generating videos are located in directories like `app/backend/static_content/manim_videos/<video_id>/script/`.
*   These scripts can be rendered using the Manim library. The output videos are served by the backend.

---

This README provides a comprehensive overview to help new users and contributors understand, set up, and run the EdTech Platform.

Note: This project was developed in a constrained hackathon setting and may require setup tweaks to run locally.


