
# Django Gunicorn NGINX Auto Deploy

## Introduction

The script basically sets up the environment needed to deploy Django projects to Nginx server using Gunicorn

## Installation

 1. Clone the Project from github
 2. Copy the files of the project to root folder of Django project (mainly : setup.py & __setup__)
 3. Give executable permissions to two .sh scripts in __setup__ folder
 4. Run the setup.py in root folder using `python3 setup.py`
 5. Put the configuration details, the script will automatically create virtual environment and install dependencies needed for the project run. **Note : The project must have a requirements.txt file for dependency installation, also gunicorn should be added to requirements file as a prerequisite**
 6. Incase of local machine setup, do add an entry for local domain used in nginx file to /etc/hosts file and restart nginx once.
 7. Now, check your browser with the domain your django project should have been deployed.

