#!/usr/bin/env bash

#eval "python3 /root/scripts/main.py"
eval "python3 /py/main.py"

echo -e "\n[  INFO  ] Giving permissions..."
eval "chmod -R ugo+rw /output/"
#eval "chown -R ssilvari /output/"