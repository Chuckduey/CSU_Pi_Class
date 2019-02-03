#!/bin/sh
sudo eepromutils/eepflash.sh -r -t=24c32 -f=out.eep
hexdump -C out.eep
