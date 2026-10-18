"""Local preview server with HTTP Range support.

`python -m http.server` cannot serve byte ranges, so browsers treat the hero video
as non-seekable and the scroll-controlled video does not work. Real web servers
(Vercel, nginx, Apache) support ranges; this script does the same locally.

Usage:  python tools/serve.py [port]      (default port 8080, serves the project root)
"""

import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RangeHandler(SimpleHTTPRequestHandler):
    _range = None

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")  # preview: always re-check files after a rebuild
        super().end_headers()

    def send_head(self):
        self._range = None
        header = self.headers.get("Range")
        path = self.translate_path(self.path)
        match = re.match(r"bytes=(\d*)-(\d*)$", header or "")
        if not match or not os.path.isfile(path):
            return super().send_head()

        size = os.path.getsize(path)
        first, last = match.groups()
        if first == "":                      # suffix range: last N bytes
            start, end = max(size - int(last or 0), 0), size - 1
        else:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        if start > end or start >= size:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        handle = open(path, "rb")
        handle.seek(start)
        self._range = end - start + 1
        return handle

    def copyfile(self, source, outputfile):
        try:
            if self._range is None:
                super().copyfile(source, outputfile)
                return
            remaining = self._range
            while remaining > 0:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the browser cancelled the request (normal when scrubbing video)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    handler = partial(RangeHandler, directory=ROOT)
    print(f"Serving {ROOT} at http://localhost:{port}/")
    ThreadingHTTPServer(("", port), handler).serve_forever()
