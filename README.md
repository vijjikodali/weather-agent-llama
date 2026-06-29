# 🌦️ Weather AI Agent

> **AI-powered Weather Agent built with Streamlit, OpenWeather API, Groq Llama, and Databricks SQL, featuring Playwright end-to-end testing and GitHub Actions CI/CD.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Playwright](https://img.shields.io/badge/Playwright-E2E-green)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-blue)

---

## 📌 Overview

Weather AI Agent is an interactive web application that combines live weather information with AI-generated responses. Users can ask weather-related questions or general queries through a conversational interface powered by Groq Llama. The application integrates cloud services for weather retrieval, AI processing, and database logging while demonstrating automated testing and CI/CD practices.

---

## 🏗️ Architecture

```text
                           User
                             │
                             ▼
                  Streamlit Web Application
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 OpenWeather API       Groq Llama 3.1      Databricks SQL
 (Live Weather)      (Intent & AI Chat)   (Weather Logging)
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                     AI Weather Response
                             │
                             ▼
                Playwright End-to-End Tests
                             │
                             ▼
                 GitHub Actions CI Pipeline
```

---

## ✨ Features

### 🌦️ Application

* Live weather information
* AI-powered weather recommendations
* General AI chat assistant
* Intent-based request routing
* Weather interaction logging
* Built-in system health check

### 🔗 Integrations

* OpenWeather API
* Groq Llama 3.1
* Databricks SQL Warehouse

### 🧪 Test Automation

* Playwright End-to-End Tests
* Smoke Test Suite
* HTML Test Reports
* Automatic Screenshots on Failure
* Video Recording on Failure

### ⚙️ CI/CD

* GitHub Actions Workflow
* Automated Playwright Execution
* Environment-based Configuration
* Test Report & Log Artifacts

---

## 🛠️ Technology Stack

| Category        | Technology      |
| --------------- | --------------- |
| Language        | Python 3.11     |
| UI              | Streamlit       |
| AI              | Groq Llama 3.1  |
| Weather API     | OpenWeather API |
| Database        | Databricks SQL  |
| Test Automation | Playwright      |
| Test Language   | TypeScript      |
| CI/CD           | GitHub Actions  |
| Version Control | Git & GitHub    |

---

## 📂 Project Structure

```text
weather-agent-llama/
│
├── .github/
│   └── workflows/
│       └── playwright.yml
│
├── .streamlit/
│   └── secrets.toml
│
├── tests/
│   └── e2e/
│       ├── weather.spec.ts
│       └── ai-validation.spec.ts
│
├── app.py
├── playwright.config.ts
├── package.json
├── package-lock.json
├── requirements.txt
├── tsconfig.json
├── README.md
└── .gitignore
```

---

## ✅ Current Test Coverage

### Playwright End-to-End Tests

* Application launches successfully
* Weather AI interface validation
* Smoke test execution
* HTML report generation
* Screenshot capture on failures
* Video capture on failures

---

## 🚀 CI/CD Pipeline

The GitHub Actions workflow automatically:

* Checks out the repository
* Sets up Python and Node.js
* Installs project dependencies
* Installs Playwright browsers
* Starts the Streamlit application
* Executes Playwright tests
* Uploads HTML reports
* Uploads application logs

---

## ⚡ Local Setup

### Clone Repository

```bash
git clone https://github.com/vijjikodali/weather-agent-llama.git
cd weather-agent-llama
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Node Dependencies

```bash
npm install
```

### Install Playwright Browsers

```bash
npx playwright install
```

### Run the Application

```bash
streamlit run app.py
```

### Execute Playwright Tests

```bash
npx playwright test
```

---

## 📈 Roadmap

* Expand Playwright end-to-end scenarios
* Add API automation using pytest
* Add Databricks database validation tests
* Add Python unit tests
* Improve UI responsiveness
* Increase automation coverage

---

## 👩‍💻 Author

**Kodali Vijayalaxmi**

* GitHub: https://github.com/vijjikodali
* LinkedIn: https://www.linkedin.com/in/kodali-vijayalaxmi-40860222

---

## 📄 License

This project is intended for learning, demonstration, and portfolio purposes.

---

⭐ If you found this project useful, consider giving it a star.
