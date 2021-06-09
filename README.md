# IPInfo Scanner

This is the source code of IPInfo Scanner, the code is written mostly in Python3.+.

The project support running on Linux, Windows and Mac OS X.

## Setup

To configure the environment, add a `.env` in the root directory of your
project:

```
.
├── .env
└── ipinfo_scan.py
└── settings.py
└── utils.py
```

Install dependencies in virutal env:

```bash
> python3 -m venv env
> source env/bin/activate
(env)> pip install -r requirements.txt
```

## Usage

To run and scan a single ip:

```bash
(env)> python3 ipinfo_scan.py --ip 1.1.1.1
```

To run and scan multiple ip's (synchronous):

```bash
(env)> python3 ipinfo_scan.py --ips 1.1.1.1 2.2.2.2 8.8.8.8 9.9.9.9
```

To run and scan multiple ip's (asynchronous):

```bash
(env)> python3 ipinfo_scan.py --ips 1.1.1.1 2.2.2.2 8.8.8.8 9.9.9.9 --no-sync
```
