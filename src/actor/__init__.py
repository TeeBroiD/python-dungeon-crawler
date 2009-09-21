import os
files = os.listdir(os.path.join('src','actor'))
for file in files:
    if file[-3:] == '.py' and file[:2] != '__':
        exec('from %s import *' % (file[:-3]))
