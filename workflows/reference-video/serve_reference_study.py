"""Serve an existing study folder locally, with MP4 byte-range seeking.

Example:
  python serve_reference_study.py --root docs/video-references/2026-11-13-user-samples
The server binds only to 127.0.0.1 and never serves resolved paths outside root.
"""
import argparse
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit


class StudyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory, **kwargs):
        self.study_root = Path(directory).resolve()
        self.byte_range = None
        super().__init__(*args, directory=str(self.study_root), **kwargs)

    def send_head(self):
        self.byte_range = None
        path = Path(self.translate_path(self.path)).resolve()
        try:
            path.relative_to(self.study_root)
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN, 'Outside study folder')
            return None
        if path.is_dir():
            for name in ('index.html', 'index.htm'):
                index = path / name
                if index.exists():
                    try:
                        index.resolve().relative_to(self.study_root)
                    except ValueError:
                        self.send_error(HTTPStatus.FORBIDDEN, 'Outside study folder')
                        return None
                    break
            return super().send_head()
        try:
            stream = path.open('rb')
        except (OSError, ValueError):
            self.send_error(HTTPStatus.NOT_FOUND, 'File not found')
            return None
        size = path.stat().st_size
        range_header = self.headers.get('Range')
        if range_header:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header.strip())
            valid = bool(match and (match[1] or match[2]) and size)
            start, end = 0, size - 1
            if valid:
                if match[1]:
                    start = int(match[1])
                    end = min(int(match[2]), size - 1) if match[2] else size - 1
                else:
                    length = int(match[2])
                    start, end = max(0, size - length), size - 1
                    valid = length > 0
                valid = valid and 0 <= start <= end < size
            if not valid:
                stream.close()
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
            self.send_response(HTTPStatus.PARTIAL_CONTENT)
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.send_header('Content-Length', str(end - start + 1))
            self.byte_range = (start, end)
        else:
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Length', str(size))
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Last-Modified', self.date_time_string(path.stat().st_mtime))
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        try:
            if self.byte_range is None:
                shutil.copyfileobj(source, outputfile, length=256 * 1024)
                return
            start, end = self.byte_range
            source.seek(start)
            remaining = end - start + 1
            while remaining:
                data = source.read(min(remaining, 256 * 1024))
                if not data:
                    break
                outputfile.write(data)
                remaining -= len(data)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # Seeking or switching videos cancels the previous browser request.
            return

    def log_message(self, fmt, *args):
        # No query strings, cookies or request headers in study-server output.
        if args:
            print(f'{self.command} {urlsplit(self.path).path} {args[1] if len(args) > 1 else ""}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8880)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    if not root.is_dir() or not (root / 'index.html').is_file():
        parser.error('--root must be a study directory containing index.html')
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(StudyHandler, directory=root))
    print(f'Study library: http://127.0.0.1:{args.port}/index.html', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
