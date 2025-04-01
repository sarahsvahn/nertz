from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.json
    print("Received:", data)
    response = {"reply": f"Echo: {data['message']}"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
