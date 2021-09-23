#!/usr/bin/env python

import lzma
import http.server
import os
import socketserver
import shutil

PORT = int(os.environ.get("PORT", 8000))
DIR = os.environ.get("DIR", "/data")
DISK_FILE = os.environ.get("DISK_FILE", "/data/disk.img")
DISK_DEV = os.environ.get("DISK_DEV", "/dev/vmdisk")
COPY_BUFSIZE = 64 * 1024

class XZHandler(http.server.SimpleHTTPRequestHandler):
    def copyfile(self, source, outputfile):
        length = COPY_BUFSIZE
        with lzma.open(outputfile, mode="wb", format=lzma.FORMAT_XZ) as outputxz:
            read = source.read
            write = outputxz.write
            while True:
                buf = read(length)
                if not buf:
                    break
                write(buf)

    def find_vm_disk(self):
        if os.path.exists(DISK_FILE):
            return open(DISK_FILE, "rb")
        elif os.path.exists(DISK_DEV):
            return open(DISK_DEV, "rb")
        else:
            raise Exception("Unable to find VM disk")

    def do_GET(self):
        f = self.find_vm_disk()
        try:
            self.send_response(http.server.HTTPStatus.OK)
            self.end_headers()
            self.copyfile(f, self.wfile)
        finally:
            f.close()

with socketserver.TCPServer(("", PORT), XZHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
