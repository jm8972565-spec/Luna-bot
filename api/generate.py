import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

        prompt = f"""
Create content for Luna, a fictional adult virtual AI creator.

Content type: {data.get("type", "Short video")}
Topic: {data.get("topic") or "choose a fresh topic"}

Return ONLY valid JSON with these keys:
idea
script
caption

Keep it SFW, natural, warm, elegant and suitable for a public social-media post.
Do not claim Luna is a real person.
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        result = json.loads(response.output_text)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
