import openai
import subprocess
import json

# Set the api key directly
openai.api_key = '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'

# Define the Node.js script's path
node_script_path = 'src\\features\\scraping\\ex.js'


def get_scanner_data(website_url):
    # Execute the Node.js script using subprocess
    # Specify 'utf-8' encoding for the output
    process = subprocess.run(['node', node_script_path, website_url], capture_output=True, text=True, encoding='utf-8')

    # Check if the subprocess ran successfully
    if process.returncode == 0:
        # Get the stdout from the Node.js script and parse the JSON
        output = process.stdout
        # print("output", output)
        data = json.loads(output)  # Parse the JSON output from Node.js
        # print("Data received from Node.js:", data)
        return data
    else:
        # print("Node.js script failed with return code:", process.returncode)
        return False

def ask_openai_gpt4(url, question):
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
                        "text": f"<question> {question} </question>\n<url>{url}</url>"
                    }
                ]
            }
        ]

    chat_completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    return chat_completion.choices[0].message.content

def answer_with_pages_code(pages, question):
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
                        "text": f"{pages}\n\n#####\n\n<question> {question} </question>"
                    }
                ]
            }
        ]

    chat_completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    return chat_completion.choices[0].message.content

def answer_website(url, question):
    raw_answer = ask_openai_gpt4(url=url, question=question)
    # raw_answer = "Sorry"
    if raw_answer.startswith("Sorry"):
        raw_page = get_scanner_data(website_url=url)
        if raw_page:
            second_answer = answer_with_pages_code(pages=raw_page["page"], question=question)
            return second_answer
        else:
            return False
    else:
        return raw_answer
print(answer_website(url="https://www.airealm.tech", question="the summary of this website"))