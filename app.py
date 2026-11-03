"""Flask web application for the Expense Claim AI Agent."""

import asyncio

from flask import Flask, jsonify, render_template, request

from src.agent import create_expense_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


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

