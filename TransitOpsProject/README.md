# TransitOps ERP - Enterprise Fleet & Logistics Management Portal

TransitOps is a next-generation, professional-grade Enterprise Resource Planning (ERP) platform designed for logistics operations, fleet tracking, and transport compliance. It enables real-time tracking of assets, drivers, dispatches, maintenance operations, and finances in a secure, role-restricted environment.

---

## 🚀 Key Modules & Features

### 1. Unified Dashboard
* **Dynamic KPIs**: Real-time metrics including active/available fleet count, maintenance status, active dispatches, and total monthly OpEx.
* **Interactive Data Visualizations**: Custom Chart.js charts showing fleet utilization trends and asset status distributions.
* **Responsive Layout**: Fluid design adapts to mobile, tablet, and desktop monitors.

### 2. Vehicle Registry
* **Asset Tracking**: Complete lifecycle records including registration plate numbers, odometer status, load capacities, and acquisition costs.
* **View Modes**: Switch dynamically between clean Table List and detailed Card Grid views.
* **Automated Lifecycles**: Automatic status changes (Available, On Trip, In Shop, Retired) driven by trip manifests and maintenance tickets.

### 3. Driver Dossier
* **Identity Profiles**: Comprehensive licensing details (HMV/LMV categories, expiry dates), contact records, and current duty status.
* **Safety Scoring**: Performance logging mapping driver safety indices.

### 4. Trip Manifest (Logistics Dispatcher)
* **Smart Dispatcher**: Interactive trip scheduler matching cargo weight requirements to available vehicle capacity.
* **Live Opex Calculator**: Automatically estimates logistics costs (fuel costs, toll fees) based on trip distance in real time before dispatching.
* **Driver Self-Assignment Rule**: Drivers are locked to dispatching and managing only their own trips.

### 5. Safety & Compliance Desk
* **Active License Surveillance**: Automatically flags driver licenses expiring within 30 days.
* **Automated License Alerts**: Triggers renewal alert emails directly to drivers with a single click.
* **Compliance Checks**: Non-admin panels are fully restricted from accessing raw driver dossiers or switching roles.

### 6. Maintenance Workshop
* **Service Tickets**: Tracks routine maintenance, repair actions, and compliance tasks.
* **Auto Shop Transitions**: Creating a maintenance ticket automatically sends the vehicle to "In Shop" status; signing off on repair releases it back to "Available".

### 7. Fuel & Expenses Ledger
* **Fuel Efficiency Calculator**: Computes fuel consumption (L/100km) and logs fill-ups.
* **OpEx Category Matrix**: Tracks costs across Fuel, Maintenance, Tolls, Parts, Insurance, and Other, complete with cost distribution percentages.

### 8. Analytics & Professional Reporting
* **Archive Downloads**: Triggers actual dynamic browser file downloads for CSV, XLSX, and PDF exports.
* **Printable Executive Summary**: Dedicated `@media print` layout that strips dashboard web chrome to render a clean, high-quality white-background report for PDF printing.

---

## 🔒 Security & Role-Based Access Control (RBAC)

The system enforces strict role-based access control via custom Django decorators:
* **Admin**: Complete access to all panels, Global Operations Config, the RBAC Matrix, and the navbar Sandbox Role Switcher.
* **Fleet Manager**: Manages vehicles, trips, and maintenance tickets; restricted from system settings and admin role switcher.
* **Financial Analyst**: Manages expensing, fuel records, and analytics reports; restricted from operational dispatches and settings.
* **Driver**: Has access only to their assigned Trip Manifest workspace; restricted from all management panels.
* **Safety Officer**: Has access only to the Safety & Compliance Desk.

---

## 🛠️ Technology Stack

* **Backend**: Django 5.2 (Python)
* **Frontend**: HTML5, Vanilla CSS, TailwindCSS, Chart.js
* **Database**: SQLite3
* **Environment Configuration**: `.env` variables for sensitive settings (Secret key, SMTP credentials)

---

## 💻 Local Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Configure Environment Variables
Create a `.env` file in the `TransitOpsProject` directory:
```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Initialize Database & Seed Users
Run the seeder script to automatically create database tables, run migrations, and seed all five core roles with initial test credentials:
```powershell
python seed_db.py
```

### Seeded Credentials:
* **Admin**: `Parth` / Password: `Parth@123`
* **Driver**: `parthgoyal2809@gmail.com` / Password: `Parth@123`
* **Safety Officer**: `chronix2809@gmail.com` / Password: `Parth@123`
* **Fleet Manager**: `parth28@gmail.com` / Password: `Parth@123`
* **Financial Analyst**: `parth0928@gmail.com` / Password: `Parth@123`

### 4. Start Development Server
```powershell
python manage.py runserver
```
Visit the application in your browser at `http://127.0.0.1:8000/`.

---

## 🧪 Testing
Run the automated test suite to verify the authentication flow, role restriction guards, trip dispatch status lifecycles, and pagination thresholds:
```powershell
# Run main workflow tests
python C:\Users\ASUS\.gemini\antigravity\brain\ea8d0f19-d626-4ca7-b72b-86febb28746a\scratch\test_modules_flow.py

# Run pagination threshold tests
python C:\Users\ASUS\.gemini\antigravity\brain\ea8d0f19-d626-4ca7-b72b-86febb28746a\scratch\test_pagination.py
```
