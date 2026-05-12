import os
import sys

if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
