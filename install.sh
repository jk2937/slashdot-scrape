#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

sudo apt -y update 
sudo apt -y upgrade

sudo apt install python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

python3 -m pip install torch transformers

deactivate
