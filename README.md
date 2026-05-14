# Dairy Management System 

A modern Dairy Management System built using Django and Django REST Framework to help manage dairy farm operations efficiently.

## Features

- Farmer management
- Milk collection tracking
- Customer management
- Payment management
- Inventory management
- RESTful API
- Authentication & Authorization
- Reports and analytics


## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite / PostgreSQL
- HTML/CSS/JavaScript
- Bootstrap


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/collins05-munene/dairy-management-system.git
```

### 2. Navigate into the project folder

```bash
cd dairy-management-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the server

```bash
python manage.py runserver
```


## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/farmers/` | Manage farmers |
| `/api/milk/` | Milk records |
| `/api/customers/` | Customer records |
| `/api/payments/` | Payment records |


## Authentication

This project uses token/session authentication provided by Django REST Framework.


## Project Structure

```bash
dairy_management/
│
├── api/
├── app/
├── config/
├── users/
├── manage.py
├── requirements.txt
└── README.md
```



## Future Improvements

- Mpesa integration
- SMS notifications
- Mobile app support
- Analytics dashboard
- AI-powered milk production predictions


## Contributing

Contributions are welcome.

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request


## License

This project is licensed under the MIT License.


## Author

Developed by Collins Gitonga