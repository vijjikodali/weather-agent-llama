# 🌦️ Weather AI Agent

<p align="center">

**AI-powered Weather Assistant built with Streamlit, Groq Llama, OpenWeather API, Databricks SQL, Playwright & GitHub Actions**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Playwright](https://img.shields.io/badge/Playwright-E2E-green)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-blue)

</p>

---

## 🚀 Overview

Weather AI Agent is an interactive web application that combines **live weather data** with **AI-generated responses**. It demonstrates API integration, conversational AI, cloud database logging, automated UI testing, and CI/CD workflows.

---

## 🏗️ Solution Architecture

```text
                    👤 User
                       │
                       ▼
            🌐 Streamlit Web Application
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
🌦️ OpenWeather     🤖 Groq AI      🗄️ Databricks
   Live API        Intent Router      SQL Logs
      └────────────────┼────────────────┘
                       ▼
              💬 AI Weather Response
                       │
                       ▼
          🧪 Playwright E2E Automation
                       │
                       ▼
           ⚙️ GitHub Actions CI/CD
```

---

## ✨ Features

| ✅   | Feature                      |
| --- | ---------------------------- |
| 🌦️ | Live Weather Retrieval       |
| 🤖  | AI-powered Weather Responses |
| 💬  | General AI Chat              |
| 🎯  | Intent-based Request Routing |
| 🗄️ | Databricks SQL Logging       |
| 🔍  | System Health Check          |
| 🧪  | Playwright End-to-End Tests  |
| ⚙️  | GitHub Actions CI/CD         |

---

## 🛠️ Tech Stack

| Layer        | Technology              |
| ------------ | ----------------------- |
| 🐍 Language  | Python 3.11             |
| 🎨 UI        | Streamlit               |
| 🤖 AI        | Groq Llama 3.1          |
| 🌦️ Weather  | OpenWeather API         |
| 🗄️ Database | Databricks SQL          |
| 🧪 Testing   | Playwright + TypeScript |
| ⚙️ CI/CD     | GitHub Actions          |

---

## 📂 Project Structure

```text
weather-agent-llama/
│
├── .github/
│   └── workflows/
│
├── .streamlit/
│
├── tests/
│   └── e2e/
│
├── app.py
├── database.py
├── playwright.config.ts
├── requirements.txt
├── package.json
├── README.md
└── .gitignore
```

---

## ▶️ Quick Start

```bash
git clone https://github.com/vijjikodali/weather-agent-llama.git

cd weather-agent-llama

pip install -r requirements.txt

npm install

npx playwright install

streamlit run app.py
```

### Run Playwright Tests

```bash
npx playwright test
```

---

## 🧪 Testing

✔️ Smoke Tests

✔️ End-to-End UI Automation

✔️ HTML Reports

✔️ Screenshots on Failure

✔️ Video Recording on Failure

---

## ⚙️ Continuous Integration

GitHub Actions automatically:

* ✅ Install dependencies
* ✅ Launch the Streamlit application
* ✅ Execute Playwright tests
* ✅ Upload HTML reports
* ✅ Upload application logs

---

## 📸 Application Preview

> Add screenshots here after deployment.

```
Home Screen
```

```
Weather Response
```

```
System Check
```

---

## 🔮 Next Steps

* Expand Playwright regression suite
* Add pytest API tests
* Add database validation tests
* Add unit test coverage

---

## 👩‍💻 Author

**Kodali Vijayalaxmi**

🔗 GitHub: https://github.com/vijjikodali

💼 LinkedIn: https://www.linkedin.com/in/kodali-vijayalaxmi-40860222

---

⭐ If you found this project helpful, consider giving it a star.
