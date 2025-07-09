# 🪞LookingGlass

A minimalist daily log tracker API - reflect on what you did today.  
Built with Python, FastAPI, and MySQL.

---

## Development Environment

### LookingGlassAPI
- **Language** - Python 3.11+
- **Framework** - FastAPI (via Connexion)
- **Spec Format** - OpenAPI 3.0
- **Database** - MySQL 8
- **ORM** - SQLAlchemy Core
- **Environment** - dotenv

---

## API Directory & File Structure

```
LookingGlass/                       # Root project directory
│   __main__.py                     # Application entry point
│   .env                            # Environment variables for DB
└───app/
    ├───database/
    │   └── db.py                   # SQLAlchemy session & engine setup
    ├───openapi_server/
    │   ├── controllers/            # Route logic (CRUD operations)
    │   ├── models/                 # OpenAPI models
    │   └── openapi/openapi.yaml    # API schema (OpenAPI 3.0)
    └─────────────────────
```

---

## How to Run

### Requirements

- [Git](https://git-scm.com/downloads)
- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL 8](https://dev.mysql.com/downloads/)

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/johnshields/LookingGlass
cd LookingGlass

# Create virtual environment
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up MySQL

Ensure you have a `.env` file in the project root with the following:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=lookingglass_db
```

Create the database manually with SQL [script](sql/looking_glass_db.sql).

---

### 3. Run the API

```bash
python main.py
```

- API Base URL: `http://localhost:8080`
- Swagger UI: `http://localhost:8080/ui`
- Health check: `GET /` or `GET /api/`

---

