# Chillr Bot

## Features

Some features are still under development


## Purpose

Chillr is specifically designed to respond to the needs of my Discord server, providing functionality that aligns with server management, community interaction, and more.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/Ju2H3brc0t/Chillr.git
cd Chillr
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt`
```

## Running the bot

To launch the bot on the server, run the following command:

```bash
nohup python3 ~/Chillr/Bot/main.py > Chillr.log 2>&1 &
```

This will start the bot and redirect its output to `Chillr.log`. To stop it, use the kill command with the PID, which can be obtained using:

```bash
ps aux | grep Chillr.py
```

Once you have the PID, stop the bot by executing:

```bash
kill <PID>
```

## Contributing

Feel free to fork this repository and submit pull request. Contributions and suggestions are always welcome !

---

Let me know if you want any adjustements on the content !