from flask import Flask, request, jsonify
import socket

app = Flask(__name__)
dns_records = {}  # 存储 DNS 解析信息

# 监听注册请求（UDP）
def listen_udp():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", 53533))

    while True:
        data, addr = udp_sock.recvfrom(1024)
        message = data.decode().strip().split("\n")
        if len(message) == 4 and message[0] == "TYPE=A":
            name = message[1].split("=")[1]
            ip = message[2].split("=")[1]
            dns_records[name] = ip
            print(f"Registered {name} -> {ip}")

# 监听 DNS 查询（HTTP）
@app.route("/dns-query", methods=["GET"])
def query_dns():
    name = request.args.get("name")
    if name in dns_records:
        return jsonify({"hostname": name, "ip": dns_records[name]}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    import threading
    threading.Thread(target=listen_udp, daemon=True).start()
    app.run(host="0.0.0.0", port=30001)
