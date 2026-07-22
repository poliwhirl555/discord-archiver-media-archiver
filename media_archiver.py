import re
import requests
import html
import argparse
from pathlib import Path

class CDN_Media:
    """
    Class to represent a pair of Discord CDN media link and the associated saved image's path. 
    Upon use of the constructor, downloads the media via GET request and saves it to either the default location or provided location.
    """
    # Set to keep track of names and avoid duplicate names
    used_names = set()

    def __init__(self, media_link: str, save_location: Path, fetch = True):

        if fetch:
            print(media_link)
            r = requests.get(media_link, timeout= 30)
            if r.status_code == 404:
                print("content not found")

        
        self.link = media_link
        self.name = self.get_media_name(media_link)

        # Disambiguate the media name
        number_add = 1
        while self.name in CDN_Media.used_names:
            period = self.name.rfind(".")
            dash_number = re.compile(r"-\d+")
            dash_number_found = re.search(dash_number, self.name)

            if dash_number_found and len(dash_number_found.group()) > 0:
                dash = self.name.rfind(dash_number_found.group())
            else:
                dash = None

            if not dash:
                self.name = self.name[:period] + "-" + str(number_add) + self.name[period : ]
                number_add = number_add + 1
            else:
                number_add = int(dash_number_found.group()[1:]) + 1
                self.name = self.name[:dash] + "-" + str(number_add) + self.name[period : ]

        CDN_Media.used_names.add(self.name)
        self.path = save_location / self.name

        if fetch: 
            with open(self.path, "wb")  as file:
                file.write(r.content)

        # Need to change the path back in order to have the proper relative path for the html file once copied.
        self.path = Path(save_location.stem) / self.name


    def get_media_name(self, media_link):
        last_slash = media_link.rfind("/")
        question_mark = media_link.find("?")
        if not question_mark == -1:
            return media_link[last_slash + 1 : question_mark]
        else:
            return media_link[last_slash + 1 : ]

def fetch_tenor_media_link(tenor_view_link : str):
    r = requests.get(tenor_view_link, timeout = 30)

    media_link_pattern = re.compile(r"https?://media1.tenor.com/m\S+.gif")

    r.encoding = "utf-8"
    found = re.search(media_link_pattern, r.text)

    if found:
        return found.group()
    

def archive_media(archive_name: str, do_cdn = True, do_gifs = False, do_gif_links = False):
    compile_folder = Path(f"{archive_name[:-5]}") # Remove the .html from the end
    compile_folder.mkdir(exist_ok= True)
    media_folder = compile_folder / Path(f"media_{archive_name[:-5]}")
    media_folder.mkdir(exist_ok= True)
    destination = compile_folder / archive_name

    with open(archive_name, "r", encoding="utf-8") as file, open(destination, "w", encoding="utf-8") as out:
        already_loaded = {}
        cdn_link_pattern = re.compile(r"\"https://cdn.discordapp.com/[^\"]*\"")
        gif_link_pattern = re.compile(r"\"https?://tenor.com/view/[^\"]*\"")
        for line in file:

            line_urls = []
            is_gif = False

            if do_cdn:
                line_urls.extend(re.findall(cdn_link_pattern, line))
            
            if do_gifs or do_gif_links:
                tenor_links = re.findall(gif_link_pattern, line)
                if tenor_links:
                    is_gif = True
                    true_link = fetch_tenor_media_link(tenor_links[0][1:-1]) # Have to strip quotes from beginning and end
                    if true_link:
                        # Need to add back on the quotes, as it will try to strip the quotes later
                        line_urls.append(f"\"{true_link}\"") 

            out_line = line

            for link in line_urls:
                # Strip the quotes from beginning and end, and unescape the ampersands
                link = html.unescape(link[1:-1]) 

                loaded_media = already_loaded.get(link)
                if not loaded_media:
                    load = not (is_gif and do_gif_links) # Don't load if gif links flag is True and it is a gif, else default to loading
                    loaded_media = CDN_Media(link, media_folder, load)
                    already_loaded[link] = loaded_media
                
                if is_gif and not do_gif_links:
                    out_line = f"<div><img class=\"chatlog__attachment-img\" src=\"{str(loaded_media.path)}\" alt= \"{loaded_media.name}\" loading=\"lazy\"><br></div>"
                elif do_gif_links:
                    out_line = f"<div><img class=\"chatlog__attachment-img\" src=\"{link}\" alt= \"{loaded_media.name}\" loading=\"lazy\"><br></div>"
                else:
                    out_line = out_line.replace(html.escape(link), str(loaded_media.path))

            out.write(out_line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type = str, help = "the Discord archive in the current working directory to archive media from")
    parser.add_argument("-g", "--gifs", action = "store_true", default = False, help = "enable the download and archival of gifs from Tenor while archiving")
    parser.add_argument("-ndc", "--no-discord-cdn", action = "store_false", default = True, help = "disable downloads from the Discord CDN servers (useful for if the CDN links are already expired or downloaded and you just want to archive gifs)")
    parser.add_argument("-gl", "--gif-links", action = "store_true", default = False, help = "replace the gif embed links in the archive with the direct media links from Tenor (does not archive any media, overrides -g)")
    args = parser.parse_args()
    archive_media(args.archive, args.no_discord_cdn, args.gifs, args.gif_links)


if __name__ == "__main__":
    main()
