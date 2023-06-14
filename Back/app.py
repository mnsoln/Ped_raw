from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    # return render_template("index.html", **{"greeting": "Hello from Flask!"})
    return jsonify("Hello from Flask!")


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4280)
