import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import os
import openai


app = Flask(__name__)
CORS(app)

openai_api_key = os.getenv('OPENAI_API_KEY')


@app.route('/scrape', methods=['POST'])
def scrape_url():
    url = request.json.get('scrape')
    if url is None:
        return jsonify({'error': 'Please provide a URL parameter'})

    # send a GET request to the URL
    response = requests.get(url)

    # check if the request was successful
    if response.status_code != 200:
        return jsonify({'error': 'Unable to access URL'})

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # get the heading and paragraph text
    heading = soup.find('h1').text if soup.find(
        'h1') else "No heading to be scraped"

    paragraphs = soup.find_all('p')
    if paragraphs:
        paragraph_text = "\n\n ".join([p.text for p in paragraphs])
    else:
        paragraph_text = "No paragraph to be scraped"

    # call the open_ai endpoint with the extracted text as a parameter
    # return jsonify({'heading': heading, 'paragraph_text': paragraph_text})
    return jsonify(paragraph_text)

    





@app.route('/openai', methods=['POST'])
def openai_summary():
    text = str(request.json.get('text'))
    if text is None:
        return jsonify({'error': 'Please provide a text parameter'})

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Summarize key point from the following, Your summary should be approximately 3 - 7 sentences in length and cover the main points of the article. Use clear, concise language and avoid repeating information. Separeate each sentence with new line syntax. Here is the text: "+ text,
        max_tokens=60,
        temperature=0.5
    )
    print(response)
    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True)
