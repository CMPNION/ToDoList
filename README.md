# Todo List Application

This is a simple Todo List application built with FastAPI and SQLAlchemy. The application allows users to register, log in, create, and manage their todo tasks.

## Project Structure

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/register` to register a new user.

## Project Files

### [database.py](http://_vscodecontentref_/7)

This file sets up the database connection using SQLAlchemy.

### [models.py](http://_vscodecontentref_/8)

This file defines the database models for [User](http://_vscodecontentref_/9) and [Todo](http://_vscodecontentref_/10).

### [main.py](http://_vscodecontentref_/11)

This file contains the main FastAPI application and the route handlers for user registration, login, logout, and todo management.

### [templates](http://_vscodecontentref_/12)

This directory contains the HTML templates for the application.

- [login.html](http://_vscodecontentref_/13): The login page template.
- [register.html](http://_vscodecontentref_/14): The registration page template.
- [todos.html](http://_vscodecontentref_/15): The todo list page template.

## Routes

### User Registration

- **GET /register**: Display the registration form.
- **POST /register**: Handle user registration.

### User Login

- **GET /login**: Display the login form.
- **POST /login**: Handle user login.

### User Logout

- **GET /logout**: Log out the user and clear the session.

### Todo Management

- **GET /todos**: Display the user's todo list.
- **POST /todos**: Create a new todo task.
- **POST /todos/{todo_id}/toggle**: Toggle the completion status of a todo task.

## Dependencies

- FastAPI
- SQLAlchemy
- Jinja2
- Passlib
- Uvicorn

## License

This project is licensed under the MIT License.