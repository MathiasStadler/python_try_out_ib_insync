```python
cat > workspace/first_connect_tws.py << EOF
from ib_insync import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12)

# python3 workspace/first_connect_tws.py 
EOF
```