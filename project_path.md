# path step by step for this project

## detect os version

```bash
Debian 12.8 
```

## detect python version


```bash
python3 --version
Python 3.11.2
```


## create venv

[install venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv .venv
```

## enter .venv

```bash
source .venv//bin/activate
```

## exit/leave venv

```bash
deactivate
```

## install packages - command  inside .venv

```bash
pip3 install ib_insync
```

## show what is already installed inside .venv - command inside .venv

```bash
pip3 list
```


> [!NOTE]
> I want the readers to read it carefully as it contains many important docs.


https://stackoverflow.com/questions/17115664/can-linux-cat-command-be-used-for-writing-text-to-file

## first tws connect

```python
from ib_insync import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)
```