import os


from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = FastAPI(title="CPI Groovy Copilot API")
#Initialize the Google GenAI client with the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable is not set.")
client = genai.Client(api_key=api_key)

class GroovyRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Welcome to the CPI Groovy Helper API!"}

@app.get("/api/v1/sum")
async def find_sum(num1:int, num2:int):
    return {"sum": num1 + num2}
    
@app.post("/api/v1/generate-groovy")
async def generate_groovy(request: GroovyRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail={"error": "A prompt is required."})

    try:
        # Load the system prompt template from the file
        template_path = "backend/templates/system_prompt.txt"
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"System prompt file not found at: {template_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

        formatted_prompt = system_prompt.replace(
            "{user_prompt}", 
            request.prompt.strip())

        generation_config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1000,
        )
        # Generate content using the Google GenAI client
        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
        )
        #verify the response and extract the generated text
        

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=1000,
            ),
        )

        generated = getattr(response, "text", None)
        if not generated:
            candidates = getattr(response, "candidates", None) or []
            if candidates and getattr(candidates[0], "content", None):
                parts = getattr(candidates[0].content, "parts", None) or []
                if parts and getattr(parts[0], "text", None):
                    generated = parts[0].text

        if not generated or not str(generated).strip():
            raise HTTPException(status_code=500, detail={"error": "No output from the model."})

        return {
            "generated_groovy": generated,
            "status": "success",
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"error": str(exc)}) from exc
    

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
