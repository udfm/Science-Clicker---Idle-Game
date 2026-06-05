from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Port 5000 is now Active!</h1><p>Your python web server is running smoothly.</p>"

if __name__ == '__main__':
    # CRITICAL: '0.0.0.0' tells the server to listen to all public cloud networks
    # port=5000 matches your forwarded port configuration
    app.run(host='0.0.0.0', port=5000)
