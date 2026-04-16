#!/usr/bin/env python3

import sys
import time


def main():
    mib = int(sys.argv[1])
    size_bytes = mib * 1024 * 1024
    data = bytearray(size_bytes)

    # Touch one byte per page so RSS reflects the requested allocation.
    for i in range(0, size_bytes, 4096):
        data[i] = 1

    data[-1] = 1
    time.sleep(0.1)


if __name__ == "__main__":
    main()
