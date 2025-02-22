
import logging
import tempfile

from typing import Tuple

from telethon.types import Message
from .. import loader, utils

from pytubefix import YouTube
# from pytubefix.helpers import install_proxy
from pytubefix.exceptions import BotDetection, RegexMatchError


"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    YoutubeDL
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: https://0x0.st/s/h111E8AonLcGdpV5N8rx6A/XWiz.jpg
# meta desc: Download youtube videos
# meta developer: @BruhHikkaModules

# requires: pytubefix

logger = logging.getLogger("YoutubeDL-BETA")
__version__ = (1, 0, 6)


# It is necessary for auto update of the library, because it is frequently updated (for now, deprecated, not needed)
# async def update_lib():

#     process = await asyncio.create_subprocess_shell(
#         'pip install -U "pafy""',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     return True


# async def check_ffmpeg():
#     ffmpeg = await asyncio.create_subprocess_shell(
#         'ffmpeg',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     ffprobe = await asyncio.create_subprocess_shell(
#         'ffprobe',
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )

#     status = {
#         "ffmpeg": ffmpeg.returncode != 127,
#         "ffprobe": ffprobe.returncode != 127
#     }

#     return status


@loader.tds
class YoutubeDLB(loader.Module):
    """THIS IS A BETA! BUGS MAY OCCUR!"""

    strings = {"name": "YoutubeDLB"}

    # todo: token support (PoToken), inline cancel button
    # auto generator, manually

    def __init__(self):
        self.config = loader.ModuleConfig(
            # loader.ConfigValue(
            #     "proxy_url",
            #     "http://127.0.0.1:8080",
            #     lambda: "You can use proxy for download videos (maybe you can also use socks5)"
            # ),
            # loader.ConfigValue(
            #     "proxy_enabled",
            #     False,
            #     lambda: "Proxy status",
            #     validator=loader.validators.Boolean()
            # ),
            loader.ConfigValue(
                "visitor_data",
                "CgtJMmJMRmJHQmVPdyjI2La7BjIKCgJSVRIEGgAgKA%3D%3D",
                lambda: "Visitor data to bypass bot protection from youtube (default data is invalid)"
            ),
            loader.ConfigValue(
                "po_token",
                "MnTtI005pJJQcu0bsVebvAKOcv6j6D46uKF_IUhRD4b62U6s6w9P_QX42G4LIITz-m6nE1u0yf9XD_7oJggQetqbzeftkhqcsS-Cs7UJCoRxuF9gZItXnSf-MUKCNmHJEHSkaTdKpkVNX06xVup89P3n87mQ2Q==",
                lambda: "Visitor data to bypass bot protection from youtube (default data is invalid)"
            ),
            loader.ConfigValue(
                "bypass_botprotector",
                False,
                lambda: "Allows bypassing bot verification with PoToken and Visitor Data",
                validator=loader.validators.Boolean()
            )
        )

    def get_potoken(self) -> Tuple[str, str]:
        visitor_data = self.config["visitor_data"]
        po_token = self.config["po_token"]
        return visitor_data, po_token

    @loader.command()
    async def videodl(self, message: Message):
        """[link] - Download video"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(
                message,
                "no arguments, use this link for example: https://www.youtube.com/watch?v=RM4Ue8Xy55c",
            )

        else:
            try:
                # if self.config['proxy_enabled']:
                #     protocol = self.config['proxy_url'].split('://')[0]

                #     # proxies = {
                #     #     protocol: self.config['proxy_url']
                #     # }

                #     proxies = {
                #         'http': 'http://127.0.0.1:8080',
                #         'https': 'https://127.0.0.1:8080'
                #     }
                #     logger.info(proxies)

                #     youtube = YouTube(args, proxies=proxies)
                #     logger.info('proxy')

                if self.config['bypass_botprotector']:
                    youtube = YouTube(
                        args,
                        use_po_token=True,
                        po_token_verifier=self.get_potoken()
                    ) 
                    logger.info('bypass')

                # elif self.config['bypass_botprotector'] and self.config['proxy_enabled']:
                #     youtube = YouTube(
                #         args,
                #         use_po_token=True,
                #         po_token_verifier=self.get_potoken(),
                #         proxies=self.proxies
                #     ) 
                #     logger.info('proxy + bypass')
                else:
                    youtube = YouTube(args)
                    logger.info("else")

                await utils.answer(message, "Please, wait.")

                with tempfile.TemporaryDirectory() as path:
                    stream = await utils.run_sync(youtube.streams.get_highest_resolution)

                    try:
                        await utils.run_sync(stream.download, path, "/video.mp4")
                    except BotDetection:
                        await utils.answer(
                            message,
                            "Youtube recognize in you bot, so, try use PoToken, if you already use it, I cant do anything. Try use proxy, or change ip, idk",
                        )

                    await utils.answer_file(message, path + "/video.mp4")
            except RegexMatchError:
                await utils.answer(
                    message, "Hmm, I don't think that link is quite right. \nDouble-check it."
                )

    @loader.command()
    async def potoken(self, message: Message):
        await utils.answer(
            message,
            ("Go to terminator.aeza.net, select Debian, paste this in terminal:"
            "\n"
            "\n<code>apt update -y; apt install docker.io -y; docker run -p 8080:8080 quay.io/invidious/youtube-trusted-session-generator:webserver</code>"
            "\nAfter, copy the values from the JSON, paste in the corresponding values in the config."
            '\n({ “updated”: 1735240777, “potoken”: “MnTtI005pJJJQcu0bsVebvAKOcv6j6D46uKF_IUhRD4b62U6s6w9P_QX42G4LIITz-m6nE1u0yf9XD_7oJggQetqbzeftkhqcsS-Cs7UJCoRxuF9gZItXnSf-MUKCNmHJEHSkaTdKpkVNX06xVup89P3n87mQ2Q==”, ‘visitor_data’: “CgtJMmJMRmJHQmVPdyjI2La7BjIKCgJSVRIEGgAgKA%3D%3D"} take potoken and visitor_data)'
            "\n"
            "\nData and token are valid for 5-10 minutes, after that they won't work and need to be recreated.")
        )
            
            
