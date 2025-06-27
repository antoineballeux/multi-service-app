# 🛠️ Multi-Service App

Full-stack web application for a small business offering various local services (repairs, maintenance, etc.). This project includes a backend built with FastAPI and a React-based frontend (to be integrated soon).

---

## 📦 Stack

- Backend: FastAPI (Python)
- Database: SQLModel (with SQLite for development)
- Authentication: Google OAuth (admin-only access)
- Frontend: React (planned)
- Deployment-ready: Modular structure for scalability

---

## 🔐 Admin Access

Only authorized Google accounts (e.g. the business owner) can access protected /admin routes and admin-only API endpoints. Authentication handled securely via OAuth2.

---

## 📁 Folder Structure

multi-service/
├── backend/         # FastAPI app (planned structure)
├── .env             # Environment variables (not committed)
├── main.py          # FastAPI entry point
├── models/          # SQLModel data models
├── routes/          # Public + admin API endpoints
├── auth/            # Google OAuth & admin validation
├── crud/            # Database access logic
└── README.md

---

## 🚧 Current Features

- ✅ Project initialized and pushed to GitHub
- ✅ GitHub repo cleaned and configured with proper .gitignore
- ✅ Google OAuth authentication implemented
- ✅ Admin-only route secured
- ✅ Service listing endpoint created
- 🔜 Frontend integration with React
- 🔜 Admin dashboard UI

---

## 🔒 .env File Format (example)

GOOGLE_CLIENT_ID=your-google-client-id  
GOOGLE_CLIENT_SECRET=your-client-secret  
ADMIN_EMAIL=youremail@example.com  
SECRET_KEY=your-secret

> Do not commit your .env file — use a .env.example version for sharing.

---

## ⚙️ Installation & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the development server:
   ```bash
   uvicorn backend.main:app
   ```

---

## 💡 To Do

- [ ] Set up React frontend
- [ ] Deploy to production (e.g. Vercel + Railway)
- [ ] Add unit tests
- [ ] Add contact form or service request form
- [ ] Frontend styling and dashboard layout

---

## 🧠 About the Project

This project is for a real small business and is intended to be scalable and clean enough for future growth. Built with professional structure and real-world deployment in mind.

---

## 👤 Author

Antoine Balleux  
antoineballeux015@gmail.com  
GitHub: https://github.com/antoineballeux
