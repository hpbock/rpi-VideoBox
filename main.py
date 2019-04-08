#! /bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from random import randint

from pirc522 import RFID


def tryFindVideosIn(searchPath):
    files = []
    basepath = Path(searchPath)
    files_in_basepath = basepath.iterdir()
    for item in files_in_basepath:
        if item.is_file():
            files.append(item)
    return files


def main():
    rdr = RFID()
    while True:
        rdr.wait_for_tag()
        (error, tag_type) = rdr.request()
        if not error:
            print("Tag detected")
            (error, uid) = rdr.anticoll()
            if not error:
                print("UID: " + str(uid))
                uidString = "{:02x}-{:02x}-{:02x}-{:02x}".format(
                    uid[0], uid[1], uid[2], uid[3]
                )
                print("UID as string: " + uidString)

                videos = tryFindVideosIn(uidString)

                VIDEO_PATH = videos[randint(0, len(videos) - 1)]

                if VIDEO_PATH.is_file():
                    player = OMXPlayer(VIDEO_PATH, args="-o both")
                    sleep(player.duration())

                    if player.can_quit():
                        player.quit()
                else:
                    print(str(VIDEO_PATH) + " not found")

    # Calls GPIO cleanup
    rdr.cleanup()


if "__main__" == __name__:
    main()
