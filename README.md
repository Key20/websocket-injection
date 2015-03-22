WebSocket Injection
=========
WebSocket 中转注入(for SQL Injection tools: sqlmap, etc.)

### Installation

    git clone https://github.com/RicterZ/websocket-injection
    cd websocket-injection
    pip install -r requirements.txt

### Usage

    python main.py --port=8888
    python sqlmap.py -u "http://localhost:8888/?url=[target]&data=[sqli]" -p data

![](https://github.com/RicterZ/websocket-injection/raw/master/usage.png)

### License
MIT
