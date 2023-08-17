#!/usr/bin/env python3

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import configparser

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
    
config = configparser.ConfigParser()
config.read('config.ini')

ADDED_LATENCY = 0
RESPONSE = "a configurable response"

SERVER_PORT = int(config.get('General', 'SERVER_PORT'))
logging.info(f'PORT is {SERVER_PORT}')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get':
            try: 
                time.sleep(float(ADDED_LATENCY))
                
                start_time = time.time()
                
                logging.info(f'configurable response is {RESPONSE}')
                logging.info(f'added latency is {ADDED_LATENCY} seconds')
                
                data = {
                    "added_latency": ADDED_LATENCY,
                    "response": RESPONSE
                }
                
                response_data = json.dumps(data)
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                data["processing_time"] = processing_time
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                self.wfile.write(json.dumps(data).encode())
                
                logging.info(f'Request processing time: {processing_time:.6f} seconds')
                
            except Exception as e:
                logging.error(f'Error processing the GET request: {e}')
                self.send_error(500, b'Something went wrong with the request')
            

    def do_POST(self):
        global ADDED_LATENCY, RESPONSE

        if self.path == '/post':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_data = json.loads(post_data)
                
                logging.info("Received POST request with data: %s", post_data)

                if 'added_latency' in post_data:
                    try:
                        added_latency = float(post_data['added_latency'])
                        if added_latency < 0:
                            raise ValueError("'added_latency' must be a non-negative numeric value.")
                        ADDED_LATENCY = added_latency
                    except ValueError:
                        raise ValueError("'added_latency' must be a numeric value.")

                if 'response' in post_data:
                    RESPONSE = post_data['response']
                    logging.info("'response' set to %s", RESPONSE)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response_data = json.dumps({
                    "added_latency": ADDED_LATENCY,
                    "response": RESPONSE
                })
                
                self.wfile.write(response_data.encode())

                logging.info("POST request processed successfully.")

            except Exception as e:
                logging.error(f'Error processing the POST request: {e}')
                self.send_error(500, b'Something went wrong with the request')


if __name__ == '__main__':
    print('starting server on port: {}'.format(SERVER_PORT))
    httpd = HTTPServer(('', SERVER_PORT), Handler)
    print('running server...')
    httpd.serve_forever()
