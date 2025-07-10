# 🪞LookingGlass

A minimalist daily log tracker – reflect on what you did today.  
Built with **Python + FastAPI** on the backend and a **React + TypeScript** frontend.

![image](https://github.com/user-attachments/assets/8c754399-f721-41bd-bfd2-e77527a7c465)

---

## 🔧 Tech Stack

### Backend – LookingGlassAPI
- **Language:** Python 3.11+
- **Framework:** FastAPI (via Connexion)
- **Spec Format:** OpenAPI 3.0
- **Database:** MySQL 8
- **ORM:** SQLAlchemy Core
- **Environment:** dotenv

### Frontend – React App
- **Language:** TypeScript
- **Framework:** React (Vite)
- **Styling:** TailwindCSS

---

## 📁 API Directory & File Structure

```
LookingGlass/                       # Root project directory
│   main.py                         # API entry point
│   .env                            # MySQL credentials
├───backend/
│   ├───database/
│   │   └── db.py                   # SQLAlchemy engine + session
│   ├───openapi_server/
│   │   ├── controllers/            # CRUD logic
│   │   ├── models/                 # Data models
│   │   └── openapi/openapi.yaml   # OpenAPI schema
└───frontend/                      # Frontend source (Vite + React)
    ├── public/
    ├── src/
    │   ├── types.ts                # Shared types
    │   └── App.tsx                 # Main app
    └───────────────── 
```

---

## 🚀 How to Run the Project

### 1. Clone & Set Up Backend

```bash
git clone https://github.com/johnshields/LookingGlass
cd LookingGlass

# Create virtual environment
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows

# Install backend dependencies
pip install -r requirements.txt
```

### 2. Set Up MySQL

Ensure your `.env` file in the root contains:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=lookingglass_db
```

Then create the database manually using the provided SQL script:

```bash
mysql -u root -p < sql/lookingglass_db.sql
```

---

### 3. Run LookingGlass App

Run it from PowerShell/Command Prompt:

```bash
.\start.bat
```

- **Base URL:** `http://localhost:8080`
- **Docs:** `http://localhost:8080/ui`
- **Health Check:** `GET /api/`
- Frontend will be available at **http://localhost:5174**

---

MIT License © 2025 John Shields
