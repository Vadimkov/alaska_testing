import random
import socket
from subprocess import Popen
import time
import re


class Alaska:

    def __init__(self):
        self._port = str(self._get_random_port())
        self._url = "http://0.0.0.0:"
        self._bear_endpoint = "/bear"

    def get_port(self):
        return self._port

    def get_url(self):
        return self._url + self._port

    def get_default(self):
        return self.get_url() + self._bear_endpoint

    def _get_random_port(self):
        while True:
            port = random.randint(1000, 64000)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if s.connect_ex(("0.0.0.0", port)):
                return port


def run_alaska_service(port):
    filename = "alaska_test_logs_" + str(port) + ".log"
    logfile = open(filename, "w")
    p = Popen(["docker", "run", "-p", str(port) + ":8091",
               "--rm", "azshoo/alaska:1.0"], stdout=logfile)

    pattern = re.compile(".*Alaska - ========== ALASKA ==========")
    started = False
    while not started:
        file_for_read = open(filename, "r")
        logs = file_for_read.readlines()
        for line in logs:
            if pattern.match(line):
                started = True
                break
    return p
