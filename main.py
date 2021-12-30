import asyncio
import websockets
import requests
import json
import os
import time

current_log = open(os.path.join("logs", str(time.time())+".log"), "w+")


def log(message):
    current_log.write(f"{message}\n")
    current_log.flush()


psUrl = "ws://sim.smogon.com:8000/showdown/websocket"
psLoginUrl = "https://play.pokemonshowdown.com/action.php"
username = ""
password = ""


async def main():
    async with websockets.connect(psUrl) as ps:
        while True:
            received = await ps.recv()
            log(f"{received}")
            messages = received.split("\n")
            for message in messages:
                if (message):
                    if (message[0] == "|"):
                        parts = message.split("|")
                        if (parts[1] == "challstr"):
                            loginData = {"act": "login", "name": username,
                                         "pass": password, "challstr": "|".join(parts[2:])}
                            response = requests.post(
                                psLoginUrl, data=loginData).content.decode("utf-8")[1:]
                            await ps.send(f"|/trn {username},0,{json.loads(response)['assertion']}")
                            print("Logged in successfully!")


if __name__ == "__main__":
    asyncio.run(main())
