#!/bin/bash

#set -x

# Reset dummynet to default config
sudo dnctl -f -q flush
sudo pfctl -f /etc/pf.conf

bw="$1"
delay="$2"
plr="$3"

# Compose an addendum to the default config: creates a new anchor
(cat /etc/pf.conf &&
  echo 'dummynet-anchor "project_anchor"' &&
  echo 'anchor "project_anchor"') | pfctl -q -f -

# Configure the new anchor
cat <<EOF | pfctl -q -a project_anchor -f -
no dummynet quick on lo0 all
dummynet out proto tcp from any to any port 1:65535 user 501 pipe 1
dummynet in proto tcp from any to any port 1:65535 user 501 pipe 1
EOF

# Create the dummynet queue
sudo dnctl pipe 1 config bw "${bw}Mbit/s" delay "${delay}" plr "${plr} noerror"
echo dnctl pipe 1 config bw "${bw}Mbit/s" delay "${delay}" plr "${plr} noerror"

# Activate PF
sudo pfctl -E

# to check that dnctl is properly configured: 
sudo dnctl list
exit 0
