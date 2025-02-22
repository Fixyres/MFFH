#Name: Profile
#Description: Module for changing profile data.
#Author: @nervousmods
# Commands:
# .name | .about | .user
#     _  __     ____    __    __  ________    ____       __  __
#    | |/ /    / /\ \   \ \  / / |__    __|  /_/\ \     /  \/  \
#    |   /    / /__\ \   \ \/ /     |  |        / /    / /\__/\ \
#    |   \   / /____\ \   |  |      |  |     _  \ \   / /      \ \
#    |_|\_\ /_/      \_\  |__|      |__|     \_\/_/  /_/        \_\
#    
#
#
#     🔐  Licenced under the GNU AGPLv3
#                        https://www.gnu.org/licenses/aplg-3.0.html
#meta developer: @nervousmods
#scope: hikka_only 
#scope: hikka_min 1.4.2

__version__ = (0, 1, 1 )

import logging
import os 
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

    strings = {
        "name": "Profile",
        "author": "smlgwy"
        }
   
    
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
    
