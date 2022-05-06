from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify

application = Flask(__name__)
limiter = Limiter(
    application,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@application.route("/")
def default():
    return "default limit!"
    # return get_remote_address()


@application.route("/five")
@limiter.limit("5 per minute")
def five():
    return "5 per minute!"


@application.route("/exempt")
@limiter.exempt
def exempt():
    return "No limits!"


@application.route("/get_my_ip", methods=["GET"])  # return ip of current request
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


@application.errorhandler(429)
def ratelimit_handler(e):
    return "You have exceeded your rate-limit"
## duration?
## Endpoint



if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001, debug=False)

