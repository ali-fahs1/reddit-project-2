from dotenv import load_dotenv
import os
load_dotenv()

from langchain.chat_models import init_chat_model
my_GOOGLE_API_KEY= os.environ.get("GOOGLE_API_KEY")
model=init_chat_model(model="gemini-3.6-flash",model_provider="google_genai",api_key=my_GOOGLE_API_KEY)

print(model.invoke("what your name").content)