import os
import logging
import json
from datetime import datetime

# Configure logging
log_directory = os.getenv("LOG_DIR", "logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, f"llm_calls_{datetime.now().strftime('%Y%m%d')}.log")

# Set up logger
logger = logging.getLogger("llm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to root logger
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Simple cache configuration
cache_file = "llm_cache.json"

def call_llm(prompt: str, use_cache: bool = True, model: str = None) -> str:
    """
    Call OpenAI LLM with the given prompt.
    
    Args:
        prompt: The prompt to send to the LLM
        use_cache: Whether to use caching for responses
        model: The model to use (defaults to gpt-4o)
    
    Returns:
        The LLM response as a string
    """
    # Log the prompt
    logger.info(f"PROMPT: {prompt}")
    
    # Check cache if enabled
    if use_cache:
        # Load cache from disk
        cache = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            except:
                logger.warning(f"Failed to load cache, starting with empty cache")
        
        # Return from cache if exists
        cache_key = f"{model or 'gpt-4o'}:{prompt}"
        if cache_key in cache:
            logger.info(f"RESPONSE (cached): {cache[cache_key]}")
            return cache[cache_key]
    
    # Call OpenAI API
    try:
        from openai import OpenAI
        
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        client = OpenAI(api_key=api_key)
        
        # Use provided model or default to gpt-4o
        model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        
        # Log the response
        logger.info(f"RESPONSE: {response_text}")
        
        # Update cache if enabled
        if use_cache:
            # Load cache again to avoid overwrites
            cache = {}
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r') as f:
                        cache = json.load(f)
                except:
                    pass
            
            # Add to cache and save
            cache_key = f"{model_name}:{prompt}"
            cache[cache_key] = response_text
            try:
                with open(cache_file, 'w') as f:
                    json.dump(cache, f)
            except Exception as e:
                logger.error(f"Failed to save cache: {e}")
        
        return response_text
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise

# Alternative models for specific use cases
def call_llm_o1(prompt: str, use_cache: bool = True) -> str:
    """Call OpenAI o1 model for complex reasoning tasks."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="o1",
            messages=[{"role": "user", "content": prompt}],
            reasoning_effort="medium"
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error calling OpenAI o1 API: {e}")
        raise

if __name__ == "__main__":
    test_prompt = "Hello, how are you?"
    
    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
    
