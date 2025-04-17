## Tailwind CSS Setup

These instructions will guide you through setting up Tailwind CSS in your Django project using django-tailwind.

### Prerequisites

-   Node.js and npm installed. You can download them from [https://nodejs.org](https://nodejs.org).

### Installation

1.  Install django-tailwind:

    ```bash
    pip install django-tailwind==4.0.1
    ```

2.  Initialize Tailwind CSS for your app (replace "theme" with your app name if different):

    ```bash
    python manage.py tailwind init --app-name theme
    ```

3.  Add `tailwind` and your app to `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        ...
        'tailwind',
        'theme',
    ]
    ```

    Also, add `TAILWIND_APP_NAME = 'theme'` to your `settings.py` file.

4.  Install the npm dependencies:

    ```bash
    python manage.py tailwind install
    ```