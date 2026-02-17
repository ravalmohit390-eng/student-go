# SmartCampus Pro

SmartCampus Pro is a full-stack web application designed to help students manage their academic life efficiently. It includes features for notes management, assignment tracking, attendance monitoring, and todo lists, all wrapped in a secure and responsive interface.

## 🚀 Features

*   **Authentication**: Secure login and signup with password hashing.
*   **Dashboard**: Overview of your academic progress with graphical analytics.
*   **Notes Manager**: Create, search, delete, and **export** notes (with optional file attachments).
*   **Assignment Tracker**: Track assignments and deadlines with visual cues for pending/completed tasks.
*   **Attendance Tracker**: Monitor subject-wise attendance with percentage calculations and progress bars.
*   **To-Do List**: Prioritize tasks with High, Medium, and Low levels.
*   **Responsive Design**: Works on desktop and mobile.
*   **Dark/Light Mode**: Toggle between themes.

## 🛠 Tech Stack

*   **Frontend**: HTML5, CSS3 (Custom Design), JavaScript (Vanilla), Chart.js
*   **Backend**: Python (Flask 3.0)
*   **Database**: SQLite (default) / SQLAlchemy ORM
*   **Libraries**: Flask-Login, Flask-WTF, ReportLab (PDF Export)

## 📦 Installation & Setup

1.  **Clone the repository** (or download usage):
    ```bash
    git clone <repository-url>
    cd SmartCampusPro
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    python run.py
    ```

5.  **Access the app**:
    Open your browser and visit `http://localhost:5000`.

## 📂 Project Structure

```
SmartCampusPro/
├── app/
│   ├── static/          # CSS, JS, Uploads
│   ├── templates/       # HTML Templates
│   ├── __init__.py      # App Factory
│   ├── auth.py          # Authentication Routes
│   ├── models.py        # Database Models
│   └── routes.py        # Main Application Routes
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── run.py               # Entry Point
└── README.md            # Documentation
```

## 📸 Usage

1.  **Register** a new account.
2.  **Login** to access your dashboard.
3.  Use the sidebar to navigate between features.
4.  **Notes**: Click "New Note" to create. Use the "Export" button to download a PDF of your note.
5.  **Attachments**: You can upload files when creating a note.

## 🤝 Contributing

This project is for educational purposes. Feel free to fork and improve!
