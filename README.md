# ExpenseFlow — AI Expense Claim Agent

## Project Overview

ExpenseFlow is a purpose-built AI expense claim assistant developed with Python, Flask and Microsoft Agent Framework.

The application allows users to submit expense claims through a conversational interface. The AI agent uses a custom Python validation tool to compare claimed amounts against predefined expense policy limits and explain the results.

The project demonstrates how to build, test and deploy an AI-powered application without requiring a paid Microsoft Azure subscription.

## Project Objectives

This project explores how to:

- Set up a Python development environment.
- Run a local language model using Ollama.
- Work with Microsoft Agent Framework.
- Build an AI agent using Python.
- Create custom Python tools that an agent can call.
- Connect an agent to local and hosted AI model providers.
- Build a web interface using Flask.
- Validate expense claims against configurable policy limits.
- Test and troubleshoot an AI application.
- Deploy an application using Render.
- Document and publish a software project using GitHub.

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.13 | Main programming language |
| Microsoft Agent Framework | AI agent development |
| Ollama | Local AI model runtime |
| Qwen2.5 3B | Local language model |
| Groq | Hosted AI model provider |
| Gemini | Hosted AI model provider |
| Flask | Web application framework |
| HTML, CSS and JavaScript | Frontend interface |
| Git and GitHub | Version control and project documentation |
| Render | Application hosting |

## Key Features

- Conversational expense claim assistant.
- Custom Python expense-policy validation tool.
- Expense category validation.
- Clear explanations of policy limits and claim differences.
- Support for local and hosted AI model providers.
- Responsive web interface.
- Human-review safeguards: the agent does not automatically approve or pay claims.

## Simulated Expense Policy

The application currently uses the following educational policy limits:

| Expense Category | Policy Limit |
|---|---:|
| Transport | ₦50,000 |
| Meals | ₦30,000 |
| Accommodation | ₦150,000 |
| Other | ₦25,000 |

The validation tool identifies whether a claim is within or above its configured limit.

A result within policy does not guarantee approval or reimbursement. Claims exceeding a configured limit may require human review.

These limits are simulated examples, not the official policy of an actual organisation.

## AI Model Providers

ExpenseFlow supports three provider configurations:

- **Ollama:** Local model execution using Qwen2.5 3B.
- **Groq:** Hosted model access using the Groq API.
- **Gemini:** Hosted model access using the Gemini API.

The provider is selected through the local environment configuration. API credentials must be stored securely and must never be committed to GitHub.

## Running the Project Locally

### 1. Clone the repository

```powershell
git clone https://github.com/AgatuBot/ExpenseFlow.git
cd ExpenseFlow
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure your AI provider

Create a local `.env` file in the project directory.

For local Ollama use:

```env
AI_PROVIDER=ollama
```

For Groq use:

```env
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
```

For Gemini use:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
```

Use your own API credentials. Do not publish them or include them in source control.

For Ollama, install Ollama and download the local model:

```powershell
ollama pull qwen2.5:3b
```

### 6. Start the application

```powershell
python app.py
```

Open the application in your browser:

`http://127.0.0.1:5000/`

## Live Application

The deployed application is hosted on Render:

https://expenseflow-4jsn.onrender.com/

Hosting availability and free-tier limitations may affect response times.

## Project Structure

```text
Azure-AI-Agents-Journey/
├── app.py
├── src/
│   ├── agent.py
│   └── policy_tools.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── agatubot-logo.jpg
├── requirements.txt
├── Procfile
├── .python-version
├── .gitignore
├── README.md
└── LEARNING-JOURNAL.md
```

## Learning Journey

This project is part of my practical journey towards becoming an AI Agentic Developer.

The goal is to understand more than how to run an AI model. It is to learn how agents interact with tools, how application logic is designed, how AI responses are controlled, and how an application is tested and deployed.

The learning journal records the development process, technical decisions, challenges, solutions and lessons learned.

## Current Project Status

- [x] Create project directory and Python virtual environment.
- [x] Install and configure Ollama.
- [x] Download and test Qwen2.5 3B.
- [x] Integrate Microsoft Agent Framework.
- [x] Build the expense claim AI agent.
- [x] Implement custom Python policy validation.
- [x] Integrate local and hosted AI providers.
- [x] Build the Flask web interface.
- [x] Test within-policy and over-limit claims.
- [x] Implement safeguards against unsupported approval and payment claims.
- [x] Deploy the application to Render.
- [x] Publish the project to GitHub.
- [ ] Complete the learning journal.
- [ ] Prepare a beginner-friendly project tutorial.
- [ ] Produce a YouTube demonstration.

## Author and Project Branding

**Developer:** Daniel Samson
**GitHub:** [AgatuBot](https://github.com/AgatuBot)
**Project:** ExpenseFlow

ExpenseFlow is developed as a practical learning project focused on Python, AI agents, tool integration and application deployment.

## Disclaimer

ExpenseFlow is an educational demonstration. Its expense limits and validation rules are simulated.

The application does not make official financial decisions, approve claims or initiate payments. Actual expense claims require the appropriate organisational review and approval processes.

---

**Project Status:** Functional prototype — deployed on Render.
