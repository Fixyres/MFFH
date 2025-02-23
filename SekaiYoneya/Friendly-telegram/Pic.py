# @Sekai_Yoneya

from .. import loader
from random import choice as Yoneya


def register(cb):
 cb(PicPhotosMod())

class PicPhotosMod(loader.Module):
 """Фотографии из @pic."""
 strings = {'name': 'Pic'}

 async def gowcmd(self, event):
  await event.edit('<b>Бог Войны!</b>')
  reslt=await event.client.inline_query('pic',Yoneya(['Кратос убил Зевса']))
  await reslt[reslt.index(Yoneya(reslt))].click(event.to_id)
