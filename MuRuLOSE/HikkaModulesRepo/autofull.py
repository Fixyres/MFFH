# I'm too lazy to update full.txt every time, so automation

import glob


modules = glob.glob("*.py")
modules.remove("!example.py")
modules.remove("autofull.py")

mods = '\n'.join(modules).replace('.py','')

with open('full.txt', 'w') as f:
    f.write(mods)
