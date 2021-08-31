import numpy as np
from Preliminaries import *
from FA import *
from Algorithms import *
from UI import *
from Tests import *


def main(test=False):
    if test:
        run_tests()
    else:
        app_startup()


if __name__ == "__main__":
    main()
