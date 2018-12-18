#!/usr/bin/python
from threading import Thread

from util import query_barcode_apis
from gui import Base, ScannerApp

app = ScannerApp()
root = Base()

if __name__ == '__main__':
    try:
        app.run()
        # while True:
            # query_barcode_apis(input("Scan the barcode: "))
        # query_barcode_apis(883929140886)  # Harry Potter 7.2 Blu-Ray
    except KeyboardInterrupt:
        pass
