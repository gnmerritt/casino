import os.path, sys
parent = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(parent))

from matchmaker import db
from matchmaker.skill import SkillUpdater


if __name__ == "__main__":
    SkillUpdater().run(db)
