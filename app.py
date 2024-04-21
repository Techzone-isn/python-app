from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
db_path = 'mirror_db.sqlite'

# Create a function to initialize the database
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mirrors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_word TEXT,
            mirrored_word TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call the init_db function to create the database if it doesn't exist
init_db()
# Define the mirror endpoint
@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/mirror')
def mirror():
    word = request.args.get('word', '')
    transformed_word = transform_word(word)
    save_to_db(word, transformed_word)
    return jsonify({"transformed": transformed_word})

def transform_word(word):
    transformed = ''
    for char in word:
        if char.islower():
            transformed += char.upper()
        elif char.isupper():
            transformed += char.lower()
        else:
            transformed += char
    return transformed[::-1]

def save_to_db(original_word, mirrored_word):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mirrors (original_word, mirrored_word) VALUES (?, ?)', (original_word, mirrored_word))
    conn.commit()
    conn.close()

# Run the Flask app
import requests

def test_mirror_endpoint():
    response = requests.get('http://54.169.232.18:4004/api/mirror?word=fOoBar25')
    data = response.json()
    assert data['transformed'] == '52RAbOoF'

if __name__ == '__main__':
        app.run(port=4004, host='54.169.232.18')
