from threading import Thread
import openai
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

openai_key = os.getenv('OPEAN_AI')
# Set the api key directly
openai.api_key = openai_key

# Define the Node.js script's path
node_script_path = 'src\\features\\scraping\\website_scrap.js'

class Openai_gpt4(Thread):
    def __init__(self, url: str, prompt:str) -> None:
        super().__init__()
        if "http" in url:
            self.url = "http://" + url
        else:
            self.url = url
        self.prompt = prompt
        self.code = None
        self.result = None

    def run(self) -> None:
        messages = [
                {
                    "role": "system",
                    "content": "You will be provided with the url of one website and question about this website. You must answer for this question. The answer must be detailed and correctly, and be clear to understand. If you don't know about the given website, your answer must start with 'Sorry'."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"<question> {self.prompt} </question>\n<url>{self.url}</url>"
                        }
                    ]
                }
            ]
        try:
            chat_completion = openai.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages
            )
            self.result = chat_completion.choices[0].message.content
            self.code = 200
        except Exception as e:
            self.result = False
            self.code = e.response.json()["error"]["code"]

class Scrap_gpt4(Thread):
    def __init__(self, url: str, prompt:str) -> None:
        super().__init__()
        self.url = url
        self.prompt = prompt
        self.code = None
        self.result = None

    def run(self) -> None:
        process = subprocess.run(['node', node_script_path, self.url], capture_output=True, text=True, encoding='utf-8')

        # Check if the subprocess ran successfully
        if process.returncode == 0:
            # Get the stdout from the Node.js script and parse the JSON
            output = process.stdout
            # print("output", output)
            data = json.loads(output)  # Parse the JSON output from Node.js
            # print("Data received from Node.js:", data)
            if data["page"] == "FALSE/FALSE":
                self.result = False
                self.code = "Scrapping_failed"
            else:
                messages = [
                        {
                            "role": "system",
                            "content": "You will be provided with the all contents of one website and question about this website. You must answer for this question. The answer must be detailed and correctly, and be clear to understand."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"{data["page"]}\n\n#####\n\n<question> {self.prompt} </question>"
                                }
                            ]
                        }
                    ]
                try:
                    chat_completion = openai.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=messages
                    )
                    self.result = chat_completion.choices[0].message.content
                    self.code = 200
                except Exception as e:
                    self.result = False
                    self.code = e.response.json()["error"]["code"]
        else:
            # print("Node.js script failed with return code:", process.returncode)
            self.result = False
            self.code = "Scrapping_failed"

def answer_website(url, question):
    thread1 = Openai_gpt4(url=url, prompt=question)
    thread2 = Scrap_gpt4(url=url, prompt=question)
    thread1.start()
    thread2.start()
    thread1.join()
    if thread1.result:
        if thread1.result.startswith("Sorry"):
            thread2.join()
            return thread2.result, thread2.code
        else:
            return thread1.result, thread1.code
    else:
        return False, thread1.code