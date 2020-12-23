from setuptools import setup, find_packages
from setuptools.command.install import install

from http.server import HTTPServer, BaseHTTPRequestHandler
import multiprocessing
import os
import pkg_resources
import socket
import sys
import time

import requests


def generate_pypi_indices():
    html_body="<!DOCTYPE html><html><body>{}</body></html>"
    wheels_indices = []
    release_dict = requests.get("https://api.github.com/repos/suquark/pickle5-backport/releases/latest").json()
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


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        port = find_available_port()
        p = multiprocessing.Process(target=run, kwargs={'port': port}, daemon=True)
        p.start()
        time.sleep(0.5)
        os.system(f'{sys.executable} -m pip install --no-index --find-links=http://localhost:{port} pickle5')
        p.terminate()


setup(
    name="pickle5-wheels-indices",
    version="0.0.1",
    author="Siyuan Zhuang",
    author_email="suquark@gmail.com",
    description="Helper package for installing pickle5 wheels",
    url="https://github.com/suquark/pickle5-wheels-indices",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    license="Apache 2.0",
    cmdclass={"install": PostInstallCommand},
)

