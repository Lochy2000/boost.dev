# Boost.dev  <a id="top"/>
<img src=""> 

## Introduction

This project was made for the April Hackthon - "Unmask The Coder" by Code Institute.

It aims to show users that they have good skills and to help dealing with Imposter Syndrome.

The idea for the project came from one of the members and was consistent with the suggested projects by CI - Hack Team. Incorporating more than one idea of those suggested.

Live site: [Boost.dev]( )

## Table of Contents
- [Boost.dev]()
    - [Introduction](#introduction)
    - [Table of Contents](#table-of-contents)
    - [Overview](#overview)
- [Ux - User Experience](#ux---user-experience)
    - [Colour Scheme](#colour-scheme)
    - [Contrast Check](#contrast-check)
    - [Typography](#typography)
- [Project Planning](#project-planning)
    - [Strategy Plane](#strategy-plane)
      - [Agile Methodologies](#agile-methodologies)
      - [Users](#users)
      - [MoSCoW Prioritorization](#moscow-prioritorization)
      - [User Stories](#user-stories)
    - [Scope Plane](#scope-plane)
    - [Structural Plane](#structural-plane)
      - [Homepage](#homepage)
        - [Footer](#footer)
        - [Pagination](#pagination)
      - [Profile](#profile)
      - [Create Post](#create-post)
    - [Skeleton & Surface Planes](#skeleton--surface-planes)
      - [Wireframes](#wireframes)
      - [Imagery](#imagery)
- [Technologies Used](#technologies-used)
    - [Languages and Technologies](#languages-and-technologies)
    - [Libraries](#libraries)
    - [Tools and Programs](#tools-and-programs)
- [Deployment](#deployment)
    - [Connecting to GigHub](#connecting-to-github)
    - [Django Project Setup](#django-project-setup)
    - [Cloudinary API](#cloudinary-api)
    - [Heroku Deployment](#heroku-deployment)
    - [Clone Project](#clone-project)
    - [Fork Project](#fork-project)
- [ERD](#erd)
- [Bugs to fix](#bugs-to-fix)
- [AI Implementation and Orchestration](#ai-implementaion-and-orchestration)
    - [Code Generation](#code-generation)
    - [Debugging](#debugging)
    - [Code Optimization](#code-optimisation)
    - [Impact on Workflow](#impact-on-workflow)
- [Testing](#testing)
    - [HTML Validation](#html-validation)
    - [CSS Validation](#css-validation)
    - [Lighthouse Audit](#lighthouse-audit)
    - [Python Tests & Check](#python-tests--check)
    - [JavaScript Check](#javascript-check)
    - [Manual Testing](#manual-testing)
- [Future Features](#future-features)
- [Credits](#credits)
    - [Code References](#code-references)
    - [Media References](#media-references)
    - [Acknowledgments](#acknowledgements)
    - [Owner Details](#owner-details)


[Back to top](#top)

# Overview
Boost.dev is a simple site with information about Imposter Syndrome that many developers can go through with different symptoms, and it aims to provide information about this subject and also present ideas about how the user can try to overcome this.<br>

It's meant to be an interactive and responsive site.

  - Users have access to posts related to the main subject
  - Can showcase their apps/sites for others to see
  - Users can do coding challenges in different levels

The site is designed to be responsive in different screen sizes.

Our main goal is to let the user know that they are great developers and hopefully to let them improve their confidence with coding and to help others in similar situation, creating a supporting community for developers that have low-confidence.

## UX - User Experience







Colours - checked against WCAG for contrast 

#581CA0 - purple (from the canva mind map)
#312fa6 - indigo 
#b12e5d - roseberry
#0088cc - bright blue
#121212 - dark background

| Colour      | WCAG Ratio (against #121212) | WCAG Contrast          |
|-------------|-------------------------------|-------------------------|
| Purple      | Pass (7.1:1)                 | ✅ AAA                 |
| Indigo      | Pass (8.23:1)                | ✅✅ AAA               |
| Roseberry   | Pass (6.71:1)                | ✅✅ AAA               |
| Bright Blue | Pass (6.95:1)                | ✅✅ AAA               |




## Technologies Used
### Languages and Technologies
  - HTML
  - CSS
  - JavaScript
  - Python
  - PostgreSQL
  - Git
  - Github
  - VS-Code
  - Django
  - Cloudinary
  - Heroku

### Libraries
  - Bootstrap v5.2.3
  - Django v3.2.19
  - Django AllAuth v0.54.0
  - Django Crispy Forms v2.0
  - Google Fonts
  - Crispy Bootstrap5 v0.7
  - Django Summernote v0.8.2
  - Pillow v9.5

### Tools and Programs
  - Balsamiq wireframe
  - MSCopilot AI
  - VS-Code Copilot
  - ChatGPT

[Back to top](#top)

## Deployment

### Connecting to GitHub
To begin this project from scratch, you must first create a new GitHub repository using the Code Institute's Template. This template provides the relevant tools to get you started. To use this template:

  - Log in to GitHub or create a new account.<br>
  - Navigate to the above CI Full Template.<br>
  - Click 'Use this template' -> 'Create a new repository'.<br>
  - Choose a new repository name and click 'Create repository from template'.<br>
  - In your new repository space, click the purple CodeAnywhere (if this is your IDE of choice) button to generate a new workspace.<br>

### Django Project Setup<br>
Install Django and supporting libraries:<br>
  - pip3 install 'django<4' gunicorn<br>
  - pip3 install dj_database_url psycopg2<br>
  - pip3 install dj3-cloudinary-storage<br>

Once you have installed any relevant dependencies or libraries, such as the ones listed above, it is important to create a requirements.txt file and add all installed libraries to it with the pip3 freeze --local > requirements.txt command in the terminal.

Create a new Django project in the terminal django-admin startproject ems .

Create a new app eg. python3 mangage.py startapp events

Add this to list of INSTALLED_APPS in settings.py - 'booking',

Create a superuser for the project to allow Admin access and enter credentials: python3 manage.py createsuperuser

Migrate the changes with commands: python3 manage.py migrate

An env.py file must be created to store all protected data such as the 
DATABASE_URL and SECRET_KEY. These may be called upon in your project's settings.py file along with your Database configurations. The env.py file must be added to your gitignore file so that your important, protected information is not pushed to public viewing on GitHub. For adding to env.py:

  - import os
  - os.environ["DATABASE_URL"]="<copiedURLfrom postgresql://neondb_owner>"
  - os.environ["SECRET_KEY"]="my_super^secret@key"

For adding to settings.py:

  - import os
  - import dj_database_url
  - if os.path.exists("env.py"):
  - import env
  - SECRET_KEY = os.environ.get('SECRET_KEY') (actual key hidden within env.py)

Replace DATABASES with:

DATABASES = {<br>
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))<br>
  }

Set up the templates directory in settings.py:
  - Under BASE_DIR enter TEMPLATES_DIR = os.path.join(BASE_DIR, ‘templates’)
  - Update TEMPLATES = 'DIRS': [TEMPLATES_DIR] with:<br>
  os.path.join(BASE_DIR, 'templates'),<br>
  os.path.join(BASE_DIR, 'templates', 'allauth')<br>
  - Create the media, static and templates directories in top level of project file in IDE workspace.<br>
  
A Procfile must be created within the project repo for Heroku deployment with the following placed within it: web: gunicorn ems.wsgi

Make the necessary migrations again.

[Back to top](#top)

### Cloudinary API
Cloudinary provides a cloud hosting solution for media storage. All users uploaded images in the FreeFid project are hosted here.

Set up a new account at Cloudinary and add your Cloudinary API environment variable to your env.py and Heroku Config Vars. In your project workspace:

  - Add Cloudinary libraries to INSTALLED_APPS in settings.py
  - In the order:<br>
   'cloudinary_storage',<br>
   'django.contrib.staticfiles',  <br>
   'cloudinary',<br>

  - Add to env.py and link up with settings.py: os.environ["CLOUDINARY_URL"]="cloudinary://...."
  - Set Cloudinary as storage for media and static files in settings.py:
  - STATIC_URL = '/static/'<br>
  STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'<br>  
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]<br>
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')‌<br>  
  MEDIA_URL = '/media/'<br>  
  DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'<br>

### Heroku deployment
To start the deployment process , please follow the below steps:

  - Log in to Heroku or create an account if you are a new user.

  - Once logged in, in the Heroku Dashboard, navigate to the 'New' button in the top, right corner, and select 'Create New App'.

  - Enter an app name and choose your region. Click 'Create App'.

  - In the Deploy tab, click on the 'Settings', reach the 'Config Vars' section and click on 'Reveal Config Vars'. Here you will enter KEY:VALUE pairs for the app to run successfully. The KEY:VALUE pairs that you will need are your:<br>
CLOUDINARY_URL: cloudinary://....<br>
DATABASE_URL:postgres://...<br>
DISABLE_COLLECTSTATIC of value '1' (N.B Remove this Config Var before deployment),<br>
PORT:8000<br>
SECRET_KEY and value<br>

  - Add the Heroku host name into ALLOWED_HOSTS in your projects settings.py file ->  ['800-nielmc-django-project-lxqprmm3qz.us2.codeanyapp.com', '.herokuapp.com', 'localhost', '127.0.0.1'].

  - Once you are sure that you have set up the required files including your requirements.txt and Procfile, you have ensured that DEBUG=False, save your project, add the files, commit for initial deployment and push the data to GitHub.

  - Go to the 'Deploy' tab and choose GitHub as the Deployment method.

  - Search for the repository name, select the branch that you would like to build from, and connect it via the 'Connect' button.

  - Choose from 'Automatic' or 'Manual' deployment options, I chose the 'Manual' deployment method. Click 'Deploy Branch'.

  - Once the waiting period for the app to build has finished, click the 'View' link to bring you to your newly deployed site. If you receive any errors, Heroku will display a reason in the app build log for you to investigate. DISABLE_COLLECTSTATIC may be removed from the Config Vars once you have saved and pushed an image within your project, as can PORT:8000.

[Back to top](#top)

### Clone project
A local clone of this repository can be made on GitHub. Please follow the below steps:

  - Navigate to GitHub and log in.
  - Kids Art Repository can be found at this location.
  - Above the repository file section, locate the 'Code' button.
  - Click on this button and choose your clone method from HTTPS, SSH or GitHub CLI, copy the URL to your clipboard by clicking the 'Copy' button.
  - Open your Git Bash Terminal.
  - Change the current working directory to the location you want the cloned directory to be made.
  - Type git clone and paste in the copied URL from step 4.
  - Press 'Enter' for the local clone to be created.
  - Using the pip3 install -r requirements.txt command, the dependencies and libraries needed for FreeFido will be installed.
  - Set up your env.py file and from the above steps for Cloudinary and NeonSQL, gather the Cloudinary API key and the Neon SQL url for additon to your code.
  - Ensure that your env.py file is placed in your .gitignore file and follow the remaining steps in the above Django Project Setup section before pushing your code to GitHub.

### Fork Project
A copy of the original repository can be made through GitHub. Please follow the below steps to fork this repository:

  - Navigate to GitHub and log in.
  - Once logged in, navigate to this repository using this link Eventia Repository.
  - Above the repository file section and to the top, right of the page is the 'Fork' button, click on this to make a fork of this repository.
  - You should now have access to a forked copy of this repository in your Github account.
  - Follow the above Django Project Steps if you wish to work on the project.

### Connecting to GitHub
To begin this project from scratch, you must first create a new GitHub repository using the Code Institute's Template. This template provides the relevant tools to get you started. To use this template:

  - Log in to GitHub or create a new account.<br>
  - Navigate to the above CI Full Template.<br>
  - Click 'Use this template' -> 'Create a new repository'.<br>
  - Choose a new repository name and click 'Create repository from template'.<br>
  - In your new repository space, click the purple CodeAnywhere (if this is your IDE of choice) button to generate a new workspace.<br>

### Django Project Setup<br>
Install Django and supporting libraries:<br>
  - pip3 install 'django<4' gunicorn<br>
  - pip3 install dj_database_url psycopg2<br>
  - pip3 install dj3-cloudinary-storage<br>

Once you have installed any relevant dependencies or libraries, such as the ones listed above, it is important to create a requirements.txt file and add all installed libraries to it with the pip3 freeze --local > requirements.txt command in the terminal.

Create a new Django project in the terminal django-admin startproject ems .

Create a new app eg. python3 mangage.py startapp events

Add this to list of INSTALLED_APPS in settings.py - 'booking',

Create a superuser for the project to allow Admin access and enter credentials: python3 manage.py createsuperuser

Migrate the changes with commands: python3 manage.py migrate

An env.py file must be created to store all protected data such as the 
DATABASE_URL and SECRET_KEY. These may be called upon in your project's settings.py file along with your Database configurations. The env.py file must be added to your gitignore file so that your important, protected information is not pushed to public viewing on GitHub. For adding to env.py:

  - import os
  - os.environ["DATABASE_URL"]="<copiedURLfrom postgresql://neondb_owner>"
  - os.environ["SECRET_KEY"]="my_super^secret@key"

For adding to settings.py:

  - import os
  - import dj_database_url
  - if os.path.exists("env.py"):
  - import env
  - SECRET_KEY = os.environ.get('SECRET_KEY') (actual key hidden within env.py)

Replace DATABASES with:

DATABASES = {<br>
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))<br>
  }

Set up the templates directory in settings.py:
  - Under BASE_DIR enter TEMPLATES_DIR = os.path.join(BASE_DIR, ‘templates’)
  - Update TEMPLATES = 'DIRS': [TEMPLATES_DIR] with:<br>
  os.path.join(BASE_DIR, 'templates'),<br>
  os.path.join(BASE_DIR, 'templates', 'allauth')<br>
  - Create the media, static and templates directories in top level of project file in IDE workspace.<br>
  
A Procfile must be created within the project repo for Heroku deployment with the following placed within it: web: gunicorn ems.wsgi

Make the necessary migrations again.

[Back to top](#top)

### Cloudinary API
Cloudinary provides a cloud hosting solution for media storage. All users uploaded images in the FreeFid project are hosted here.

Set up a new account at Cloudinary and add your Cloudinary API environment variable to your env.py and Heroku Config Vars. In your project workspace:

  - Add Cloudinary libraries to INSTALLED_APPS in settings.py
  - In the order:<br>
   'cloudinary_storage',<br>
   'django.contrib.staticfiles',  <br>
   'cloudinary',<br>

  - Add to env.py and link up with settings.py: os.environ["CLOUDINARY_URL"]="cloudinary://...."
  - Set Cloudinary as storage for media and static files in settings.py:
  - STATIC_URL = '/static/'<br>
  STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'<br>  
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]<br>
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')‌<br>  
  MEDIA_URL = '/media/'<br>  
  DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'<br>

### Heroku deployment
To start the deployment process , please follow the below steps:

  - Log in to Heroku or create an account if you are a new user.

  - Once logged in, in the Heroku Dashboard, navigate to the 'New' button in the top, right corner, and select 'Create New App'.

  - Enter an app name and choose your region. Click 'Create App'.

  - In the Deploy tab, click on the 'Settings', reach the 'Config Vars' section and click on 'Reveal Config Vars'. Here you will enter KEY:VALUE pairs for the app to run successfully. The KEY:VALUE pairs that you will need are your:<br>
CLOUDINARY_URL: cloudinary://....<br>
DATABASE_URL:postgres://...<br>
DISABLE_COLLECTSTATIC of value '1' (N.B Remove this Config Var before deployment),<br>
PORT:8000<br>
SECRET_KEY and value<br>

  - Add the Heroku host name into ALLOWED_HOSTS in your projects settings.py file ->  ['800-nielmc-django-project-lxqprmm3qz.us2.codeanyapp.com', '.herokuapp.com', 'localhost', '127.0.0.1'].

  - Once you are sure that you have set up the required files including your requirements.txt and Procfile, you have ensured that DEBUG=False, save your project, add the files, commit for initial deployment and push the data to GitHub.

  - Go to the 'Deploy' tab and choose GitHub as the Deployment method.

  - Search for the repository name, select the branch that you would like to build from, and connect it via the 'Connect' button.

  - Choose from 'Automatic' or 'Manual' deployment options, I chose the 'Manual' deployment method. Click 'Deploy Branch'.

  - Once the waiting period for the app to build has finished, click the 'View' link to bring you to your newly deployed site. If you receive any errors, Heroku will display a reason in the app build log for you to investigate. DISABLE_COLLECTSTATIC may be removed from the Config Vars once you have saved and pushed an image within your project, as can PORT:8000.

[Back to top](#top)

### Clone project
A local clone of this repository can be made on GitHub. Please follow the below steps:

  - Navigate to GitHub and log in.
  - Kids Art Repository can be found at this location.
  - Above the repository file section, locate the 'Code' button.
  - Click on this button and choose your clone method from HTTPS, SSH or GitHub CLI, copy the URL to your clipboard by clicking the 'Copy' button.
  - Open your Git Bash Terminal.
  - Change the current working directory to the location you want the cloned directory to be made.
  - Type git clone and paste in the copied URL from step 4.
  - Press 'Enter' for the local clone to be created.
  - Using the pip3 install -r requirements.txt command, the dependencies and libraries needed for FreeFido will be installed.
  - Set up your env.py file and from the above steps for Cloudinary and NeonSQL, gather the Cloudinary API key and the Neon SQL url for additon to your code.
  - Ensure that your env.py file is placed in your .gitignore file and follow the remaining steps in the above Django Project Setup section before pushing your code to GitHub.

### Fork Project
A copy of the original repository can be made through GitHub. Please follow the below steps to fork this repository:

  - Navigate to GitHub and log in.
  - Once logged in, navigate to this repository using this link Eventia Repository.
  - Above the repository file section and to the top, right of the page is the 'Fork' button, click on this to make a fork of this repository.
  - You should now have access to a forked copy of this repository in your Github account.
  - Follow the above Django Project Steps if you wish to work on the project.

[Back to top](#top)

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

