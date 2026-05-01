import os
import asyncio
from openai import AsyncOpenAI
import anthropic
import google.generativeai as genai

# ---- INIT ----

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

anthropic_client = anthropic.AsyncAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-pro")


# ---- ROUTER ----

async def call_llm(provider, model, prompt):
    if provider == "openai":
        return await call_openai(model, prompt)

    elif provider == "anthropic":
        return await call_claude(model, prompt)

    elif provider == "gemini":
        return await call_gemini(prompt)

    else:
        raise ValueError("Unknown provider")

async def call_openai(model, prompt):
    res = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content

async def call_claude(model, prompt):
    res = await anthropic_client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.content[0].text

async def call_gemini(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: gemini_model.generate_content(prompt).text
