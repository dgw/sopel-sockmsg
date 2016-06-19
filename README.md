# sopel-sockmsg

Proof that it is possible to have a Sopel bot say text sent from outside IRC.

## Requirements

The script to send a message to the socket assumes the default IP and port, and assumes `/bin/bash` is
available. It should work on any *nix system, but it should be possible to do something similar on
Windows (pull requests welcome with e.g. a BAT file).

## Usage

* Put `sockmsg.py` in your Sopel bot's `modules` directory (and add `sockmsg` to `core.enable` if needed)
* Set `TARGET` variable as desired, e.g. `#mybot` or `nick,#channel`
* Put `sendsockmsg.sh` anywhere it's convenient, e.g. the current directory (`./`)
* (re)start Sopel
* Call e.g. `./sendsockmsg.sh test message through socket`

Alternatively, create a long-lived connection to the listening socket and send a line whenever you want
the module to post a message (terminated by `\n`).
