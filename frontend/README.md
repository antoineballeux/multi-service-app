# React Frontend

This is a lightweight React + Tailwind CSS frontend that interacts with the FastAPI backend.

The app uses CDN links for React, Babel and Tailwind so no build step or Node.js installation is required. You can serve the files with any static HTTP server.

## Running

1. Start the FastAPI backend (see project README for instructions).
2. In another terminal, serve the `frontend/` directory. For example using Python:
   ```bash
   python -m http.server --directory frontend 8000
   ```
3. Open `http://localhost:8000` in your browser.

The frontend will call the backend at the same host (adjust URLs if hosting separately).
