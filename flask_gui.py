from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk

app = Flask(__name__)
root = tk.Tk()
root.title("News App")

@app.route('/indonesia', methods=['GET'])
def get_berita():
    num_articles = int(request.args.get('berita', '5'))  # Get the 'berita' query parameter from the URL, defaulting to 5
    url = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE55ZVc0U0FtbGtLQUFQAQ?hl=id&gl=ID&ceid=ID%3Aid"
    r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac'})
    soup = BeautifulSoup(r.content, "html.parser")
    test = soup.find_all('c-wiz', attrs={'class': 'PIlOad'})
    titles = []
    links = []
    images = []
    for item in test:
        for img in item.find_all('figure', attrs={'class': 'K0q4G P22Vib'}):
            images.append(img.find('img')['src'])
        for teks in item.find_all('h4', attrs={'class': 'gPFEn'}):
            titles.append(teks.text)
        for link in item.find_all('a'):
            href = link.get('href')
            absolute_url = urljoin("https://news.google.com/", href)
            if '/stories/' not in absolute_url:
                links.append(absolute_url)
    berita_list = []
    for title, link, gambar in zip(titles, links, images):
        berita_list.append({'Berita': title, 'Gambar': gambar, 'Link Berita': link})
        if len(berita_list) == num_articles:
            break
    return jsonify(berita_list)

@app.route('/world', methods=['GET'])
def get_berita_world():
    num_articles = int(request.args.get('news', '5'))  # Get the 'news' query parameter from the URL, defaulting to 5
    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtbGtHZ0pKUkNnQVAB?hl=id&gl=ID&ceid=ID:id"
    r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac'})
    soup = BeautifulSoup(r.content, "html.parser")
    test = soup.find_all('c-wiz', attrs={'class': 'PIlOad'})
    titles = []
    links = []
    images = []
    for item in test:
        for img in item.find_all('figure', attrs={'class': 'K0q4G P22Vib'}):
            images.append(img.find('img')['src'])
        for teks in item.find_all('h4', attrs={'class': 'gPFEn'}):
            titles.append(teks.text)
        for link in item.find_all('a'):
            href = link.get('href')
            absolute_url = urljoin("https://news.google.com/", href)
            if '/stories/' not in absolute_url:
                links.append(absolute_url)
    berita_list = []
    for title, link, gambar in zip(titles, links, images):
        berita_list.append({'News': title, 'Image': gambar, 'Link News': link})
        if len(berita_list) == num_articles:
            break
    return jsonify(berita_list)

def start_flask_server():
    import threading

    def run_flask():
        app.run(debug=False)

    thread = threading.Thread(target=run_flask)
    thread.start()

def open_gui():
    def get_indonesia_news():
        num_articles = int(berita_entry.get())
        response = requests.get(f"http://127.0.0.1:5000/indonesia?berita={num_articles}")
        berita_list = response.json()
        result_text.delete(1.0, tk.END)
        for berita in berita_list:
            result_text.insert(tk.END, f"Berita: {berita['Berita']}\n")
            result_text.insert(tk.END, f"Gambar: {berita['Gambar']}\n")
            result_text.insert(tk.END, f"Link Berita: {berita['Link Berita']}\n\n")

    def get_world_news():
        num_articles = int(news_entry.get())
        response = requests.get(f"http://127.0.0.1:5000/world?news={num_articles}")
        news_list = response.json()
        result_text.delete(1.0, tk.END)
        for news in news_list:
            result_text.insert(tk.END, f"News: {news['News']}\n")
            result_text.insert(tk.END, f"Image: {news['Image']}\n")
            result_text.insert(tk.END, f"Link News: {news['Link News']}\n\n")

    root.geometry("600x400")

    berita_label = tk.Label(root, text="Indonesia News", font=("Arial", 16, "bold"))
    berita_label.pack()

    berita_frame = tk.Frame(root)
    berita_frame.pack()

    berita_label = tk.Label(berita_frame, text="Number of Articles:")
    berita_label.pack(side=tk.LEFT)

    berita_entry = tk.Entry(berita_frame)
    berita_entry.pack(side=tk.LEFT)

    berita_button = tk.Button(root, text="Get Indonesia News", command=get_indonesia_news)
    berita_button.pack()

    news_label = tk.Label(root, text="World News", font=("Arial", 16, "bold"))
    news_label.pack()

    news_frame = tk.Frame(root)
    news_frame.pack()

    news_label = tk.Label(news_frame, text="Number of Articles:")
    news_label.pack(side=tk.LEFT)

    news_entry = tk.Entry(news_frame)
    news_entry.pack(side=tk.LEFT)

    news_button = tk.Button(root, text="Get World News", command=get_world_news)
    news_button.pack()

    result_label = tk.Label(root, text="Result:", font=("Arial", 14, "bold"))
    result_label.pack()

    result_text = tk.Text(root, height=10, width=60)
    result_text.pack()

    root.mainloop()

if __name__ == '__main__':
    start_flask_server()
    open_gui()
