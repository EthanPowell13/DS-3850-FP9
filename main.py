
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from dotenv import load_dotenv
import os
import json
import urllib.request

# Load API key from .env file
load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(api_key=apikey)

def get_completion(prompt):

    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode("utf-8")

    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {apikey}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# Function to handle submit button click
def on_submit():
    prompt = prompt_text.get("1.0", tk.END).strip()
    if prompt:
        completion = get_completion(prompt)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, completion)



# Function to handle focus in event for prompt text box
def on_focus_in(event):
    if prompt_text.get("1.0", tk.END).strip() == "Enter your prompt here...":
        prompt_text.delete("1.0", tk.END)
        prompt_text.config(fg="#000000")

# Function to handle focus out event for prompt text box
def on_focus_out(event):
    if prompt_text.get("1.0", tk.END).strip() == "":
        prompt_text.insert("1.0", "Enter your prompt here...")
        prompt_text.config(fg="#A9A9A9")

# Create the main window
window = tk.Tk()
window.title("OpenAI Completion GUI")
window.configure(bg="#E6E6FA") # Lavender background

# Add a border around the entire window
border_frame = ttk.Frame(window, padding="10", relief="solid", borderwidth=2)
border_frame.pack(padx=10, pady=10)




# Create and place the prompt text box
prompt_label = tk.Label(border_frame, text="Enter your prompt:", bg="#E6E6FA", fg="#4B0082", font=("Arial", 14, "bold"))
prompt_label.pack(pady=10)
prompt_text = scrolledtext.ScrolledText(border_frame, wrap=tk.WORD, width=50, height=10, bg="#F8F8FF", fg="#A9A9A9", font=("Arial", 12))
prompt_text.insert("1.0", "Enter your prompt here...")
prompt_text.bind("<FocusIn>", on_focus_in)
prompt_text.bind("<FocusOut>", on_focus_out)
prompt_text.pack(pady=10)

# Create and place the submit button
submit_button = tk.Button(border_frame, text="Submit", command=on_submit, bg="#4B0082", fg="#FFFFFF", font=("Arial", 12, "bold"))
submit_button.pack(pady=10)



# Create and place the output text box
output_label = tk.Label(border_frame, text="Output:", bg="#E6E6FA", fg="#4B0082", font=("Arial", 14, "bold"))
output_label.pack(pady=10)
output_text = scrolledtext.ScrolledText(border_frame, wrap=tk.WORD, width=50, height=10, bg="#F8F8FF", fg="#000000", font=("Arial", 12))
output_text.pack(pady=10)



# Run the application
window.mainloop()


