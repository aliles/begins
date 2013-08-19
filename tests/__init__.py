from __future__ import absolute_import, division, print_function

import logging
import sys

if sys.version_info[:2] < (2, 7):
    logging.raiseExceptions = 0
