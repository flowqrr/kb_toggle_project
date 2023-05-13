import os
import json
import psutil
import subprocess


def modify_kb_manager_value(settings_file):
    with open(settings_file, 'r') as f:
        data = json.load(f)
    if data['enabled']['Keyboard Manager']:
        data['enabled']['Keyboard Manager'] = False
    else:
        data['enabled']['Keyboard Manager'] = True
    with open(settings_file, 'w') as f:
        json.dump(data, f, indent=4)


settings_file = os.getenv('LOCALAPPDATA')
settings_file = os.path.join(settings_file, 'Microsoft', 'PowerToys', 'settings.json')

# check if readonly

if os.access(settings_file, os.W_OK):
    # modify file
    modify_kb_manager_value(settings_file)
    # set to readonly
    os.chmod(settings_file, os.stat(settings_file).st_mode & ~0o222)
else:
    # remove readonly property
    os.chmod(settings_file, os.stat(settings_file).st_mode | 0o222)
    # modify file
    modify_kb_manager_value(settings_file)
    # set back to readonly
    os.chmod(settings_file, os.stat(settings_file).st_mode & ~0o222)

os.system("taskkill /F /IM PowerToys.exe")
args = ["C:\Program Files\PowerToys\PowerToys.exe", "-r"]
subprocess.Popen(args)
