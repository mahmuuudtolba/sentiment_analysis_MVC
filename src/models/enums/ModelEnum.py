from enum import Enum

class ModelEnum(Enum):
    MODEL_NAME = "openai/gpt-4o-mini"
    MODEL_ENDPOINT = "https://models.github.ai/inference"
    CLIENT_INIT="OpenAI client initialized."
    
    OPENAI_NAUTRAL = "Neutral (no input)"
    OPENAI_WARNING = "Warning: Unexpected sentiment response from OpenAI:"
    OPENAI_ERROR = "ERROR : Error calling OpenAI API"
    
    SYSTEM_PROMPT = "You are a helpful assistant that analyzes sentiment."
    
    MAX_TOKENS = 10 
    TEMPERATURE = 1 

