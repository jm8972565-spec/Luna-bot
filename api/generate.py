import os, json
from http.server import BaseHTTPRequestHandler
from openai import OpenAI

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(n) or "{}")
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

            prompt = f'''Create content for Luna, a fictional adult virtual AI creator. Content type: {data.get("type","Short video")}. Topic: {data.get("topic") or "choose a fresh topic"}. Return ONLY valid JSON with keys idea, script, caption. Keep it SFW, natural, warm, elegant and suitable for a public social-media post. Do not claim Luna is a real person.'''

            resp = client.responses.create(
                model="gpt-5-mini",
                input=prompt
            )

            text = resp.output_text
            result = json.loads(text)

            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            body = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
