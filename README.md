# Serial HTTP Daemon

This provides an HTTP interface for a serial port.

## Build (Not really)

Download Python **3.10 or later** [here](https://www.python.org).

And install the dependencies with this command:

```shell
python3 install -r requirements.txt
```

### For Windows users

On Windows, we usually use `python`, instead of `python3`.

## Run

| Parameter       | Meaning                         | Default Value |
|:----------------|:--------------------------------|:--------------|
| `-p` `--port`   | Port of this HTTP daemon server | 50001         |
| `-d` `--device` | Path to the serial device       |               |

| Flag          | Meaning                                       |
|:--------------|:----------------------------------------------|
| `-h` `--help` | Show help information                         |
| `-m` `--mac`  | Treat device path as a serial number on macOS |

### Auto-detecting device

If the path to the serial device is not provided, follow the instructions,
and this program will guide you to find that device's path.

## Examples

### Quick start

```shell
./serial-http-daemon.py
```

### Runs on port 51145

```shell
./serial-http-daemon.py -p 51145
```

### For Windows users

On Windows, we must use `python serial-http-daemon.py` instead of `./serial-http-daemon.py`.
