# ChatX - A Django Chat Application

## Project Overview

ChatX is a real-time chat application built using the Django framework. It provides a platform for users to register, log in, and engage in real-time conversations. The application is designed to be simple, efficient, and scalable.

## Features

*   **User Authentication:** Secure user registration and login system.
*   **Real-time Chat:** Instant messaging capabilities.
*   **User Profiles:** Basic user profile management.
*   **Responsive Design:** User-friendly interface across various devices (though this may need further development).

## Installation

To set up ChatX on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/old-droid/ChatX.git
    cd ChatX
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: A `requirements.txt` file is assumed to exist. If not, you'll need to create one with Django and any other necessary packages.)

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

## Usage

1.  **Register:** Navigate to the registration page (`/register/`) to create a new account.
2.  **Login:** After registration, log in using your credentials.
3.  **Chat:** Once logged in, you can access the chat interface and start communicating with other users.

## Technologies Used

*   **Backend:** Django (Python Web Framework)
*   **Database:** SQLite (default for development)
*   **Frontend:** HTML, CSS (with `custom_admin.css` and `style.css` for styling)

## License

This project is licensed under the anything License - see the `LICENSE.md` file for details.

## Contributing

Contributions are welcome! Please feel free to fork the repository, create a new branch, and submit a pull request.
