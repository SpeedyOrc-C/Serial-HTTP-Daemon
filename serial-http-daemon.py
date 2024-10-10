#! python3

import argparse
from http import HTTPStatus
import http.server
import serial
import urllib


def server_main(port: int, device: str) -> None:
    serial_connection = serial.Serial(device)

    class Handler(http.server.BaseHTTPRequestHandler):

        def add_default_header(self):
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

        def serial_send(self, data: bytes) -> None:
            written_len = serial_connection.write(data)

            self.send_response(HTTPStatus.OK)
            self.add_default_header()
            self.wfile.write(str(written_len).encode('utf-8'))

        def serial_read(self, size: int):
            data = serial_connection.read(size)

            self.send_response(HTTPStatus.OK)
            self.add_default_header()
            self.wfile.write(data)

        def not_found(self):
            self.send_response(HTTPStatus.NOT_FOUND)
            self.add_default_header()

        def bad_request(self, message: str = ""):
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.add_default_header()
            self.wfile.write(message.encode("utf-8"))

        def do_GET(self):
            url = urllib.parse.urlparse(self.path)
            query = url.query
            params = urllib.parse.parse_qs(query)

            match url.path:
                case "/send":
                    try:
                        data = params["data"][0].encode("utf-8")
                    except:
                        self.bad_request("Missing parameter `data`, the message to be send.")
                        return

                    self.serial_send(data)

                case "/read":
                    try:
                        raw_size = params["size"][0]
                    except:
                        self.bad_request("Missing parameter `size`, the size of data to be read.")
                        return

                    try:
                        size = int(raw_size)
                    except:
                        self.bad_request("Parameter `size` is not a number.")
                        return

                    self.serial_read(size)

                case _:
                    self.not_found()

    server = http.server.HTTPServer(("", port), Handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        serial_connection.close()


def apple_device(device_id: str) -> str:
    return f"/dev/cu.usbmodem{device_id}"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="serial-http-daemon",
        description="HTTP wrapper over serial port.")

    parser.add_argument("-p", "--port", default=50001, type=int,
                        help="Port of this HTTP daemon server")

    parser.add_argument("-d", "--device",
                        help="Path to the serial device")

    parser.add_argument("-m", "--mac", action="store_true",
                        help="Add the prefix `/dev/cu.usbmodem` for device path in macOS.")

    args = parser.parse_args()

    if args.port is None or args.device is None:
        parser.print_help()
        return 1

    port = args.port

    if args.mac:
        device = apple_device(args.device)
    else:
        device = args.device

    server_main(port, device)

    return 0


if __name__ == "__main__":
    exit(main())
