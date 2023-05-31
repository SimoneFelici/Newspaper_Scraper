import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from transformers import pipeline
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

def generate_summary(text):
    summarization_pipeline = pipeline("text-generation", model="gpt2-xl", tokenizer="gpt2-xl")
    summary = summarization_pipeline(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['generated_text']

def scrape_and_display(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all('p')

        text = ''
        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            if paragraph_text:
                formatted_text = re.sub(r'\.(\s|$)', '.\n', paragraph_text)
                text += formatted_text + '\n'

        output_text.delete("1.0", tk.END)  # Clear previous output
        output_text.insert(tk.END, text)

        # Prompt the user to generate a summary
        generate_summary_prompt = messagebox.askyesno("Summary Generation", "Would you like to generate a summary?")
        if generate_summary_prompt:
            summary = generate_summary(text)
            output_text.insert(tk.END, "\n\nSummary:\n")
            output_text.insert(tk.END, summary)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred while making the request: {e}")

def extract_urls_from_site(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all('a', href=True)
        urls = [link['href'] for link in links if link['href'].startswith('http')]

        return urls
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred while making the request: {e}")
        return []

site_urls = ["https://nascecresceignora.it/", "https://www.everyeye.it/"]
site_names = [urlparse(url).hostname.replace("www.", "").split(".")[0] for url in site_urls]

site_names.append("Enter custom URL...")  # Add option to enter a custom URL

root = tk.Tk()
root.title("Website Scraper")
root.geometry("500x400")

selected_site = ttk.Combobox(root, values=site_names)
selected_site.set("Select a website to scrape")
selected_site.pack()

def handle_selection():
    selected = selected_site.get()
    if selected == "Enter custom URL...":
        site_url = simpledialog.askstring("Custom URL", "Enter the website URL:")
        if not site_url:
            messagebox.showerror("Error", "No website URL entered. Exiting...")
            root.quit()
        parsed_url = urlparse(site_url)
        site_name = parsed_url.netloc.replace("www.", "").split(".")[0]
        messagebox.showinfo("Website Selection", f"You have entered the website: {site_name}")
    else:
        site_url = site_urls[site_names.index(selected)]
        site_name = selected
        messagebox.showinfo("Website Selection", f"You have selected the website: {site_name}")

    urls = extract_urls_from_site(site_url)

    titles = {re.sub(r'\W+', ' ', url): url for url in urls}

    selected_title = simpledialog.askstring("News Titles", "Select a news title:", 
                                            list(titles.keys()))

    if selected_title:
        selected_link = titles[selected_title]
        scrape_and_display(selected_link)

# Create the output text widget
output_text = tk.Text(root, height=20, width=60)
output_text.pack()

# Create the "Scrape" button
scrape_button = ttk.Button(root, text="Scrape", command=handle_selection)
scrape_button.pack()

root.mainloop()
