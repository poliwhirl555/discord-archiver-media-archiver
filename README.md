# Discord Archiver Media Archiver
Meant to be used in conjunction with [Discord Archiver](https://github.com/rroy676/Discord-Archiver/)

A simple script and command line tool to archive the Discord media from Discord CDN links in archived chats, along with options for archiving Tenor gifs in the chat, or replacing the embed Tenor view links with direct media links to make the chat look nicer.

All media sent through Discord uses Discord's CDN (Content Distribution Network) links, which have a built in expiry of around 24 hours when not used in the Discord app or website. Thus, any links archived will be inaccessible after that time period, meaning that your archived chats will lose all their media after 24 hours.

This script downloads and replaces all the CDN media links in the archive HTML file with a path to a locally saved version of the media, meaning even after the links expire you can still scroll through the chats and see all the photos, voice messages, and videos in all their glory.

Please run this tool either **immediately** after downloading the archive via [Discord Archiver](https://github.com/rroy676/Discord-Archiver/), or within approximately **24 hours** so that media can be saved without the links expiring.

## Installation

### As Python Package

Install from pip with the following command

```
python3 -m pip install discord-archiver-media-archiver
```

Can also be run as a python script via

```
python3 media_archiver.py "archive name"
```

### As executable (Windows Only)

- Go to [Releases](https://github.com/poliwhirl555/discord-archiver-media-archiver/releases) on Github and download the media_archiver.exe file

- Place the exe in the same folder as the html or file that you're trying to archive the links from.

- Double click and run the exe and follow the instructions.


## Usage

```
usage: media_archiver.py [-h] [-g] [-ndc] [-gl] [-r [REFRESH]] archive

positional arguments:
  archive               the Discord archive in the current working directory to archive media from

options:
  -h, --help            show this help message and exit
  -g, --gifs            enable the download and archival of gifs from Tenor while archiving
  -ndc, --no-discord-cdn
                        disable downloads from the Discord CDN servers (useful for if the CDN links are already expired or downloaded and you just
                        want to archive gifs)
  -gl, --gif-links      replace the gif embed links in the archive with the direct media links from Tenor (does not archive any media, overrides -g)
  -r, --refresh [REFRESH]
                        refresh the cdn links in the file with new ones. Uses the entered Discord auth token, or defaults to the environmental
                        variable DISCORD_TOKEN if none entered
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

## Python Library

Since this was written in Python, you can also import the package media_archiver in order to use the underlying methods behind the CLI tool in your Python scripts and programs.

The core methods are:
```python
def archive_media(archive_name: str, do_cdn : bool = True, do_gifs : bool = False, do_gif_links : bool = False, refresh_token : str = ""):
    """
    Archive all the media from a given html and replace all cdn web links in the html with local file paths.
        
    :param archive_name: name of archive file to replace and archive the media from
    :type archive_name: str
    :param do_cdn: whether to archive from Discord CDN Links (default True)
    :type do_cdn: bool
    :param do_gifs: whether to archive gifs from TENOR (default False)
    :type do_gifs: bool
    :param do_gif_links: whether to not archive gifs but just replace the gif embed links with true TENOR media links (default False, overrides do_gifs)
    :type do_gif_links: bool
    :param refresh_token: if provided, refresh Discord CDN links in the file using the provided Discord authentication token
    :type refresh_token: str
    """

def fetch_tenor_media_link(tenor_view_link : str)
# Convert from a Tenor view link to a Tenor direct media link

class CDN_Media(media_link: str, save_location: Path, fetch = True)
# Downloads media from media_link upon creation unless fetch is set to false, so be careful.
# Despite the name, does still work on gifs
```

## Note
If this package was of use to you, maybe leave a comment in Github Discussions, or a star or a watch, just so I know that someone got use out of something I made, since it's hard to tell otherwise. It's a nice feeling, to know that your efforts weren't wasted on just yourself.

## Changelog

### V 1.0.4
- Changed the Regex string for the Discord CDN URLs to be more robust and to capture other types such as the one used in the non-web app, although how useful that is, that is to be seen.

### V 2.0.0
- Added functionality to refresh links via [discord_cdn_link_refresher](https://github.com/poliwhirl555/discord-cdn-link-refresher)
- Added an interactive command line interface for a compiled exe version on Windows
