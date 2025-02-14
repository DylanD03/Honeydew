## Main Branch Test State: [![Main Branch](https://github.com/uofa-cmput404/f24-project-honeydew/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/uofa-cmput404/f24-project-honeydew/actions/workflows/django.yml)

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zUKWOP3z)
CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See [the web page](https://uofa-cmput404.github.io/general/project.html) for a description of the project.
Make a distributed social network!

### Watch on YouTube
[![Watch the video](https://img.youtube.com/vi/-5R_JLsiuoI/maxresdefault.jpg)](https://www.youtube.com/watch?v=-5R_JLsiuoI)
[video also posted on youtube](https://www.youtube.com/watch?v=-5R_JLsiuoI).

# Node Links and Credentials

## Our Node
- **URL**: [Honeydew Node](https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/login/)
  - **Username**: `dndu_brianna_node`
  - **Password**: `dndu_brianna_node`

## Fully Connected Nodes
### Chartreuse
- **URL**: [Chartreuse Node](https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/)
  - **Username**: `honeydew-chartreuse`
  - **Password**: `honeychar`

### Fuchsia
- **URL**: [Fuchsia Node](https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/)
  - **Username**: `dndu_fuschia`
  - **Password**: `dndu_fuschia`

### Papayawhip
- **URL**: [Papayawhip Node](https://c404-project-7bb630f157d0.herokuapp.com/home)
  - **Username**: `honeydewteam`
  - **Password**: `honeydewteam`

### Gold
- **URL**: [Gold Node](https://gold-d9aafb476531.herokuapp.com/login)
  - **Username**: `honeydew`
  - **Password**: `123456789`

# Running Our Application Locally

## Prerequisites
- **Python 3.11** must be installed.  
  - [Download Python 3.11 here](https://www.python.org/downloads/).  
- **pip** must be installed.

---

1) Create a Virtual Enviroment:
- ```virtualenv venv --python=python3.11 ```

2) Run the Virtual Enviroment and Install Requirements
- ```source venv/bin/activate ```
- ```python3.11 -m pip install -r requirements.txt ```

3) Create Migrations and SQL database
- ```python3.11 manage.py makemigrations ```
- ```python3.11 manage.py migrate auth ```
- ```python3.11 manage.py migrate --run-syncdb ```

4) (OPTIONAL) Run Database Tests
- ```python3.11 manage.py test ```
- If you want to run a specific test suite: ```python3 manage.py test api_tests.test_inbox.HandleInboxTests```

6) Run The Server Locally
- ```python3.11 manage.py runserver 0.0.0.0:8000 ```
  



## License

* MIT License

## Copyright

The authors claiming copyright, if they wish to be known, can list their names here...

* Alex Huo - MdzzLO
* Ben Gao
* Brett Liu - Polaris Starnor
* Brianna Stals - stalsb
* Dylan Du - DylanD03
* Shiv Chopra - Shiv Chopra
