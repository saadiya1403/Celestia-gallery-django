# Celestia

Celestia is a web application that allows users to upload pictures, browse other users' pictures, and like them. The app includes user authentication features such as signup, login, and logout. It is built using Django for the backend and Bootstrap for the frontend UI.

## Features

* User signup and login/logout
* Upload pictures with captions
* View a gallery of uploaded pictures
* Like/unlike pictures
* Responsive design with Bootstrap

## Technologies Used

* Django (Python Web Framework)
* Bootstrap (CSS Framework)
* SQLite (default Django database)
* HTML, CSS, JavaScript

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/celestia.git
cd celestia
```

2. **Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Create a superuser (optional, for admin access)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. **Open the app**

Go to `http://127.0.0.1:8000/` in your browser.

## Usage

* Sign up for an account or log in if you already have one.
* Upload your pictures from the upload page.
* Browse the gallery to see pictures uploaded by all users.
* Click the like button on any picture to show your appreciation.
* Log out when done.

## Project Structure

* `celestia/` - Django project folder
* `media/` - Uploaded pictures are stored here
* `templates/` - HTML templates using Bootstrap
* `static/` - CSS, JS, images
* `requirements.txt` - Python dependencies list

## Future Improvements

* Add comments on pictures
* Pagination on gallery pages
* User profile pages
* Notifications for likes
* Image filters and editing options

## Screenshot
![image](https://github.com/user-attachments/assets/44905ebd-f53d-409e-a446-6bafd2541ee3)

