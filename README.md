# 🪞LookingGlass

A minimalist daily log tracker - reflect on what you did today.  
Built with **Python + FastAPI**, **MySQL** and **React + TypeScript**.

![image](https://github.com/user-attachments/assets/8c754399-f721-41bd-bfd2-e77527a7c465)

---

## 🧰 Development Environment

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (via Connexion)
- **Spec Format:** OpenAPI 3.0
- **Database:** MySQL 8
- **ORM:** SQLAlchemy Core

### Frontend
- **Language:** TypeScript
- **Framework:** React (Vite)
- **Styling:** TailwindCSS

---

## 📁 Directory Structure

```
LookingGlass/
├── .env
├── main.py
├── backend/
│   ├── database/
│   │   └── db.py
│   ├── openapi_server/
│   │   ├── controllers/
│   │   ├── models/
│   │   └── openapi/
│   │       └── openapi.yaml
├── frontend/
│   ├── public/
│   └── src/
│       ├── types.ts
│       └── App.tsx
└─────────────────────────────
```

---

## 🚀 How to Run

### Requirements

- [Git](https://git-scm.com/downloads)
- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/)
- [Node.js](https://nodejs.org/) (for frontend)

---

### ⚙️ Backend Setup

1. Clone the repo:

```bash
git clone https://github.com/johnshields/LookingGlass.git
cd LookingGlass
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=lookingglass_db
```

5. Create database:

```bash
mysql -u root -p < sql/lookingglass_db.sql
```

---

### ▶️ Start the App

From PowerShell or Command Prompt:

```bash
.\start.bat
```

- **Backend**: `http://localhost:8080`
- **Docs**: `http://localhost:8080/ui`
- **Health Check**: `GET /api/`
- **Frontend**: `http://localhost:5174`

---

MIT License © 2025 John Shields
