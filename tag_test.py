import subprocess
import shlex

cmd = 'git describe --tags'
cmd_array = shlex.split(cmd)
out = subprocess.run(cmd_array)
print(out.returncode)
