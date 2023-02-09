# in the tests/test_module.py file
import sys
sys.path.append("..") # For local running
sys.path.append("/Users/julianotto/Documents/Projects/jules/gfunctions/animus/") # For PyCharm

from utils.prompt_utils import bulletpoint_str_to_list

if __name__ == "__main__":
    print(bulletpoint_str_to_list("- Hello\n- Hi\n- How are you?"))
