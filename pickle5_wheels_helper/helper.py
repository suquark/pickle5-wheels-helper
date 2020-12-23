from http.server import HTTPServer, BaseHTTPRequestHandler
import multiprocessing
import os
import pkg_resources
import socket
import sys
import time
import json
import urllib.request


def generate_pypi_indices():
    html_body="<!DOCTYPE html><html><body>{}</body></html>"
    wheels_indices = []
    with urllib.request.urlopen("https://api.github.com/repos/suquark/pickle5-backport/releases/latest") as fp:
         release_dict = json.loads(fp.read().decode("utf8"))
    for asset in release_dict['assets']:
        wheels_indices.append(f'<a href="{asset["browser_download_url"]}" data-requires-python=">=3.5.*">{asset["name"]}</a>')
    return html_body.format('\n<br>'.join(wheels_indices))


def find_available_port(port=8134):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(generate_pypi_indices().encode("utf8"))


def run(addr="localhost", port=8134):
    server_address = (addr, port)
    httpd = HTTPServer(server_address, Server)
    httpd.serve_forever()


def try_install_pickle5():
    should_install_pickle5 = False
    try:
        version_info = pkg_resources.require("pickle5")
        version = tuple(int(n) for n in version_info[0].version.split("."))
        if version < (0, 0, 11):
            should_install_pickle5 = True
    except pkg_resources.DistributionNotFound:
        should_install_pickle5 = True
    if should_install_pickle5:
        print("Count not find pickle5 >= 0.0.11 which is required. Trying to install one from prebuilt wheels...")
        port = find_available_port()
        p = multiprocessing.Process(target=run, kwargs={'port': port}, daemon=True)
        p.start()
        time.sleep(0.5)
        os.system(f'{sys.executable} -m pip install --no-index --find-links=http://localhost:{port} pickle5')
        p.terminate()
