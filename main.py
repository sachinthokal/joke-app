from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_joke():
    jokeURL = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(jokeURL, timeout=5)  # Timeout 5 sec
        response.raise_for_status()  # HTTP error handle
        joke = response.json()
    except requests.exceptions.RequestException as e:
        # Kahi error zali tar fallback joke
        print("Error fetching joke:", e)
        joke = {
            "setup": "Oops! Couldn't fetch a joke right now.",
            "punchline": "Please try again later 😅"
        }
    return joke

@app.route("/")
def joke():
    response = get_joke()
    return render_template("index.html", data=response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
