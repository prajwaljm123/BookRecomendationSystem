import requests
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = 'AIzaSyBFNpbRaRr097SQb5N1X36hZP9hws4Oda0'  # Replace with your actual API key

def generate_book_recommendation(interest, rating):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

    # Formulate a prompt to ask for book recommendations based on interest and rating
    prompt = f"Recommend books related to '{interest}' with a minimum rating of {rating}. Provide the book title, author, genre, description, and rating."

    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        # Send POST request to the API
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(request_body))
        if response.status_code == 200:
            response_data = response.json()
            print("Raw Generated Book Recommendation Text:\n", response_data)
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error generating book recommendations: {str(e)}"

def extract_book_details(generated_text):
    book_details_list = []
    
    # Adjusted pattern for flexible parsing of each section
    pattern = r"\*\*Title:\*\*\s*(.*?)\n\*\*Author:\*\*\s*(.*?)\n\*\*Genre:\*\*\s*(.*?)\n\*\*Description:\*\*\s*(.*?)\n\*\*Rating:\*\*\s*(\d+\.\d+)"

    matches = re.findall(pattern, generated_text, re.DOTALL)

    for match in matches:
        book_details = {
            'title': match[0].strip(),
            'author': match[1].strip(),
            'genre': match[2].strip(),
            'description': match[3].strip(),
            'rating': match[4].strip()
        }
        book_details_list.append(book_details)

    return book_details_list

@app.route('/recommend', methods=['POST'])
def recommend_books():
    data = request.json
    interest = data.get('interest')
    rating = data.get('rating')

    if not interest or not rating:
        return jsonify({"error": "Missing 'interest' or 'rating' in request data"}), 400

    generated_text = generate_book_recommendation(interest, rating)
    
    # Print the raw generated text
    print("Raw Generated Book Recommendation Text:\n", generated_text)

    if generated_text.startswith("Error"):
        return jsonify({"error": generated_text}), 400

    book_details = extract_book_details(generated_text)
    return jsonify(book_details), 200

if __name__ == '__main__':
    app.run(debug=True)
