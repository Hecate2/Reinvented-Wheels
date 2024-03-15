import os
import logging
from logging import handlers
import http.server
from base64 import b64decode, b64encode

# Logging Setup
class Logger:
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


logger = Logger('logs.txt', level='debug').logger

class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):

    # Basic Auth Key ( !!Change Me!! -- admin/admin )
    username = 'admin'
    password = 'admin'
    key = b64encode(f'{username}:{password}'.encode()).decode()

    def do_HEAD(self):
        '''Send Headers'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        '''Send Basic Auth Headers'''
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        '''Handle GET Request'''
        try:
            if self.headers.get('Authorization') is None:
                # Send Auth Headers
                self.do_AUTHHEAD()
                logger.debug('Auth Header Not Found')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
            elif self.headers.get('Authorization') == 'Basic ' + self.key:
                # Successful Auth
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                # Bad Credentials Supplied
                self.do_AUTHHEAD()
                auth_header = self.headers.get('Authorization')
                # Log Bad Credentials
                if len(auth_header.split(' ')) > 1:
                    logger.debug(auth_header.split(' ')[1])
                    logger.debug(b64decode(auth_header.split(' ')[1]))
                logger.debug('Bad Creds')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
        except Exception:
            logger.error("Error in GET Functionality", exc_info=True)

    def date_time_string(self, time_fmt='%s'):
        return ''

    def log_message(self, format, *args):
        '''Requests Logging'''
        logger.debug(f"{self.client_address[0]} {args}")


if __name__ == '__main__':

    # Create Handler Instance
    handler = BasicAuthHandler

    # Spoof Server Header ( !!Change Me!! )
    handler.server_version = ' '
    handler.sys_version = ''

    # SimpleHTTPServer Setup
    bind_addr = '0.0.0.0'
    port = 80
    httpd = http.server.HTTPServer((bind_addr, port), handler)
    dir = '../results'
    try:
        if not os.path.isdir(dir):
            os.makedirs(dir)
        os.chdir(dir)
        logger.info(f"Serving at {bind_addr}:{port}")
        httpd.serve_forever()
    except Exception:
        logger.error("Fatal error in main loop", exc_info=True)