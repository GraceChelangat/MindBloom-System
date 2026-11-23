# 🌸 MindBloom System

A web-based system for tracking mood and eating behaviours, and flagging relapse risk in anorexia nervosa among teenagers and young adults.

> **Disclaimer:** MindBloom is a support and monitoring tool, not a medical device. Its predictions are not a diagnosis and do not replace advice from a qualified healthcare professional. If you or someone you know is struggling, please contact a doctor, therapist, or local emergency services.

---

## 📖 Overview

Anorexia nervosa has a high risk of relapse, and early warning signs often show up in day-to-day mood and eating patterns before they become a crisis. MindBloom helps users record those patterns over time and uses them to estimate relapse risk, so that patients, caregivers, and clinicians can step in earlier.

## ✨ Features

- **Mood tracking:** log daily mood entries and view trends over time
- **Eating behaviour tracking:** record meals and eating-related behaviours
- **Relapse risk prediction:** estimate relapse risk from the logged data
- <!-- TODO: add other features, e.g. user roles, dashboards, reports, reminders -->

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Django |
| Database | SQLite |
| Frontend | Django templates, HTML, CSS |

## 📁 Project Structure

```
MindBloom-System/
├── config/          # Django project settings and root URL configuration
├── core/            # Main application (models, views, logic)
├── templates/       # HTML templates
├── static/css/      # Stylesheets
├── manage.py        # Django management script
├── db.sqlite3       # SQLite database
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer
- pip
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/GraceChelangat/MindBloom-System.git
   cd MindBloom-System
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If there is no `requirements.txt` yet, install Django directly (`pip install django`) and add any other packages the project uses.

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create an admin user**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/> in your browser.

## 🧭 Usage

1. Sign up or log in.
2. Log your mood and eating behaviours regularly.
3. Review your history and trends.
4. Check your relapse risk indicator and share it with your care team if appropriate.

<!-- TODO: add screenshots, e.g. ![Dashboard](docs/dashboard.png) -->

## 🔒 Privacy & Data

MindBloom handles sensitive health information. If you deploy it:

- Do not commit real patient data or `db.sqlite3` to a public repository
- Set `DEBUG = False` and keep `SECRET_KEY` out of version control
- Use HTTPS and a production-grade database

## 🗺️ Roadmap

- [ ] Improve the relapse prediction model
- [ ] Caregiver / clinician view
- [ ] Reminders and notifications
- [ ] Export reports

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a pull request

## 📄 License

<!-- TODO: choose a license (e.g. MIT) and add a LICENSE file -->
This project is currently unlicensed. Add a `LICENSE` file to specify the terms.

## 👩‍💻 Author

**Grace Chelangat**
GitHub: [@GraceChelangat](https://github.com/GraceChelangat)