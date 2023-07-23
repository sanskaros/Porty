import socket
import threading
from queue import Queue
from flask import Flask, render_template, request

app = Flask(__name__)

queue = Queue()
open_ports = []
thread_list = []
num_threads = 100  # Set the number of threads to use (adjust as needed)

def portscan(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout for the connection attempt (1 second)
            result = sock.connect_ex((target, port))
            return result == 0  # If the result is 0, the port is open; otherwise, it's closed or an error occurred
    except socket.error:
        return False

def mainmethod():
    while not queue.empty():
        port = queue.get()
        if portscan(target, port):
            open_ports.append(port)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global target
        target = request.form["target_ip"]
        port_list = range(1, 1025)  # Include port 1024 in the range
        fill_queue(port_list)

        for _ in range(num_threads):
            thread = threading.Thread(target=mainmethod)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        return render_template("result.html", open_ports=open_ports)

    return render_template("index.html")

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

if __name__ == "__main__":
    app.run(debug=True)
