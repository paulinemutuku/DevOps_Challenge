# FitMe: Fitness Class Booking Platform

FitMe is a Django-powered fitness class booking system designed for streamlined user interaction, secure data handling, and modern DevOps practices. It integrates Docker containerization, CI/CD pipelines, and automated deployment for a full-stack development and delivery experience.

## Features

- Secure user registration, login, and authentication  
- PostgreSQL-based persistent data storage  
- Automated email alerts for class bookings and reminders  
- Dockerized development environment  
- End-to-end CI/CD with GitHub Actions  
- Seamless deployment with Ansible  

## Project Structure

fitme/
├── docker/
│   ├── django/
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── postgres/
│       └── Dockerfile
├── ansible/
│   ├── deploy.yml
│   ├── env.j2
│   └── docker-compose.yml.j2
├── .github/
│   └── workflows/
│       └── main.yml
├── fitness_booking/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── .env

## Requirements

- Docker & Docker Compose  
- Python 3.11 or higher  
- PostgreSQL (v13+)  
- Nginx  
- Ansible  
- Docker Hub account (for deployment pipeline)  

## Running Locally

1. Clone the repository:
   git clone https://github.com/your-username/fitme.git
   cd fitme

2. Set up your environment variables:
   cp .env.example .env
   # Then fill in your .env values

3. Build and start the services:
   docker-compose build
   docker-compose up

4. Application Access:
   - Web App: http://localhost:80  
   - Admin Portal: http://localhost:80/admin  
   - REST API: http://localhost:80/api/  

## CI/CD Workflow

FitMe uses GitHub Actions to automate the CI/CD lifecycle:

### Steps:

1. Code Quality Assurance  
   - Linting via Flake8  
   - Formatting with Black  
   - Import sorting using isort  

2. Testing  
   - Executes unit and integration tests  

3. Docker Image Handling  
   - Builds and pushes Docker images to Docker Hub  

4. Deployment Trigger  
   - Automatically deploys when changes are pushed to the main branch  

### Setup for GitHub Actions

Add the following to your GitHub repository secrets:

- DOCKERHUB_USERNAME  
- DOCKERHUB_TOKEN  

The workflow will then:
- Validate code quality  
- Run tests  
- Build/push Docker images  
- Initiate deployment  

## Deployment Instructions

Deploy using Ansible with the following steps:

1. Prepare the inventory file:
   cp ansible/inventory.ini.example ansible/inventory.ini
   # Update server details

2. Export deployment environment variables:
   export DB_PASSWORD=your_password
   export DJANGO_SECRET_KEY=your_key

3. Run the Ansible playbook:
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml

## Deployment Configuration

- Server IP: 64.23.210.235  
- Nginx (Public): Port 8080  
- Django: Port 8000  
- PostgreSQL: Port 5432  

Access Points:
- Live App: http://64.23.210.235:8080  
- Admin Panel: http://64.23.210.235:8080/admin  
- API: http://64.23.210.235:8080/api/  

## Required Environment Variables

To configure .env or deployment:

- DJANGO_SECRET_KEY  
- DJANGO_DEBUG  
- DATABASE_URL  
- EMAIL_HOST  
- EMAIL_PORT  
- EMAIL_HOST_USER  
- EMAIL_HOST_PASSWORD  
- EMAIL_USE_TLS  
- DB_PASSWORD  

## Contributing

To contribute:

1. Fork this repo  
2. Create a branch with your changes  
3. Push your updates  
4. Open a Pull Request for review  

## License

FitMe is open-source and available under the MIT License.

Developer: Pauline Mutuku
