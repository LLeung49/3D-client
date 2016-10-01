import os
import logging
import subprocess
from .models import UploadFile, Task


def process_tif(file_name, file_path, user_name, out_file):
    # Call Rivulet module
    print("\n\nSTARTING PROCESS..." + user_name + "------>" + file_name + "\n\n")
    output_file = out_file
    INTERPRETER = "/usr/bin/python3.4"
    processor = "./rivuletpy/rivulet2"
    pargs = [INTERPRETER, processor]
    pargs.extend(["--file="+file_path])
    pargs.extend(["--threshold=0"])
    pargs.extend(["--speed=dt"])
    pargs.extend(["--outfile="+output_file])
    subprocess.Popen(pargs).communicate()

    print("\n\nPROCESS DONE..." + user_name + "------>" + file_name + "\n\n")
    print("\nFILE IS-------->" + output_file)
    return '%s-------->%s' % (file_name, file_path)
