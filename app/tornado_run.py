import sys
import os

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload

if __name__ == '__main__':

    from app import app

    tornado.options.options['log_file_prefix'].set('/opt/logs/my_app.log')
    tornado.options.parse_command_line()

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"

    cert = current_folder + "ssl/yychub.csr"
    key = current_folder + "ssl/yychub.key"

    http_server = HTTPServer(WSGIContainer(app), ssl_options={"certfile": cert,
                                                              "keyfile": key})

    http_server.listen(443)
    IOLoop.instance().start()