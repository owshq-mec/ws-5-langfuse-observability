"""A local webhook receiver for Langfuse alert automations, so no alert payload leaves the laptop.

Runs as the compose service `alert-sink`: in Langfuse, point an alert automation (webhook) at
http://alert-sink/langfuse. Langfuse accepts only ports 80 and 443 and blocks private hosts unless they are
whitelisted (LANGFUSE_WEBHOOK_WHITELISTED_HOST in infra/docker-compose.yml).

    make alerts        # print the alerts received so far (uv run python scripts/alert_sink.py --tail)

Every POST is appended to .helix/alerts.jsonl with its headers. When ALERT_WEBHOOK_SECRET is set, the
x-langfuse-signature header is checked (HMAC-SHA256 of "<timestamp>.<body>").
"""

import argparse
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LOG = Path(os.environ.get("ALERT_SINK_LOG") or Path(__file__).resolve().parents[1] / ".helix" / "alerts.jsonl")


def signature_ok(headers, body: bytes) -> bool | None:
    secret = os.environ.get("ALERT_WEBHOOK_SECRET")
    header = headers.get("x-langfuse-signature")
    if not secret or not header:
        return None
    parts = dict(part.split("=", 1) for part in header.split(",") if "=" in part)
    expected = hmac.new(secret.encode(), f"{parts.get('t', '')}.{body.decode()}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, parts.get("v1", ""))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        body = self.rfile.read(int(self.headers.get("content-length", 0)))
        try:
            payload = json.loads(body or b"{}")
        except ValueError:
            payload = {"raw": body.decode(errors="replace")}
        record = {"received_at": datetime.now(timezone.utc).isoformat(), "path": self.path,
                  "signature_ok": signature_ok(self.headers, body), "payload": payload}
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            f.write(json.dumps(record) + "\n")
        print(f"alert received: {json.dumps(payload)[:300]}", flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"alert-sink up")

    def log_message(self, *_) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--tail", action="store_true", help="print received alerts and exit")
    args = parser.parse_args()
    if args.tail:
        for line in LOG.read_text().splitlines() if LOG.exists() else []:
            record = json.loads(line)
            print(record["received_at"], json.dumps(record["payload"])[:400])
        return
    print(f"alert-sink listening on :{args.port}, writing {LOG}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
