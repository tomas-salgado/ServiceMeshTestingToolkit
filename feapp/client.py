#!/usr/bin/env python3

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import logging
import json
import configparser

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')

HOST = config.get('General', 'HOST')
HOST_PORT = config.get('General', 'HOST_PORT')
if ":" not in HOST:
    HOST += ":" + HOST_PORT
logging.info(f'HOST is {HOST}')

CLIENT_PORT = int(config.get('General', 'CLIENT_PORT'))
logging.info(f'CLIENT_PORT is {CLIENT_PORT}')

TRAFFIC = 1

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global TRAFFIC
        
        if self.path == '/ping':
            self.send_response(200)
            self.end_headers()
            return
        
        if self.path == '/testing':
            try:
                for i in range(TRAFFIC):
                    start_time = time.time()
                    logging.info(f'Start time: {start_time}')
                    req = Request(f'http://{HOST}/get')
                    res = urlopen(req)
                    
                    end_time = time.time()
                    rtt = end_time-start_time
                    
                    response_data = res.read()
                    response_data = json.loads(response_data)
                    response_data["traffic"] = TRAFFIC
                    response_data["RTT"] = rtt
                    
                    added_latency = response_data["added_latency"]
                    response = response_data["response"]
                    
                    logging.info(f'RTT: {rtt}')
                    logging.info(f'Added latency: {added_latency}')
                    logging.info(f'Response: {response}')
                    logging.info(f'Traffic: {TRAFFIC}')
                    
                    response_data = json.dumps(response_data)
                                
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response_data.encode())

            except HTTPError as e:
                print(f'[ERROR] {e}')
                self.send_error(e.code, e.reason)

            except Exception as e:
                print(f'[ERROR] {e}')
                self.send_error(500, b'Something bad happened')
    
    def do_POST(self):
        global TRAFFIC
        
        if self.path == '/testing':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_data = json.loads(post_data)
                
                logging.info("Received POST request with data: %s", post_data)

                if 'traffic' in post_data:
                    try:
                        TRAFFIC = int(post_data['traffic'])
                    except ValueError:
                        raise ValueError("'traffic' must be an int")
                    
                post_data = json.dumps(post_data)
                
                req = Request(f'http://{HOST}/post', post_data.encode(), method='POST')
                res = urlopen(req)

                response_data = res.read()
                response_data = json.loads(response_data)
                response_data["traffic"] = TRAFFIC
                response_data = json.dumps(response_data)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data.encode())
                
                logging.info("POST request successful.")

            except HTTPError as e:
                logging.error(f'Error processing the POST request: {e}')
                self.send_error(e.code, e.reason)

            except Exception as e:
                logging.error(f'Error processing the POST request: {e}')
                self.send_error(500, b'Something bad happened')
                

if __name__ == '__main__':
    print('starting client at port: {}'.format(CLIENT_PORT))
    httpd = HTTPServer(('', CLIENT_PORT), Handler) 
    print('running client...')
    httpd.serve_forever()