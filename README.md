# Chillr Bot

## Purpose

Chillr is specifically designed to respond to the needs of my Discord server, providing functionality that aligns with server management, community interaction, and more.


## Features

Chillr provide various functionalities to enhance server management and user interaction:

 - **Automatied Message Cleanup**: Message in specific channels are autmatically deleted after a set time.

 - **Counting System**: A counting game where users must increment the number correctly without sending consecutive messages.

The commands added in this code do not have permission checks. Discord allows you to add them in the server options under `Integration -> "Bot name"`

⚠ Some features are still in development and may experience bugs.


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

## Updating

To update the bot to its latest stable version, you can use the command below:

```bash
git pull origin main
```

Please note that using this command may overwrite the changes you have made, in this case it is recommended to copy the new version elsewhere and then add the changes one by one.



## Configuration 

Chillr Bot relies on YAML configurations files. Below is an example of how the structure should look:

`config.yaml`
```yaml
path:
  token: "path_to_token.txt"
  command: "path_to_command_folder"
  events: "path_to_events_folder"
```

`command_config.yaml`
```yaml
command:
  stop:
    channel_id:
      counting: x
      bot: x
      bot_staff: x
      log: x
  partnership:
    channel_id:
      partnership: x
  announcement:
    channel_id:
      announcement: x
```

`event_config.yaml`
```yaml
event:
  on_message:
    message_deletion:
      channel_id:
        bot: x
        bot_staff: x
        log: x
      sleep_time:
        bot: x
        bot_staff: x
        log: x
    counting:
      channel_id: x
      path: "path_to_count.json"
  on_ready:
    channel_id:
      bot: x
      bot_staff: x
      log: x
    counting:
      channel_id: x
      path: "path_to_count.json"
```


## Running the bot

To launch the bot on the server, run the following command:

```bash
nohup python3 ~/Chillr/Bot/main.py > Chillr.log 2>&1 &
```

This will start the bot and redirect its output to `Chillr.log`. To stop it, use the kill command with the PID, which can be obtained using:

```bash
ps aux | grep main.py
```

Once you have the PID, stop the bot by executing:

```bash
kill <PID>
```

## Modifying the code / Contributing

You are free to modify the bot's code to better suit your needs. Here's an overview of the project's structure and key imports:

 - `main.py`: Initializes the bot, loads commands and events.
 - `events/`: Contains events handlers such as `on_message.py`.
 - `config.yaml` & `event_config.yaml`: Store configuration values.

Key dependencies:

```python
import discord
from discord.ext import commands
import asyncio
import yaml
import json
import os
```

If you need to add new functionality, consider creating a new Cog inside the `commands/` or `events/` directory and load it in `main.py`.

---

Feel free to fork this repository and submit pull requests. Contributions and suggestions are always welcome !