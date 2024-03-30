# Hiring App

Hiring App is a Django project designed to streamline the recruitment process for both recruiters and applicants. Recruiters can post job listings, review applications, and manage the hiring process, while applicants can search for job listings, submit applications, and track their application status.

## Installation

1. Clone the repository:

    ```bash
   https://github.com/krishnaa192/Hire.git
    cd Hiring
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Access the admin interface by logging in with the superuser account created earlier at `http://localhost:8000/admin`.
2. Create job listings, review applications, and manage the hiring process from the admin dashboard.
3. Applicants can sign up for an account, create profiles, search for job listings, and submit applications.
4. Recruiters can post job listings, review applications, communicate with applicants, and make hiring decisions.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for your own purposes.
