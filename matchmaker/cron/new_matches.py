from __future__ import print_function

import os.path, sys
parent = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(parent))

from matchmaker import db
from matchmaker.matches import MatchCreatorJob


if __name__ == "__main__":
    print(" Checking to see if we need new matches...")
    job = MatchCreatorJob(db)
    match = job.run()
    if match:
        print(" added match w/ GUID of {}".format(match))
    print(" done.")
