import openai
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import random
import pyttsx3

# Set your OpenAI API key
openai.api_key = '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'

# Story templates with associated prompts
story_templates = {
    "Sci-Fi": "In the year 2050, {character} discovers {technology} that changes the course of humanity.",
    "Mystery": "Detective {detective_name} is called to investigate a mysterious {crime} in {city}.",
    "Fantasy": "In a magical kingdom, {hero} embarks on a quest to {mission}.",
}

def generate_story(template, variables):
    template_prompt = story_templates[template].format(**variables)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=template_prompt,
        max_tokens=300,
        temperature=0.7,
        n=1
    )
    generated_story = response.choices[0].text.strip()

    lines = [line.strip() for line in generated_story.split("\n") if line.strip()]
    formatted_story = "\n".join(lines)

    return formatted_story

def generate_and_display_story(template, variables):
    generated_story = generate_story(template, variables)

    story_window = tk.Toplevel()
    story_window.title(f"Generated {template} Story")

    story_text = scrolledtext.ScrolledText(story_window, wrap=tk.WORD, width=60, height=20, font=("Arial", 12), bg="#f0f0f0", fg="#000000")
    story_text.insert(tk.END, generated_story)
    story_text.pack(expand=True, fill='both')

    threading.Thread(target=fade_in_animation, args=(story_text, generated_story, 1.5)).start()

    # Add text-to-speech functionality
    speak_thread = threading.Thread(target=speak_story, args=(generated_story,))
    speak_thread.start()

def flash_button_color(button):
    colors = ["#ff0000", "#00ff00", "#0000ff"]
    random_color = random.choice(colors)
    button.configure(foreground=random_color)
    button.after(500, flash_button_color, button)

def fade_in_animation(widget, text, duration=0.5):
    steps = 10
    sleep_time = duration / steps
    alpha_step = 1.0 / steps

    for i in range(steps + 1):
        alpha = i * alpha_step
        widget.configure(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, text[:int(alpha * len(text))])
        widget.configure(state=tk.DISABLED)
        widget.update()
        time.sleep(sleep_time)

def speak_story(text):
    engine = pyttsx3.init()
    # Set the speech rate (speed) - Adjust the rate as needed
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # You can experiment with different values

    engine.say(text)
    engine.runAndWait()

def show_gui():
    root = tk.Tk()
    root.title("Story Generator")

    selected_template = tk.StringVar()
    selected_template.set("Sci-Fi")

    template_label = ttk.Label(root, text="Choose a story template:", padding=(10, 10, 10, 0), font=("Arial", 14))
    template_dropdown = ttk.Combobox(root, textvariable=selected_template, values=list(story_templates.keys()), font=("Arial", 12))
    template_label.pack(pady=10)
    template_dropdown.pack(pady=10)

    variable_entries = {}
    for variable_name in ["character", "technology", "detective_name", "crime", "city", "hero", "mission"]:
        entry_label = ttk.Label(root, text=f"Enter a value for '{variable_name}':", padding=(10, 0, 10, 0), font=("Arial", 12))
        entry_value = ttk.Entry(root, font=("Arial", 12))
        entry_label.pack(pady=5)
        entry_value.pack(pady=5)
        variable_entries[variable_name] = entry_value

    def generate_story_callback():
        variables = {name: entry.get() for name, entry in variable_entries.items()}
        generate_and_display_story(selected_template.get(), variables)

    generate_button = tk.Button(root, text="Generate Story", command=generate_story_callback, font=("Arial", 12), fg="#000000", bg="#ffffff")
    generate_button.pack(pady=20)

    flash_button_color(generate_button)

    root.mainloop()

if __name__ == "__main__":
    show_gui()
