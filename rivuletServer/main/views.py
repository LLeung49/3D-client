from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from .forms import UploadFileForm
from .models import UploadFile, Task
from django.template import loader
import os
import logging
import subprocess
from django.contrib import messages
from django_q.humanhash import humanize
from django_q.tasks import async, result
import time
from datetime import datetime
from pytz import timezone
import zipfile
from io import BytesIO
import json
from login.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


# def order(request):
#     fruit = request.POST.get('fruit_type', '')
#     num_fruit = int(request.POST.get('num_fruit', '1'))
#     task_id = async('main.tasks.order_fruit', fruit=fruit, num_fruit=num_fruit)  # Create async task
#     print("==========================\n", fruit)
#     print("==========================\n", num_fruit)
#     # ret2 = result(task_id, 10000)  # block and wait for 200 ms
#     # print("==========================\n", ret2)
#
#     messages.info(  # Django message as notification
#         request,
#         'You ordered {fruit:s} x {num_fruit:d} (task: {task})'
#         .format(fruit=fruit, num_fruit=num_fruit, task=humanize(task_id))
#     )
#     return render(request, 'main/message.html')


def new_task(request):
    if request.method == 'GET' and request.user.is_authenticated():
        all_files = UploadFile.objects.filter(username=request.user.username)
        all_unfinished_tasks = Task.objects.filter(username=request.user.username, status="QUEUING")
        all_failed_tasks = Task.objects.filter(username=request.user.username, status="FAILED")
        print("===================\n", UserProfile.objects.get(user=User.objects.get(username=request.user.username)).capacity)

        for unfinished_task in all_unfinished_tasks:
            if os.path.exists(unfinished_task.outfile_location):
                unfinished_task.status = "FINISHED"
                unfinished_task.save()
        for failed_task in all_failed_tasks:
            if os.path.exists(failed_task.outfile_location):
                failed_task.status = "FINISHED"
                failed_task.save()
        all_tasks = Task.objects.filter(username=request.user.username)
        template = loader.get_template('main/task.html')
        context = {'all_files': all_files, 'all_tasks': all_tasks}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST' and request.user.is_authenticated():
        if 'new_task_button' in request.POST:
            # username = request.POST.get("user", None)
            username = request.user.username
            filenames = request.POST.getlist("files[]")
            speed = request.POST.get("speed", "ssm")
            threshold = request.POST.get("threshold", "10")
            ssmiter = request.POST.get("ssmiter", '')
            message = "YOU SUBMITTED:\n"
            for file in filenames:
                file_path = UploadFile.objects.get(filename=file, username=username).file_path()

                fmt = "%Y-%m-%d %H:%M:%S %Z%z"

                # Current time in UTC
                now_utc = datetime.now(timezone('UTC'))
                print("+++++++++", now_utc.strftime(fmt))

                # Convert to US/Pacific time zone
                now_local = now_utc.astimezone(timezone('Australia/Sydney'))
                print("_+++++++++++++++", now_local.strftime(fmt))

                submit_time = now_utc.strftime("%Y%m%d%H%M%S")
                str_time = now_local.strftime("%Y-%m-%d %H:%M:%S %p")
                # str_time = now_local.strftime("%b %d,%Y %I:%M:%S %p")
                print("====================\n", str_time)
                output_file = file + "_" + submit_time + ".swc"
                output_location = file_path + "_" + submit_time + ".swc"

                # Create async task
                task_id = async('main.rivulet_task.process_tif', file_name=file, file_path=file_path, user_name=username,
                                out_file=output_file, output_location=output_location, threshold=threshold, ssmiter=ssmiter,speed=speed)
                task_token = humanize(task_id)

                threshold_int = int(request.POST.get("threshold", "10"))
                ssmiter_int = request.POST.get("ssmiter", '')
                if ssmiter_int != '':
                    ssmiter_int = int(ssmiter)
                    task = Task(username=username, filename=file, status="QUEUING",
                                outfile_name=output_file, outfile_location=output_location, task_id=task_id,
                                submit_time=str_time, speed=speed, ssmiter=ssmiter_int, threshold=threshold_int)
                else:
                    task = Task(username=username, filename=file, status="QUEUING",
                                outfile_name=output_file, outfile_location=output_location, task_id=task_id,
                                submit_time=str_time, speed=speed, threshold=threshold_int)
                task.save()

                message = message + file + '---> task_id: ' + str(task_token) + "<br>"

            messages.info(  # Django message as notification
                request,
                message
            )
            return render(request, 'main/message.html')
        elif 'delete_raw_file_button' in request.POST:
            filenames = request.POST.getlist("files[]")
            username = request.user.username
            for file in filenames:
                file_location = UploadFile.objects.get(filename=file, username=username).file_path()
                temp = UploadFile.objects.filter(filename=file, username=username).delete()
                raw_file_size = int(os.path.getsize(str(file_location)))/(1024*1024)
                os.remove(file_location)
                current_user = UserProfile.objects.get(user=User.objects.get(username=username))
                current_user.storage_used -= raw_file_size
                current_user.save()
                print("===================\n", temp)

            return HttpResponseRedirect(reverse('main:task'))
        elif 'download_button' in request.POST:
            request_files = []
            for item in request.POST:
                if item != "download_button" and item != "csrfmiddlewaretoken":
                    request_files.append(item)
            download_time = time.strftime("%Y%m%d%H%M%S")
            zip_subdir = "zip_swc_file_" + download_time
            zip_filename = "%s.zip" % zip_subdir   # construct zipfile name
            s = BytesIO()
            zf = zipfile.ZipFile(s, "w")

            for fpath in request_files:
                print("=========================\n", fpath)
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                zf.write(fpath, zip_path)
            zf.close()
            resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp
        elif 'delete_button' in request.POST:
            for item in request.POST:
                if item != "delete_button" and item != "csrfmiddlewaretoken":
                    temp = Task.objects.filter(outfile_location=item).delete()
                    os.remove(item)
                    print("=======================\n", temp)

            return HttpResponseRedirect(reverse('main:task'))


    notification = "Please Login First."
    return render(request, 'message.html', {'message': notification})


def upload(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.user.username
            filename = os.path.basename(request.FILES['file'].name)
            exist_check = UploadFile.objects.filter(filename=filename, username=username)
            if exist_check:
                print("===================\n ALREADY EXIST!!!  ", os.path.basename(request.FILES['file'].name))
            else:
                new_file = UploadFile(
                    username=username,
                    filename=filename,
                    file=request.FILES['file']
                )
                new_file.save()
                new_file_size = int(os.path.getsize(str(new_file.file)))/(1024*1024)
                # increment the used storage
                current_user = UserProfile.objects.get(user=User.objects.get(username=username))
                current_user.storage_used += new_file_size
                current_user.save()

                print("===================\n", new_file.file)
                print("\n===================\n", new_file_size)

            return HttpResponseRedirect(reverse('main:home'))
    elif request.method == 'GET' and request.user.is_authenticated():
        username = request.user.username
        current_user = UserProfile.objects.get(user=User.objects.get(username=username))
        capacity = current_user.capacity
        used_capacity = current_user.storage_used
        free_storage = capacity - used_capacity
        print("================================\n",free_storage)
        all_upload_files = UploadFile.objects.filter(username=request.user.username)
        files_array = []
        for file in all_upload_files:
            files_array.append(str(file))

        json_upload_files = json.dumps(files_array)
        data = {'all_upload_files': json_upload_files, 'free_storage': free_storage}
        return render(request, 'main/upload.html', data)
    notification = "Please Login First."
    return render(request, 'message.html', {'message': notification})


def home(request):
    if request.user.is_authenticated():
        return render(request, 'main/homepage.html')
    else:
        notification = "Please Login First."
        return render(request, 'message.html', {'message': notification})

