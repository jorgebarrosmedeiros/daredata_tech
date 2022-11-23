# import modules
from flask import Flask, request
from predict import predict

# define the app
app = Flask(__name__)
# define the function to be called
@app.route("/", methods=["POST"])
def data_service():
    data = request.get_json(force=True)

    response = predict(data)

    return response


# define the main function
if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
