import subprocess

print(subprocess.check_output('snap run grocy.access-change', shell=True))

