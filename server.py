from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil
import platform
import socket
import datetime

HOST = "0.0.0.0"
PORT = 8080

class SystemInfoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uptime_seconds = int(datetime.datetime.now().timestamp() - psutil.boot_time())
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))

        html = f"""
        <html>
            <head><title>Server Status</title></head>
            <body>
                <h1>🖥 Server Status Dashboard</h1>
                <p><strong>Hostname:</strong> {socket.gethostname()}</p>
                <p><strong>OS:</strong> {platform.system()} {platform.release()}</p>
                <p><strong>Uptime:</strong> {uptime_str}</p>
                <p><strong>CPU Usage:</strong> {psutil.cpu_percent(interval=1)}%</p>
                <p><strong>Memory Usage:</strong> {psutil.virtual_memory().percent}%</p>
                <p><strong>Disk Usage:</strong> {psutil.disk_usage('/').percent}%</p>
            </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

def run_server():
    print(f"Starting server on {HOST}:{PORT}... (Ctrl+C to stop)")
    server = HTTPServer((HOST, PORT), SystemInfoHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
