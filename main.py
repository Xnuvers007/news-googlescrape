from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/indonesia', methods=['GET'])
def get_berita():
    num_articles = int(request.args.get('berita', '5'))  # Get the 'j' query parameter from the URL, defaulting to 5
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
    num_articles = int(request.args.get('news', '5'))  # Get the 'j' query parameter from the URL, defaulting to 5
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

if __name__ == '__main__':
    app.run(debug=False)
