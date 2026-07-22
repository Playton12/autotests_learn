import json
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class MockPetstoreHandler(BaseHTTPRequestHandler):
    pets = {}
    next_id = 1001

    @classmethod
    def reset(cls):
        cls.pets = {}
        cls.next_id = 1001

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return {}

    def _get_path(self):
        return urlparse(self.path).path.rstrip("/")

    def _get_params(self):
        return parse_qs(urlparse(self.path).query)

    def do_GET(self):
        path = self._get_path()
        params = self._get_params()

        if path == "/v2/pet/findByStatus":
            status = params.get("status", [""])[0]
            if status not in ("available", "pending", "sold", ""):
                return self._send_json({"code": 400, "type": "error", "message": "Invalid status value"}, 400)
            filtered = [p for p in self.pets.values() if p.get("status") == status or not status]
            return self._send_json(filtered)

        if path.startswith("/v2/pet/"):
            try:
                pet_id = int(path.split("/")[-1])
            except ValueError:
                return self._send_json({"code": 400, "type": "error", "message": "Invalid ID"}, 400)
            pet = self.pets.get(pet_id)
            if pet is None:
                return self._send_json({"code": 1, "type": "error", "message": "Pet not found"}, 404)
            return self._send_json(pet)

        return self._send_json({"code": 404, "type": "error", "message": "Not found"}, 404)

    def do_POST(self):
        if self._get_path() == "/v2/pet":
            body = self._read_body()
            pet_id = body.get("id", self.next_id)
            self.next_id = max(self.next_id, pet_id + 1)
            pet = {
                "id": pet_id,
                "name": body.get("name", "Unknown"),
                "status": body.get("status", "available"),
                "photoUrls": body.get("photoUrls", []),
                "category": body.get("category"),
                "tags": body.get("tags", []),
            }
            self.pets[pet_id] = pet
            return self._send_json(pet)

        return self._send_json({"code": 404, "type": "error", "message": "Not found"}, 404)

    def do_PUT(self):
        if self._get_path() == "/v2/pet":
            body = self._read_body()
            pet_id = body.get("id")
            if pet_id is None or pet_id not in self.pets:
                return self._send_json({"code": 1, "type": "error", "message": "Pet not found"}, 404)
            self.pets[pet_id] = {**self.pets[pet_id], **body}
            return self._send_json(self.pets[pet_id])

        return self._send_json({"code": 404, "type": "error", "message": "Not found"}, 404)

    def do_DELETE(self):
        path = self._get_path()
        if path.startswith("/v2/pet/"):
            try:
                pet_id = int(path.split("/")[-1])
            except ValueError:
                return self._send_json({"code": 400, "type": "error", "message": "Invalid ID"}, 400)
            if pet_id not in self.pets:
                return self._send_json({"code": 1, "type": "error", "message": "Pet not found"}, 404)
            del self.pets[pet_id]
            return self._send_json({"code": 200, "type": "unknown", "message": str(pet_id)})

        return self._send_json({"code": 404, "type": "error", "message": "Not found"}, 404)

    def log_message(self, format, *args):
        logger.debug("MockPetstore: %s", format % args)


class MockPetstoreServer:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        MockPetstoreHandler.reset()
        threading.Thread(target=self._start, daemon=True).start()

    def _start(self):
        self.server = HTTPServer((self.host, self.port), MockPetstoreHandler)
        self.port = self.server.server_address[1]
        logger.info("Mock Petstore started on http://%s:%s", self.host, self.port)
        self.server.serve_forever()

    @property
    def url(self):
        return f"http://{self.host}:{self.port}/v2"

    def stop(self):
        if hasattr(self, "server"):
            self.server.shutdown()
