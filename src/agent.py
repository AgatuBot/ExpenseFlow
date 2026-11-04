"""Expense Claim AI Agent supporting local Ollama and hosted Gemini."""

import asyncio
import json
import os
from types import SimpleNamespace
from dotenv import load_dotenv

from src.policy_tools import check_expense_claim

load_dotenv()

INSTRUCTIONS = """
You are ExpenseFlow, a professional Expense Claim AI Assistant.

Help employees understand company expense policies.
Use the expense policy tool whenever a claim needs validation.
Never invent policy limits or validation results.
Explain the claimed amount, policy limit and difference.
Interpret the tool's "difference" field correctly:
- When status is "within_policy", difference is the amount remaining below the policy limit. Describe it as remaining allowance or below the limit. Never say it exceeds the limit.
- When status is "exceeds_policy", difference is the amount by which the claim is over the policy limit. Describe it as the excess amount.
- Check the arithmetic and explain the result clearly.
Use Nigerian Naira (NGN).
A claim within policy is NOT automatically approved or paid.

When a claim exceeds a policy limit:
- State that the validation result is "exceeds_policy".
- Explain the exact amount by which the claim exceeds the configured limit.
- Explain that the claim may require human review.
- Do not say the claim will be denied, partially reimbursed, approved up to the limit, or paid.
- Do not invent requirements for justifications, supporting documents, additional approvals, or exceptions.
- Do not describe approval, rejection, reimbursement, or exception procedures unless they are explicitly defined in the supplied policy information.

If asked what happens after a claim exceeds its limit, explain that the simulated policy identifies the excess amount and flags the claim for human review. It does not define the final approval, rejection, or reimbursement outcome.

Only report policy rules and procedures that are explicitly provided. If a procedure is not defined, say so clearly. Never tell a claimant that they must provide additional information, justification, receipts, or documents to proceed unless the supplied policy explicitly requires it. Do not invent a next step for the claimant.
Keep explanations of policy-limit breaches factual and concise. Do not add unsolicited advice, recommendations, or instructions about changing spending behaviour.
For a general question about exceeding a policy limit, explain only:
1. The validation tool flags the claim as "exceeds_policy".
2. The tool identifies the exact excess amount.
3. The claim is not automatically approved or paid.
4. The simulated policy does not specify the final approval, rejection, or reimbursement outcome.
Do not add further procedures or speculate about what the claimant should do.
For claims within policy, including claims exactly equal to the policy limit:
- State that the claim is within the configured limit.
- Report the remaining allowance, which may be zero.
- Never say that human review is unnecessary or that the claim is approved.

For claims exceeding policy:
- Report the exact excess amount.
- Never instruct the claimant to stop, proceed with, or make a payment.
- Do not give payment instructions or make payment decisions.
- State only that the claim is outside the configured limit and may require human review.

Never infer approval status, review exemptions, or payment instructions from the numerical validation result.
Never say "no further action is required" or imply that a claim within policy is exempt from review. For a claim exactly equal to its policy limit, state that it is within the limit with zero remaining allowance, but that this does not establish approval or exemption from review.
These are simulated company policies for an educational project.
When a user asks for the expense policy limits, all categories, or a general policy overview, list all four limits directly:
- Transport: ₦50,000
- Meals: ₦30,000
- Accommodation: ₦150,000
- Other: ₦25,000

Do not ask the user to select a category when they request all policy limits.
Make clear that these are simulated company policy limits.
Ask for missing information when necessary.
"""

def create_expense_agent():
    """Create the agent selected by the AI_PROVIDER setting."""

    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if provider == "groq":
        import requests

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing.")

        class GroqRuntime:
            async def close(self):
                pass

        class GroqAgent:
            async def run(self, question):
                messages = [
                    {"role": "system", "content": INSTRUCTIONS},
                    {"role": "user", "content": question}
                ]

                tools = [{
                    "type": "function",
                    "function": {
                        "name": "check_expense_claim",
                        "description": "Validate an employee expense against company policy.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "category": {
                                    "type": "string",
                                    "enum": ["transport", "meals", "accommodation", "other"]
                                },
                                "amount": {"type": "number"}
                            },
                            "required": ["category", "amount"]
                        }
                    }
                }]

                for _ in range(5):
                    result = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": os.getenv(
                                "GROQ_MODEL",
                                "openai/gpt-oss-20b"
                            ),
                            "messages": messages,
                            "tools": tools,
                            "tool_choice": "auto",
                            "temperature": 0.2
                        },
                        timeout=60
                    )

                    result.raise_for_status()
                    message = result.json()["choices"][0]["message"]
                    messages.append(message)

                    calls = message.get("tool_calls") or []

                    if not calls:
                        return SimpleNamespace(
                            text=message.get("content") or
                            "The assistant returned an empty response."
                        )

                    for call in calls:
                        if call["function"]["name"] != "check_expense_claim":
                            continue

                        arguments = json.loads(call["function"]["arguments"])
                        policy_result = check_expense_claim(
                            arguments["category"],
                            arguments["amount"]
                        )

                        messages.append({
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "content": json.dumps(policy_result)
                        })

                raise RuntimeError("The AI reached its tool-call limit.")

        return GroqAgent(), GroqRuntime()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing.")

        from google import genai

        class GeminiRuntime:
            def __init__(self):
                self.client = genai.Client(api_key=api_key)

            async def close(self):
                self.client.close()

        class GeminiAgent:
            async def run(self, question):
                from google.genai import types

                contents = [types.Content(
                    role="user",
                    parts=[types.Part(text=question)]
                )]

                tool_definition = {
                    "function_declarations": [{
                        "name": "check_expense_claim",
                        "description": "Validate an employee expense against company policy.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "category": {
                                    "type": "STRING",
                                    "description": "transport, meals, accommodation or other"
                                },
                                "amount": {
                                    "type": "NUMBER",
                                    "description": "Expense amount in Nigerian Naira"
                                }
                            },
                            "required": ["category", "amount"]
                        }
                    }]
                }

                for attempt in range(3):
                    response = runtime.client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=INSTRUCTIONS,
                            tools=[types.Tool(**tool_definition)]
                        )
                    )

                    candidate = response.candidates[0].content
                    contents.append(candidate)

                    calls = response.function_calls or []

                    if not calls:
                        return SimpleNamespace(
                            text=response.text or "I could not generate a response."
                        )

                    for call in calls:
                        if call.name == "check_expense_claim":
                            result = check_expense_claim(
                                call.args["category"],
                                call.args["amount"]
                            )
                            contents.append(types.Content(
                                role="tool",
                                parts=[types.Part.from_function_response(
                                    name=call.name,
                                    response=result
                                )]
                            ))

                return SimpleNamespace(
                    text="I could not complete the policy analysis. Please try again."
                )

        runtime = GeminiRuntime()
        agent = GeminiAgent()
        return agent, runtime

    if provider == "ollama":
        from agent_framework import tool
        from agent_framework.ollama import OllamaChatClient
        from typing import Annotated

        @tool(
            name="check_expense_claim",
            description="Validate an employee expense against company policy."
        )
        def expense_policy_tool(
            category: Annotated[str, "transport, meals, accommodation or other"],
            amount: Annotated[float, "Expense amount in Nigerian Naira"]
        ) -> str:
            return json.dumps(check_expense_claim(category, amount))

        client = OllamaChatClient(model="qwen2.5:3b")

        agent = client.as_agent(
            name="ExpenseClaimAssistant",
            description="An AI assistant for employee expense claim analysis.",
            instructions=INSTRUCTIONS + """
Always use the Python expense policy tool to validate claims.
Never claim that a real payment or approval has occurred.
""",
            tools=[expense_policy_tool],
        )

        return agent, client

    raise ValueError("AI_PROVIDER must be either 'ollama' or 'gemini'.")


async def main():
    agent, client = create_expense_agent()
    try:
        response = await agent.run(
            "Check a transport expense claim of 35000 Naira."
        )
        print(response.text)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
