from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from .forms import UploadFileForm
from .models import UploadFile, Task
from django.template import loader
import os


# Create your views here.
def new_task(request):
    if request.method == 'GET' and request.user.is_authenticated():
        all_files = UploadFile.objects.filter(username=request.user.username)
        template = loader.get_template('main/task.html')
        context = {'all_files': all_files}
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST' and request.user.is_authenticated():
        # username = request.POST.get("user", None)
        username = request.user.username
        filename = request.POST.get("filename")
        task = Task(username=username, filename=filename)
        task.save()
        file_path = UploadFile.objects.get(filename=filename, username=username).file_path()
        print("=============================\n", file_path)





        return HttpResponseRedirect(reverse('main:home'))
    notification = "Please Login First."
    return render(request, 'message.html', {'message': notification})


def upload(request):

    if request.method == 'POST' and request.user.is_authenticated():
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(
                username=request.user.username,
                filename=os.path.basename(request.FILES['file'].name),
                file=request.FILES['file'])
            new_file.save()

            return HttpResponseRedirect(reverse('main:home'))
    elif request.method == 'GET' and request.user.is_authenticated():
        form = UploadFileForm()

        data = {'form': form}
        return render(request, 'main/upload.html', data)
    notification = "Please Login First."
    return render(request, 'message.html', {'message': notification})


def home(request):
    if request.user.is_authenticated():
        return render(request, 'main/homepage.html')
    else:
        notification = "Please Login First."
        return render(request, 'message.html', {'message': notification})
