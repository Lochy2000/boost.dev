# Boost.dev  <a id="top"/>
<img src=""> 

## Introduction


Live site: [Boost.dev]()

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