#! /bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

from pirc522 import RFID
rdr = RFID()

def main():
    while True:
        rdr.wait_for_tag()
        (error, tag_type) = rdr.request()
        if not error:
            print("Tag detected")
            (error, uid) = rdr.anticoll()
            if not error:
                print("UID: " + str(uid))
    
                VIDEO_PATH = Path(str(uid[0])+"-"+str(uid[1])+"-"+str(uid[2])+"-"+str(uid[3]) + ".mkv")
    
                if VIDEO_PATH.is_file():
                    player = OMXPlayer(VIDEO_PATH, args='-o both')
                    sleep(player.duration())
    
                    if player.can_quit():
                        player.quit()
                else:
                    print (str(VIDEO_PATH) + " not found")


    # Calls GPIO cleanup
    rdr.cleanup()

if "__main__" == __name__:
    main()
