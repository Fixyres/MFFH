# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


from telethon import types
import rsa
import aioboto3
from .. import loader, utils  # type: ignore


@loader.tds
class S3Mod(loader.Module):
    """S3 file manager"""

    strings = {"name": "S3 file manager", "pref": "<b>[S3]</b> {}"}

    async def client_ready(self, client, db):
        self._db = db
        self._db_name = "S3"

    async def set_auth_data(
        self, endpoint: str, region: str, username: str, password: str, bucket: str
    ) -> None:
        self._db.set(self._db_name, "endpoint", endpoint)
        self._db.set(self._db_name, "region", region)
        self._db.set(self._db_name, "username", username)
        self._db.set(self._db_name, "password", password)
        self._db.set(self._db_name, "bucket", bucket)

    async def get_client(self) -> aioboto3.Session.client:
        session = aioboto3.Session(
            aws_access_key_id=self._db.get(self._db_name, "username"),
            aws_secret_access_key=self._db.get(self._db_name, "password"),
            region_name=self._db.get(self._db_name, "region"),
        )
        return session.client(
            service_name="s3",
            endpoint_url=f"https://{self._db.get(self._db_name, 'endpoint')}",
        )

    @loader.owner
    async def s3upcmd(self, m: types.Message):
        reply = await m.get_reply_message()
        if not reply or not reply.document:
            return await utils.answer(m, self.strings("s3").format("Reply to a document"))
        session = await self.generate_session()
        client = await self.get_client()
        async with client as s3:
            await s3.upload_fileobj(
                await bot.download_file_by_id(video.file_id),
                os.getenv("S3_BUCKET_NAME"),
                video_s3_path,
            )
        
    # @loader.owner
    # async def s3authcmd(self, m: types.Message):
    #     pass
