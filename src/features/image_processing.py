import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

openai_key = os.getenv('OPEAN_AI')
# Set the api key directly
openai.api_key = openai_key

# # When using `openai.Image.create`, it's not necessary to create an OpenAI client object

def image_generation(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url, True
    except Exception as e:
        return False, e.response.json()["error"]["code"]

# print(image_generation("a white siamese cat"))

def image_description(image_url, prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a cool image analyst.  Your goal is to describe what is in this image."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",      # Replace this with the actual model name that supports image analysis
            messages=messages,
            max_tokens=1024,
            n=1,
            temperature=0.0
            # 'stop' parameter has been removed because it was set to None which is invalid
        )
        return response.choices[0].message.content, True
    except Exception as e:
        return False, e.response.json()["error"]["code"]

# image_description("https://api.telegram.org/file/bot7144158465:AAFzpfFgORQ2veBlq_TNWA7yZBznwLAgHc4/photos/file_0.jpg", "What is name of this flower")