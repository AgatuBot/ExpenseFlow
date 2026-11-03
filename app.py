"""Flask web application for the Expense Claim AI Agent."""

import asyncio
import os

from flask import Flask, jsonify, render_template, request

from src.agent import create_expense_agent

app = Flask(__name__)


@app.route("/")
def home():
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if provider == "groq":
        model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

        if model == "openai/gpt-oss-20b":
            model_label = "GPT-OSS 20B"
        else:
            model_label = model

        settings = {
            "engine_label": "Cloud AI engine",
            "provider_label": "Powered by Groq",
            "model_label": model_label,
            "model_description": "Hosted AI model",
            "availability_label": "Cloud",
            "runtime_description": "Runs through Groq cloud service",
            "privacy_note": "ExpenseFlow uses a cloud-hosted AI model through Groq.",
            "footer_provider": "Powered by Microsoft Agent Framework & Groq",
        }
    else:
        settings = {
            "engine_label": "Local AI engine",
            "provider_label": "Powered by Ollama",
            "model_label": "Qwen 2.5",
            "model_description": "3B parameter model",
            "availability_label": "Local",
            "runtime_description": "Runs through Ollama",
            "privacy_note": "Your AI model runs locally on your computer through Ollama.",
            "footer_provider": "Powered by Microsoft Agent Framework & Ollama",
        }

    return render_template("index.html", **settings)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter an expense question."}), 400

    async def get_agent_response():
        agent, client = create_expense_agent()
        try:
            response = await agent.run(message)
            return response.text
        finally:
            await client.close()

    try:
        answer = asyncio.run(get_agent_response())
        return jsonify({"response": answer})
    except Exception:
        app.logger.exception("Expense agent request failed.")
        return jsonify({
            "error": "The AI assistant could not process your request. "
                     "Please check the AI provider configuration and try again."
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
