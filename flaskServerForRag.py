import os
import asyncio
import serverLightrag
from flask import Flask, jsonify, request

app = Flask(__name__)
serverRag = serverLightrag.lightRag()
asyncio.run(serverRag.setupRag())


@app.route("/query", methods=["POST"])
def queryAI(): 
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    requestDict = request.json # how you get the json that is being sent to you in post request
    userQuery = requestDict.get("user_query", None)

    if userQuery is None:
        return jsonify({"message": "Invalid item data"}), 400

    aiResponse = asyncio.run(serverRag.chat(userQuery))

    responseDict = {"message": aiResponse}
                    
    return jsonify(responseDict), 200



if __name__ == "__main__":
    app.run()



