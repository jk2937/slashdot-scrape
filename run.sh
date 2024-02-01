#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

echo "slashdot-scrape v0.0.2"

source venv/bin/activate
python3 scrape_rss.py
python3 zero_shot_analysis.py
deactivate
