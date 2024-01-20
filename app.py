import pyshorteners
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class URL:
    def __init__(self):
        self.encodeMap = {}
        self.decodeMap = {}
        self.base = "http://tinyurl.com"

    def encode(self, longUrl: str) -> str:
        """Encode a URL to a shortened URL."""
        if longUrl not in self.encodeMap:
            s=pyshorteners.Shortener()

            shorturl = s.tinyurl.short(longUrl)
            self.encodeMap[longUrl] = shorturl
            self.decodeMap[shorturl] = longUrl
        return self.encodeMap[longUrl]

    def decode(self, shortUrl: str) -> str:
        """Decode a URL to a shortened URL."""
        return self.decodeMap[shortUrl]

url_encoder = URL()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_url = url_encoder.encode(long_url)
    return render_template('result.html', long_url=long_url, short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    long_url = url_encoder.decode(f"{url_encoder.base}/{short_url}")
    return redirect(long_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)