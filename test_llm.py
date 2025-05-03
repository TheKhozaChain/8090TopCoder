import os
from dotenv import load_dotenv
from utils.call_llm import call_llm

def test_llm():
    # Load environment variables
    load_dotenv()
    
    # Get and mask the API key for safe printing
    api_key = os.getenv("GEMINI_API_KEY", "not_found")
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "not_found"
    print("Using API key (masked):", masked_key)
    
    test_prompt = "Please respond with a simple 'Hello, I am working!' if you receive this message."
    try:
        response = call_llm(test_prompt, use_cache=False)  # Disable cache for testing
        print("API Response:", response)
        print("\nSuccess! Your Gemini API is working correctly!")
    except Exception as e:
        print("Error occurred:", str(e))
        print("\nPlease check your API key and configuration.")

if __name__ == "__main__":
    test_llm() 