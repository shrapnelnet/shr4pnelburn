import sys
import os
from m3u_parser import M3uParser
import json
from halo import Halo
import glob
wodimInfo = dict()
print("""        __          _____                     __ __                     
.-----.|  |--.----.|  |  |.-----.-----.-----.|  |  |--.--.--.----.-----.
|__ --||     |   _||__    |  _  |     |  -__||  |  _  |  |  |   _|     |
|_____||__|__|__|     |__||   __|__|__|_____||__|_____|_____|__| |__|__|
                          |__|                   
                    yet another shrapnelnet production!
""")

def usage(err: str = "") -> None:
    print(f"{err}\nUsage:\n\tpython3 shr4pnelburn.py -f [brasero file] -d [device]")

def parseArgs() -> bool:
    args = sys.argv[1:]
    validFlags = {"-f", "-d"}
    flagsFound = []
    for n, arg in enumerate(args):
        # check if valid flag
        if arg in validFlags:
            flagsFound.append(arg)
            wodimInfo[arg] = args[n + 1]
    if not "-f" in flagsFound or not "-d" in flagsFound:
        return False
    return True

def parse() -> list[str]:
    songs = list()
    parser = M3uParser()
    try:
        parser = parser.parse_m3u(wodimInfo["-f"])
        streamsJSON = parser.get_json()
        streamsDict: list[dict] = json.loads(streamsJSON)
        for song in streamsDict:
            path = song.get("url")
            if not path:
                return []
            songs.append(path)
        return songs
    except FileNotFoundError:
        print("Specified M3U playlist was not found in this location.")
        return []

# https://web.archive.org/web/20240101234150/https://tldp.org/HOWTO/MP3-CD-Burning/dao-burning.html
# https://tldp.org/HOWTO/MP3-CD-Burning/dao-burning.html
def saveAsTOC(songs: list[str]):
    TOCDirPresent = os.path.exists("./tmp")
    if not TOCDirPresent:
        os.mkdir("./tmp")
    with open("./tmp/tracklist.toc", "w") as toc:
        toc.write("CD_DA\n\n")
        for n, song in enumerate(songs):
            toc.writelines(["TRACK AUDIO\n", f"AUDIOFILE \"{os.getcwd()}/tracks/{n}.wav\" 0", "\n\n"])
    print("TOC file written")

def convert(songs: list[str]):
    trackDirPresent = os.path.exists("./tracks")
    if not trackDirPresent:
        os.mkdir("tracks")
    with Halo("Converting to WAV", spinner="dots", placement="right", color="white"):
        for n, song in enumerate(songs):
            os.system(f"ffmpeg -y -i \"{song}\" -ar 44100 ./tracks/{n}.wav -loglevel warning")
    print("WAV conversion done")

def execute():
    print("Burning disk. Using cdrdao.")
    print(f"Parameters:\nM3U path: {wodimInfo['-f']}\nDevice: {wodimInfo['-d']}")
    cmd = f"cdrdao write --device {wodimInfo['-d']} --eject --driver generic-mmc:0x10 -v 2 -n ./tmp/tracklist.toc"
    print("Burning CD:")
    os.system(cmd)

def cleanup():
    os.remove(f"{os.getcwd()}/tmp/tracklist.toc")
    songsToRemove = glob.glob(f"{os.getcwd()}/tracks/*.wav")
    for path in songsToRemove:
        os.remove(path)
    print("Cleanup complete. Goodbye!")
        
def main() -> None:
    hasArgs = len(sys.argv) > 1
    if hasArgs is False:
        usage("No arguments were passed.")
        return
    success = parseArgs()
    if not success:
        usage("Illegal flag used.")
        return
    parsedSongs = parse()
    if (len(parsedSongs) == 0):
        usage()
        return
    saveAsTOC(parsedSongs)
    convert(parsedSongs)
    execute()
    cleanup()
        
if __name__ == "__main__":
    main()
