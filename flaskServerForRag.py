import os
import asyncio
import serverLightrag
from flask import Flask, jsonify, request
import ollama

app = Flask(__name__)
serverRag = serverLightrag.lightRag()
asyncio.run(serverRag.setupRag())


@app.route("/health", methods=["GET"])
def health():
        return jsonify(status="ok"), 200

@app.route("/query", methods=["POST"])
def queryAI(): 
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    requestDict = request.json # how you get the json that is being sent to you in post request
    userQuery = requestDict.get("user_query", None)

    if userQuery is None:
        return jsonify({"message": "Invalid item data"}), 400

    aiPrompt = asyncio.run(serverRag.chat(userQuery)) # this is just getting us the prompt
    aiResponse = ollama.chat(model="qwen2:latest", messages=[{'role': 'user', 'content': aiPrompt}])

    sourcesSectionAndBelow = aiPrompt.split("Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks)")[1]
    sources = sourcesSectionAndBelow.split("---User Query---")[0]




    responseDict = {"content": aiResponse.message.content, "sources": sources}
                    
    return jsonify(responseDict), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)



