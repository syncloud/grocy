import subprocess

print(subprocess.check_output('snap run grocy.storage-change', shell=True))
