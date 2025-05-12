# CRM Invoice Manager

Django-based system for managing clients, vehicles, contracts, and automated invoicing.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser  # Crea un usuario administrador para iniciar sesión
```

Se debe crear un superusuario para acceder al sistema por primera vez.