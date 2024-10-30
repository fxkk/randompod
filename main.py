import requests
import random
import xml.etree.ElementTree as ET
from flask import Flask, redirect

app = Flask(__name__)

def get_random_podcast_url(podcast_name):
    # Fetch the XML data from podigee.com
    response = requests.get(f'https://{podcast_name}.podigee.io/feed/mp3')
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the XML data
    root = ET.fromstring(response.content)

    # Find all items in the XML structure
    items = root.findall('.//item')

    # Extract the enclosure URLs from each item
    urls = [item.find('.//enclosure').attrib['url'] for item in items if item.find('.//enclosure') is not None]

    # Select a random URL from the list
    random_url = random.choice(urls)
    
    return random_url

@app.route('/<podcast_name>')
def redirect_to_podcast(podcast_name):
    try:
        # Get a random podcast URL
        podcast_url = get_random_podcast_url(podcast_name)
        # Redirect to the podcast URL
        return redirect(podcast_url, code=302)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
