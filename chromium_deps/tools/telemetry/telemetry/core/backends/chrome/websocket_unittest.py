# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import base64
import BaseHTTPServer
import hashlib
import socket
import threading
import unittest


from telemetry.core.backends.chrome import websocket


# Minimal handler for a local websocket server.
class _FakeWebSocketHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    key = self.headers.getheader('Sec-WebSocket-Key')

    value = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    hashed = base64.encodestring(hashlib.sha1(value).digest()).strip().lower()

    self.send_response(101)

    self.send_header('Sec-Websocket-Accept', hashed)
    self.send_header('upgrade', 'websocket')
    self.send_header('connection', 'upgrade')
    self.end_headers()

    self.wfile.flush()


class TestWebSocket(unittest.TestCase):
  def testExports(self):
    self.assertNotEqual(websocket.create_connection, None)
    self.assertNotEqual(websocket.WebSocketException, None)
    self.assertNotEqual(websocket.WebSocketTimeoutException, None)

  def testSockOpts(self):
    httpd = BaseHTTPServer.HTTPServer(('', 0), _FakeWebSocketHandler)
    threading.Thread(target=httpd.handle_request).start()
    ws_url = 'ws://127.0.0.1:%d' % httpd.server_port
    ws = websocket.create_connection(ws_url)
    self.assertNotEquals(
        ws.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR), 0)

    threading.Thread(target=httpd.handle_request).start()
    ws = websocket.create_connection(
        ws_url,
        sockopt=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
    self.assertNotEquals(
        ws.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR), 0)
    self.assertNotEquals(
        ws.sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY), 0)
