# 🎥 **SINEHAN**

*A simple and intuitive cinema ticketing system for steamlined movie-watching.*

[![Contributors](https://img.shields.io/badge/Contributors-3-34D399?style=for-the-badge)](https://github.com/elib00/sinehan/graphs/contributors)  [![Forks](https://img.shields.io/badge/Forks-0-3182CE?style=for-the-badge)](https://github.com/elib00/sinehan/network)  [![Stars](https://img.shields.io/badge/Stars-2-FBBF24?style=for-the-badge)](https://github.com/elib00/sinehan/stargazers)  [![Issues](https://img.shields.io/badge/Issues-0-9CA3AF?style=for-the-badge)](https://github.com/elib00/sinehan/issues)  [![License](https://img.shields.io/badge/License-Not%20Specified-DC2626?style=for-the-badge)](https://opensource.org/licenses)

## Table of Contents  

<details>  
  <summary></summary>  

- [Overview](#-overview)  
- [Functional Requirements](#-functional-requirements)  
- [Resources](#-resources)  
  - [Gantt Chart](#-gantt-chart)  
  - [ERD](#-erd)  
  - [UI/UX Design](#-uiux-design)  
- [Tech Stack](#-tech-stack)  
- [Getting Started](#-getting-started)  
  - [Prerequisites](#-prerequisites)  
  - [Installation](#-installation)  
- [Contributors](#-contributors)  
- [Contact](#-contact)  

</details>

---

## ✨ **Overview**  
Sinehan is a modern cinema ticketing system crafted to deliver seamless ticket purchasing and management.  

🎬 **Effortless Browsing**: Users can explore an updated catalog of films with details such as showtimes, genres, and ratings, ensuring informed decisions.

🎟 **Quick & Secure Ticketing**: Streamlined ticket purchasing allows seat selection and payment completion without the hassle of mandatory account creation, maintaining user convenience.

🍿 **Admin Efficiency**: Administrators gain access to robust tools for managing essential operations, including adding/editing movie schedules, monitoring user activity, and tracking bookings.  

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 🚀 **Functional Requirements**  
1. **User Management**  
   Manage user authentication, registration, and settings.

2. **Booking Management**  
   Book tickets, select films and showtimes, and confirm seats.

3. **Movie Management**  
   Admins can manage movie information.

4. **Payment Processing**  
   Integrate secure payments for transactions.

5. **Seat Selection**  
   Users can choose seats during ticket booking.

6. **Admin Tools**  
   Oversee bookings, manage users, and generate reports.

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 📂 **Resources**  

### **Gantt Chart**  
![Gantt Chart](resources/gantt-chart.png)

### **ERD**  
![ERD](static/images/erdfinal.png)

### **UI/UX Design**  
<div style="display: flex; gap: 10px;">

<img src="static/images/figma1.png" alt="Figma Design 1" width="200"/>
<img src="static/images/figma2.png" alt="Figma Design 2" width="200"/>
<img src="static/images/figma3.png" alt="Figma Design 3" width="200"/>

</div>


<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 🛠️ **Tech Stack**  

- [![Django](https://img.shields.io/badge/Django-5.1.1-006400?logo=django&logoColor=white&style=for-the-badge)](https://www.djangoproject.com/)
- [![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white&style=for-the-badge)](https://www.sqlite.org/)
- [![Python](https://img.shields.io/badge/Python-3.12.5-FF6347?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
- [![HTML5](https://img.shields.io/badge/HTML5-5-F4A300?logo=html5&logoColor=white&style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [![CSS3](https://img.shields.io/badge/CSS3-3-1E90FF?logo=css3&logoColor=white&style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [![JavaScript](https://img.shields.io/badge/JavaScript-ES6-FFD700?logo=javascript&logoColor=black&style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4.13-8A2BE2?logo=tailwind-css&logoColor=white&style=for-the-badge)](https://tailwindcss.com/)

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 🍿 **Getting Started**  

### 📦 **Prerequisites**  

Before you start, ensure you have the following installed:

- [![Python](https://img.shields.io/badge/Python-3.12.5-306998?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

### 🛠️ **Installation**  

1. **Clone the repository**  
   Open your terminal and run the following command:
   ```bash
   git clone https://github.com/elib00/sinehan.git
   cd sinehan
   ```

2. **Create a virtual environment**  
   It’s recommended to create a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies**  
   Install all the required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**  
   Run the database migrations to set up the database schema:
   ```bash
   python manage.py make migrations
   python manage.py migrate
   ```

5. **Start the development server**  
   Now, you can start the development server and view the project locally:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**  
   Open your browser and go to `http://127.0.0.1:8000/` to see the application running locally.

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 👨‍💻 **Contributors**  
**Our Amazing Contributors! ✨**

<div align="center">

| <img src="https://avatars.githubusercontent.com/u/119659329?v=4" width="100" style="border-radius:50%;" alt="Joshua Napiñas"> | <img src="https://avatars.githubusercontent.com/u/151008985?v=4" width="100" style="border-radius:50%;" alt="Summer Ishi Rodrigo"> | <img src="https://avatars.githubusercontent.com/u/134621548?v=4" width="100" style="border-radius:50%;" alt="Zhazted Rhixin Valles"> |
|---|---|---|
| **Joshua Napiñas** | **Summer Ishi Rodrigo** | **Zhazted Rhixin Valles** |

</div>

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>

---

## 📬 **Contact**  

For inquiries, feel free to contact us:

- 📧 **Email**: [joshuanapinas@gmail.com](joshuanapinas@gmail.com)  
- 📌 **GitHub**: [elib00](https://github.com/elib00)  

- 📧 **Email**: [summerrodrigo07@gmail.com](summerrodrigo07@gmail.com)  
- 📌 **GitHub**: [SummerIshi](https://github.com/SummerIshi)  

- 📧 **Email**: [vallestedted@gmail.com](vallestedted@gmail.com)  
- 📌 **GitHub**: [Rhixin](https://github.com/Rhixin)

<div align="right"><a href="#-sinehan">🔝 Back to Top</a></div>
