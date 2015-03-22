WebSocket Injection
=========
WebSocket 中转注入(for SQL Injection tools: sqlmap, etc.)

### Usage

    python main.py 8888
    python sqlmap.py -u "http://localhost:8888/?url=[target]&data=[sqli]" -p data

### License
MIT
