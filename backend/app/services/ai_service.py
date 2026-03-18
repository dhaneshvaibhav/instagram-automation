import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from app.utils.file_helpers import append_log

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def generate_reel_summary(caption: str, media_type: str = "VIDEO"):
    """
    Generates a concise summary of a reel based on its caption and type.
    """
    if not GEMINI_API_KEY:
        return None

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Summarize the following Instagram Reel based on its metadata.
        This summary will be used as a knowledge base for an AI assistant to reply to comments.
        
        Media Type: {media_type}
        Caption: "{caption}"
        
        Keep the summary factual and concise (under 100 words). 
        Identify the key topics, products, or questions mentioned.
        Return ONLY the summary text.
        """
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        append_log(f"Error generating reel summary: {e}", "ERROR")
        return None

async def analyze_media_and_generate_reply(comment_text: str, ai_context: str = None, ai_summary: str = None, is_dm: bool = True):
    """
    Generates a personalized reply or DM using Gemini, based on the comment and reel context.
    """
    if not GEMINI_API_KEY:
        append_log("GEMINI_API_KEY not configured, skipping AI analysis", "WARN")
        return None

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Combine context and summary for a richer knowledge base
        knowledge_base = ""
        if ai_context:
            knowledge_base += f"\nBackground Context: {ai_context}"
        if ai_summary:
            knowledge_base += f"\nReel Content Summary: {ai_summary}"

        prompt = f"""
        You are an intelligent Instagram automation assistant. You are replying to a comment on a Reel.
        
        YOUR KNOWLEDGE BASE:{knowledge_base if knowledge_base else ' No specific context provided.'}
        
        USER COMMENT: "{comment_text}"
        
        TASK:
        Generate a { 'friendly, helpful Private DM' if is_dm else 'short, engaging Public Reply' } for this comment.
        
        GUIDELINES:
        1. Use the KNOWLEDGE BASE to answer any questions asked in the comment accurately.
        2. If the user is just saying hello or being friendly, respond with equal warmth.
        3. If you don't have enough information in the KNOWLEDGE BASE to answer a specific question, be polite but honest.
        4. {'For DM: Be helpful and detailed if needed.' if is_dm else 'For Public Reply: Keep it under 20 words and encourage engagement.'}
        5. Stay natural and human-like. Avoid sounding like a bot.
        6. Return ONLY the message text. No quotes, no intro text.
        """
        
        response = await model.generate_content_async(prompt)
        return response.text.strip()
        
    except Exception as e:
        append_log(f"Error in Gemini AI analysis: {e}", "ERROR")
        return None
