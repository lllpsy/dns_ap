from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

# 发送 UDP 消息到 AS
def register_to_as():
    as_ip = "as"  # AS 的 Docker 容器名称
    as_port = 53533
    hostname = "fibonacci.com"
    ip = "172.18.0.2"  # 斐波那契服务器 IP

    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.sendto(message.encode(), (as_ip, as_port))
    print(f"Registered {hostname} -> {ip}")

# Fibonacci 计算
def fibonacci(n):
    if n == 0: return 0
    elif n == 1: return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    if data:
        register_to_as()
        return jsonify({"message": "Registered"}), 201
    return jsonify({"error": "Invalid request"}), 400

@app.route("/fibonacci", methods=["GET"])
def compute_fibonacci():
    number = request.args.get("number")
    if not number.isdigit():
        return jsonify({"error": "Invalid number"}), 400
    result = fibonacci(int(number))
    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
