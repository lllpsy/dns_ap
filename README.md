# dns_ap
# Lab 3 - DNS Application Layer

## **📌 Introduction**
This lab implements a **simplified DNS resolution system**, consisting of three main components:

1. **User Server (US)**:
   - Listens on **HTTP port 8080** to handle `/fibonacci` requests.
   - Queries the **Authoritative Server (AS)** for the IP of `fibonacci.com`.
   - Sends a request to the **Fibonacci Server (FS)** to compute Fibonacci numbers.

2. **Fibonacci Server (FS)**:
   - Listens on **HTTP port 9090** to compute Fibonacci numbers.
   - Registers `fibonacci.com` with the **Authoritative Server (AS)** via UDP.

3. **Authoritative Server (AS)**:
   - Listens on **UDP port 53533** to store and resolve the IP address of `fibonacci.com`.
   - Listens on **HTTP port 30001** to allow the User Server (US) to query for DNS records.

---

## **📌 Running the Application**
You can run the application using **Python**, **Docker**, or **Kubernetes**.

### **🐳 Method 2: Run with Docker**
#### **1. Build Docker images**
```bash
docker build -t as_image -f AS/Dockerfile .
docker build -t fs_image -f FS/Dockerfile .
docker build -t us_image -f US/Dockerfile .
```

#### **2. Create a Docker network**
```bash
docker network create dns_network .
```
#### **3. Run AS (Authoritative Server)**
```bash
docker run --network dns_network --name as -p 30001:30001 -p 53533:53533/udp as_image
```

#### **4. Run FS (Fibonacci Server)**
```bash
docker run --network dns_network --name fs -p 9090:9090 fs_image
```
#### **5. Run US (User Server)**
```bash
docker run --network dns_network --name us -p 8080:8080 us_image
```
#### **6. Test Docker setup**
```bash
curl "http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=as&as_port=30001"
```
If a Fibonacci number is returned, the setup is successful!

## **📌 Project Structure**
```php
dns_app/
│── US/                     # User Server
│   ├── us.py               # US server code
│   ├── Dockerfile          # Dockerfile for US
│── FS/                     # Fibonacci Server
│   ├── fs.py               # FS server code
│   ├── Dockerfile          # Dockerfile for FS
│── AS/                     # Authoritative Server
│   ├── as.py               # AS server code
│   ├── Dockerfile          # Dockerfile for AS
│── README.md               # Documentation
│── deploy_dns.yml          # Kubernetes deployment file (optional)
```
