from openai import OpenAI
import requests
import base64
import os
import tkinter as tk
import json
client = OpenAI(
  api_key=os.environ.get('OPEN_API_KEY'),
)
github_token = os.environ.get('GITHUB_KEY')
github_headers = {
    'Authorization': f'token {github_token}',
    'Content-Type': 'application/json'
}

# Fetch the code from a specified GitHub repository
repo_owner = 'IAMNISHANTSHUKLA'
repo_name = 'XCCC'
url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents'

response = requests.get(url, headers=github_headers)
repo_contents = response.json()
analysis_code = ''


def update_text(new_text):
  text_widget.config(state=tk.NORMAL)
  text_widget.delete("1.0", tk.END)
  text_widget.insert(tk.END, new_text)
  text_widget.config(state=tk.DISABLED)
   
    
window = tk.Tk()
# Make the window fullscreen
window.title("Dynamic Text Update")

# Create a scrollbar for the text widget
scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL)

# Create and place a text widget with a scrollbar
text_widget = tk.Text(window, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=10, width=40)
text_widget.pack(pady=10, expand=True, fill=tk.BOTH)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Attach the scrollbar to the text widget
scrollbar.config(command=text_widget.yview)


for content in repo_contents:
    if content['type'] == 'file':
        file_name = content['name']
        file_content = requests.get(content['download_url']).text

        # Send the code to ChatGPT for analysis
        prompt = f"Analyze the code '{file_content}' Find code improvement suggestions in a user-friendly short format."
        completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
)      
        promptTwo = f"Analyze for bugs and optimization,.respond short/concisely, code: '{file_content}'"
        completionBugs = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": promptTwo}
  ]
)       
        analysis_code = analysis_code + '\n' + completion.choices[0].message.content +'\n' + completionBugs.choices[0].message.content 
        print("Resp1",completion.choices[0].message.content)
        update_text(analysis_code)
        print("\n")
        
window.mainloop()
