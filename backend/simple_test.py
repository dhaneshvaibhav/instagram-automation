import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

# Debug key format (without showing full key)
print(f"DEBUG: Key starts with: {GEMINI_API_KEY[:6]}... (length: {len(GEMINI_API_KEY)})")
if GEMINI_API_KEY.startswith("'") or GEMINI_API_KEY.startswith('"'):
    print("⚠️ WARNING: Your API key in .env has extra quotes!")
    GEMINI_API_KEY = GEMINI_API_KEY.strip("'\"")

genai.configure(api_key=GEMINI_API_KEY)

async def simple_test():
    print("\n--- 👋 Simple Gemini Test (Model: 2.0 Flash) ---")
    print("Just type hi, hello, or any general question. Type 'exit' to quit.\n")

    while True:
        user_input = input("👤 You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break

        if not user_input.strip():
            continue

        try:
            # Try a stable model first if 2.0 fails
            model_name = 'gemini-1.5-flash' 
            # model_name = 'gemini-2.0-flash-exp'
            print(f"⏳ AI is thinking (using {model_name})...")
            model = genai.GenerativeModel(model_name)
            
            response = await model.generate_content_async(user_input)
            print(f"🤖 Gemini: {response.text.strip()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(simple_test())
