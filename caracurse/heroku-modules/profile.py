# Name: Profile
# Description: Module for changing profile data.
# Author: @sansaramods
# Commands:
# .name | .about | .user
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/exodiast
#-----------------------------------------------------------------------------------
# meta developer: @sansaramods
#-----------------------------------------------------------------------------------

__version__ = (1, 1, 1 )

import logging
from telethon.errors.rpcerrorlist import UsernameOccupiedError 
from telethon.tl.functions.account import (
 UpdateProfileRequest, 
 UpdateStatusRequest, 
 UpdateUsernameRequest)
from .. import loader, utils

logger = logging.getLogger(__name__)

def register(cb):
    cb(ProfileEditorMod())

@loader.tds
class ProfileEditorMod(loader.Module):
    """This module can change your Telegram profile."""
 
    async def namecmd(self, message):
        """- for change your first/second name. """
        args = utils.get_args_raw(message).split("/")
        
        if len(args) == 0:
            return await message.edit("Incorrect format of args. Try again.")
        if len(args) == 1:
            firstname = args[0]
            lastname = " "
        elif len(args) == 2:
            firstname = args[0]
            lastname = args[1]
        await message.client(UpdateProfileRequest(first_name=firstname, last_name=lastname))
        await message.edit("The new name was successfully unstalled!")
    
    async def aboutcmd(self, message):
        """- for change your bio. """
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Incorrect format of args. Try again.")
        await message.client(UpdateProfileRequest(about = args))
        await message.edit("The new bio was successfully unstaled!")

    async def usercmd(self, message):
        """- for change your username. Enter value without "@". """
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Incorrect format of args. Try again.")
        try:
            await message.client(UpdateUsernameRequest(args))
            await message.edit("The new username was succesfully installed!")
        except UsernameOccupiedError:
            await message.edit("The new username is already occupied!")
    

