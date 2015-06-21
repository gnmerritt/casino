import sys


def fix_paths():
    """Hack to set up PYTHONPATH"""
    #poker_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    #sys.path.append(poker_dir)
    sys.path.append("/Users/nathan/sources/casino/poker/")
