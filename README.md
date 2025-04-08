# Fitness Class Booking System

A Django-based fitness class booking system with Docker containerization, CI/CD pipeline, and automated deployment.

## Features

- User authentication (registration/login)
- Database persistence with PostgreSQL
- Email notifications for bookings and reminders
- Docker containerization for easy setup and deployment
- Robust CI/CD pipeline with GitHub Actions for automated builds and testing
- Automated deployment with Ansible for streamlined server management

## Project Structure

```
.
├── .github/                                 # GitHub Actions and CI/CD configuration
│   ├── workflows/
│   │   ├── main.yml                          # Primary workflow for deployment
│   │   └── test.yml                          # Workflow for testing
├── ansible/                                  # Ansible playbooks and templates
│   ├── deploy.yml                            # Ansible playbook for deployment
│   ├── docker-compose.yml.j2                 # Docker Compose template for deployment
│   ├── inventory.yml                         # Ansible inventory
│   ├── templates/                            # Jinja2 templates used in Ansible
│   │   ├── docker-compose.yml.j2             # Docker Compose template
│   │   ├── env.j2                            # Environment variable template
│   │   ├── gunicorn.service.j2               # Gunicorn service template
│   │   └── nginx_site.j2                     # Nginx site configuration template
├── booking/                                  # Django application for bookings
│   ├── migrations/                           # Django migrations
│   ├── models.py                             # Models for booking
│   ├── views.py                              # Views for booking
│   ├── urls.py                               # URL routing for booking
│   ├── forms.py                              # Forms for booking
│   ├── admin.py                              # Admin configuration
│   ├── signals.py                            # Signals for booking app
│   ├── management/                           # Custom management commands
│   │   └── commands/                         # Management commands
│   │       └── create_user_profiles.py       # Custom command for creating user profiles
│   ├── templates/                            # HTML templates for booking pages
│   │   └── booking/                          # Booking-specific templates
│   │       ├── about.html                    # About page
│   │       ├── book_class.html               # Booking a class page
│   │       └── my_bookings.html              # View bookings page
│   ├── static/                               # Static files like images, CSS, JS
│   │   ├── css/                              # CSS files
│   │   ├── js/                               # JS files
│   │   └── Images/                           # Image files
├── fitness_booking/                          # Project settings and core files
│   ├── init.py                               # Initialization file for the project
│   ├── settings.py                           # Django settings
│   ├── urls.py                               # URL routing for the whole project
│   ├── wsgi.py                               # WSGI configuration
├── docker/                                   # Docker configurations
│   ├── django/                               # Django Dockerfile
│   │   └── Dockerfile                        # Dockerfile for the Django app
│   ├── nginx/                                # Nginx configuration for reverse proxy
│   │   └── nginx.conf                        # Nginx config file
│   ├── postgres/                             # PostgreSQL Dockerfile
│   │   └── Dockerfile                        # Dockerfile for PostgreSQL
├── manage.py                                 # Django project manager script
├── requirements.txt                          # Python dependencies
├── Dockerfile                                # Dockerfile for the whole project
├── docker-compose.yml                        # Docker Compose configuration
├── .gitignore                                # Git ignore rules
├── .env.example                              # Example environment variables
├── .flake8                                   # Linter configuration
├── coverage.xml                              # Test coverage report
├── conftest.py                               # Pytest configuration
├── pytest.ini                                # Pytest settings
├── README.md                                 # Project readme
└── run_django_tests.py                       # Script to run tests
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 13+
- Nginx
- Ansible (for deployment)
- Docker Hub account (for CI/CD)

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/paulinemutuku/DevOps_Challenge.git
   cd DevOps_Challenge
   ```

2. Create and configure `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose build
   docker-compose up
   ```

4. Access the application:

- Main application: [http://localhost:80](http://localhost:80)  
- Django admin: [http://localhost:80/admin](http://localhost:80/admin)  
- API endpoints: [http://localhost:80/api/](http://localhost:80/api/)

## CI/CD Pipeline

The project utilizes GitHub Actions for seamless continuous integration and deployment:

### Code Quality Check:

- Flake8 for linting  
- Black for code formatting  
- isort for import sorting  

### Testing:

- Django test suite  
- Integration tests  

### Docker Build and Push:

- Build Docker images  
- Push to Docker Hub  

## GitHub Actions Setup

Add Docker Hub credentials to GitHub Secrets:

- `DOCKERHUB_USERNAME`: Your Docker Hub username  
- `DOCKERHUB_TOKEN`: Your Docker Hub access token  

The workflow will automatically:

- Run code quality checks  
- Execute tests  
- Build and push Docker images to Docker Hub  
- Trigger deployment (on `main` branch)

## Deployment

The application can be deployed using Ansible for automated server configuration:

1. Configure your inventory file:
   ```bash
   cp ansible/inventory.yml.example ansible/inventory.yml
   # Edit inventory.yml with your server details
   ```

2. Set up environment variables:
   ```bash
   export DB_PASSWORD=your_database_password
   export DJANGO_SECRET_KEY=your_secret_key
   ```

3. Run the deployment:
   ```bash
   ansible-playbook -i ansible/inventory.yml ansible/deploy.yml
   ```

## Server Configuration

The application is configured to run on:

- Server IP: `64.23.210.235`  
- Nginx Port: `8080` (assigned port)  
- Django Port: `8000` (internal)  
- PostgreSQL Port: `5432` (internal)  

Access the deployed application at:

- Main application: [http://64.23.210.235:8080](http://64.23.210.235:8080)  
- Django admin: [http://64.23.210.235:8080/admin](http://64.23.210.235:8080/admin)  
- API endpoints: [http://64.23.210.235:8080/api/](http://64.23.210.235:8080/api/)

## Environment Variables

Required environment variables:

- `DJANGO_SECRET_KEY`  
- `DJANGO_DEBUG`  
- `DATABASE_URL`  
- `EMAIL_HOST`  
- `EMAIL_PORT`  
- `EMAIL_HOST_USER`  
- `EMAIL_HOST_PASSWORD`  
- `EMAIL_USE_TLS`  
- `DB_PASSWORD` (for Ansible deployment)

## Contributing

1. Fork the repository  
2. Create your feature branch  
3. Commit your changes  
4. Push to the branch  
5. Create a Pull Request  

## Author

**Pauline Mutuku**
