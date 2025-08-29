# 🪞LookingGlass

A minimalist daily log tracker - reflect on what you did today.  
Built with **Python + Flask**, **MySQL** and **React + TypeScript**.

![image](https://github.com/user-attachments/assets/8c754399-f721-41bd-bfd2-e77527a7c465)

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

# Run service

### Requirements

- [Git](https://git-scm.com/downloads)
- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/)
- [Node.js](https://nodejs.org/) (for frontend)

---

### ⚙️ Backend Setup

1. Init App:

```bash
git clone https://github.com/johnshields/looking-glass.git
cd looking-glass
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:

```dotenv
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=lookingglass_db
```

3. Create database:

```bash
mysql -u root -p < sql/lookingglass_db.sql
```

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
