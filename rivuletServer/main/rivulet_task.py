import os
import logging
import subprocess
from .models import UploadFile, Task


def process_tif(file_name, file_path, user_name, out_file, output_location, threshold, ssmiter, speed):
    # Call Rivulet module
    print("\n\nSTARTING PROCESS..." + user_name + "------>" + file_name + "\n\n")
    print(threshold + "+" + ssmiter + "+" + speed)

    processing_task = Task.objects.get(username=user_name, outfile_name=out_file, outfile_location=output_location)
    processing_task.status = "PROCESSING"
    processing_task.save()

    output_file = out_file
    INTERPRETER = "/usr/bin/python3.4"
    processor = "./rivuletpy/rivulet2"
    pargs = [INTERPRETER, processor]
    pargs.extend(["--file="+file_path])
    pargs.extend(["--threshold="+str(threshold)])
    pargs.extend(["--speed="+str(speed)])
    pargs.extend(["--outfile="+output_file])
    if speed == "ssm" and ssmiter != '':
        pargs.extend(["--ssmiter=" + str(ssmiter)])
        print("Using ssmiter!!")
    else:
        print("NOT using ssmiter!!")
    subprocess.Popen(pargs).communicate()

    if os.path.exists(output_location):
        task = Task.objects.get(username=user_name, outfile_name=out_file)
        task.status = "FINISHED"
        task.save()
    else:
        task = Task.objects.get(username=user_name, outfile_name=out_file)
        task.status = "FAILED"
        task.save()

    print("\n\nPROCESS DONE..." + user_name + "------>" + file_name + "\n\n")
    print("\nFILE IS-------->" + output_file)
    return '%s-------->%s' % (file_name, file_path)
