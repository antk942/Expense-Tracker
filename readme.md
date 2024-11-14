# Expense Tracking App

![Version](https://img.shields.io/badge/version-1.0-blue)

## Overview
This app focuses on tracking expenses and balances between users, offering detailed views of expenses, notifications, and balance tracking.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Automated Scripts](#automated-scripts)
- [Docker Setup](#docker-setup)
- [Installation](#installation)
- [Future Improvements](#future-improvements)

## Features
- **Expenses, Categories, and Notifications:**
  - Create, view, edit, and delete expenses, categories, and notifications.
- **Categories:**
  - View all expenses per year and per month.
  - Options for generating reports and analytics.
- **Notifications:**
  - Send users reminders about upcoming expenses via email.
- **Detailed Expenses:**
  - Track who paid, for whom, the amount, date, and currency used.
- **Balance Overview:**
  - View user balances (who owes who and how much).
  - Option to send notifications and mark balances as resolved.
- **Logging:**
  - Extensive logging with a 30-day rotation to manage disk usage.

> **Note:** Balance notifications include a cooldown period to prevent excessive alerts.

## Automated Scripts

### `tasks.py`
- [x] **Backup**: Automatically backs up the database weekly with folder configuration options.
- [x] **Notifications**: Automatically sends notifications via email based on due dates.

### `restartCronjob.py`
- [x] Manage all cron jobs configured in `settings.py`. Removes, adds, and lists all active cron jobs.

### `start.py`
- [x] Automatically runs `collectstatic` and `migrate` commands required to start the server.

### `deploy.sh`
- [x] Establishes a secure shell between the user and the server.
- [x] Pulls the latest changes from GitHub and rebuilds the Docker container.

## Docker Setup

### `Dockerfile`
- Creates a Docker container with the app and runs necessary automation scripts.

### `docker-compose.yml`
- Runs the Docker container while mounting the database and logging folders.

## Installation

To set up the app locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/antk942/Expense-Tracker.git

# Navigate to the project directory
cd ExpenseTracker

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
