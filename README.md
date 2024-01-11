# A wrapper for cdrdao that makes it easy to burn CDs.

Ever struggled through trying to use k3b or brasero? Probably not. They all use an outdated piece of software called wodim and it's very inconsistent on newer hardware.

This makes it easy to migrate any M3U tracklist and burn it onto a CD without the hassle of messing with wodim's SUID and weird ISRC errors (what even is an ISRC?)

## Usage

```bash
sudo apt install ffmpeg cdrdao python3
pip install -r requirements.txt
python3 shr4pnelburn.py -f <M3U playlist path> -d <device name (i.e /dev/sr0)>
```