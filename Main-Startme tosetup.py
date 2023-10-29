from typing import Iterable, Tuple

import cursor as cursor
from getkey import getkey, keys

from tqdm import tqdm
import requests


def clear() -> None:
    """Clear the terminal."""
    print("\033[H\033[2J", end="", flush=True)


def menu(prompt: str, options: Iterable[str]) -> Tuple[int, str]:
    cursor.hide()

    selectedOption = 0
    key = None

    while key != keys.ENTER:
        clear()
        print(prompt)
        for i in range(len(options)):
            option = f" {i + 1}. {options[i]}"
            print(f">{option}" if i == selectedOption else f" {option}")

        key = getkey()
        if key in {keys.UP, keys.W}:
            selectedOption = len(options) - 1 if selectedOption == 0 else selectedOption - 1
        elif key in {keys.DOWN, keys.S}:
            selectedOption = 0 if selectedOption == len(options) - 1 else selectedOption + 1
        elif key.isdigit() and int(key) <= len(options) and int(key) > 0:
            selectedOption = int(key) - 1

    for i in range(len(options)):
        if i == selectedOption:
            cursor.show()
            return i, options[i]

hosturl = menu("host video (W/S/Arrow_up/Arrow_down)", ["cdn2.cdn9x.com", "enter url"])[1]
if hosturl == "enter url":
    hosturl = input("url and add protocal; ")
videouid = menu("videoid (W/S/Arrow_up/Arrow_down)", ["abb7q4m", "enter id"])[1]
if videouid == "enter id":
    videouid = input("id; ")
quality = menu("quality (make sure you like support that quality) (W/S/Arrow_up/Arrow_down)", ["360p", "720p", "1080p"])[1]
pageend = input("page end at: ")


with open("Fill.ts", "wb") as handle:
    # Define the range of IDs you want
    start_id = 0
    end_id = int(pageend)
    # Determine the number of digits for the IDs
    num_digits = 3
    host = hosturl
    protocelal = "https://"
    movieid = videouid
    qan = quality

    # Loop to generate and format the IDs
    for i in range(start_id, end_id + 1):
        formatted_id = f"{i:03d}"
        response = requests.get(f"{protocelal}{host}/{movieid}/{qan}_{formatted_id}.ts", stream=True)
        #print(response.url)
        nowload = 0
        max = 0
        maxreq = []
        for data in response.iter_content():
            max += 1
            maxreq.insert(len(maxreq), data)
        #print(max)

        for data in maxreq:
            nowload += 1
            if nowload > 0 and max > 0 :
                s = int(( nowload * 100 ) / max)
                print("Download as " + str(s) + " / 100 - " + formatted_id)
            handle.write(data)
            print(formatted_id)