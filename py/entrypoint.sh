#!/usr/bin/env bash

#eval "python3 /root/scripts/main.py"
#eval "python3 /py/main.py"
eval "ls /data"
eval "python3 /py/register_mri_to_mni152.py"

echo -e "\n[  INFO  ] Giving permissions..."
eval "chmod -R ugo+rw /output/"
#eval "chown -R ssilvari /output/"