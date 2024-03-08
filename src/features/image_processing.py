import openai

# Set the api key directly
openai.api_key = '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'

# # When using `openai.Image.create`, it's not necessary to create an OpenAI client object

def image_generation(prompt):
    response = openai.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Extracting the URL from the response
    image_url = response.data[0].url
    print(image_url)

# image_generation("a white siamese cat")

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

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",      # Replace this with the actual model name that supports image analysis
        messages=messages,
        max_tokens=1024,
        n=1,
        temperature=0.0
        # 'stop' parameter has been removed because it was set to None which is invalid
    )
    # Print the text completion
    print(response.choices[0].message.content)

# image_description("https://cdn.repliers.io/IMG-X5925532_9.jpg")