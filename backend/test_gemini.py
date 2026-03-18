import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

async def test_gemini():
    print("\n--- 🤖 Gemini AI Test Terminal ---")
    print("This script simulates how the Reel Reply system uses Gemini.")
    print("Type 'exit' to quit.\n")

    # Optional: Mock some Reel context for the test
    context = input("Enter some context about your Reel (or press Enter for none): ")
    summary = input("Enter a short summary of your Reel (or press Enter for none): ")

    while True:
        comment = input("\n👤 Simulated Comment: ")
        
        if comment.lower() in ['exit', 'quit']:
            break

        if not comment.strip():
            continue

        try:
            print("⏳ AI is thinking...")
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            knowledge_base = ""
            if context:
                knowledge_base += f"\nBackground Context: {context}"
            if summary:
                knowledge_base += f"\nReel Content Summary: {summary}"

            prompt = f"""
            You are an intelligent Instagram automation assistant. You are replying to a comment on a Reel.
            
            YOUR KNOWLEDGE BASE:{knowledge_base if knowledge_base else ' No specific context provided.'}
            
            USER COMMENT: "{comment}"
            
            TASK:
            Generate a short, engaging Public Reply for this comment.
            
            GUIDELINES:
            1. Use the KNOWLEDGE BASE to answer any questions accurately.
            2. Keep it under 20 words.
            3. Stay natural and human-like.
            4. Return ONLY the message text.
            """
            
            response = await model.generate_content_async(prompt)
            print(f"🤖 AI Reply: {response.text.strip()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
