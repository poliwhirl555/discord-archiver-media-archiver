Meant to be used in conjunction with [Discord Archiver](https://github.com/rroy676/Discord-Archiver/)

A simple script and command line tool to archive the Discord media from Discord CDN links in archived chats, along with options for archiving Tenor gifs in the chat, or replacing the embed Tenor view links with direct media links to make the chat look nicer.

All media sent through Discord uses Discord's CDN (Content Distribution Network) links, which have a built in expiry of around 24 hours when not used in the Discord app or website. Thus, any links archived will be inaccessible after that time period, meaning that your archived chats will lose all their media after 24 hours.

This script downloads and replaces all the CDN media links in the archive HTML file with a path to a locally saved version of the media, meaning even after the links expire you can still scroll through the chats and see all the photos, voice messages, and videos in all their glory.

Please run this tool either **immediately** after downloading the archive via [Discord Archiver](https://github.com/rroy676/Discord-Archiver/), or within approximately **24 hours** so that media can be saved without the links expiring.

## Installation

Install from pip with the following command

```
pip install discord-archiver-media-archiver
```

Can also be run as a python script via

```
python3 media_archiver.py "archive name"
```


## Usage

```
usage: cdn_archiver.py [-h] [-g] [-ndc] [-gl] archive

positional arguments:
  archive               the Discord archive in the current working directory to archive media from

options:
  -h, --help            show this help message and exit
  -g, --gifs            enable the download and archival of gifs from Tenor or GIPHY while archiving
  -ndc, --no-discord-cdn
                        disable downloads from the Discord CDN servers (useful for if the CDN links are already expired or downloaded and you just want to archive gifs)
  -gl, --gif-links      replace the gif embed links in the archive with the direct media links from Tenor (does not archive any media, overrides -g)
```

## Examples
```
da-ma "archive_(350) Discord_2026-07-16.html"
```
Downloads all Discord CDN media in the archive file "archive_(350) Discord_2026-07-16.html", but ***not gifs***.

<br>

```
da-ma "archive_(350) Discord_2026-07-16.html" -g
```
Downloads all Discord CDN media in the archive file "archive_(350) Discord_2026-07-16.html" ***including gifs***.

<br>

```
da-ma "archive_(350) Discord_2026-07-16.html" -gl
```
Downloads all Discord CDN media in the archive file "archive_(350) Discord_2026-07-16.html" and replaces all Tenor gifs with their direct media link, but ***does not download them***.

<br>

```
da-ma "archive_(350) Discord_2026-07-16.html" -g -ndc
```
Downloads ***only the Tenor gifs*** from the archive file "archive_(350) Discord_2026-07-16.html".

## Python API

Since this was written in Python, you can also import the package media_archiver in order to use the underlying methods behind the CLI tool in your Python scripts and programs.

The core methods are:
```python
archive_media(archive_name: str, do_cdn = True, do_gifs = False, do_gif_links = False)

fetch_tenor_media_link(tenor_view_link : str)
# Convert from a Tenor view link to a Tenor direct media link

class CDN_Media(media_link: str, save_location: Path, fetch = True)
# Downloads media from media_link upon creation unless fetch is set to false, so be careful.
# Despite the name, does still work on gifs
```
