from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class UserFormView(View):
    form_class = UserForm
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        logout(request)
        num_fields = 0
        for key in request.POST:
            num_fields += 1
            print("============\n" + key)

        if num_fields == 6:
            form = self.form_class(request.POST)
            if form.is_valid():

                user = form.save(commit=False)
                # cleaned data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                # check if user register successfully
                if User.objects.get(username=username):
                    user_profile = UserProfile(user=User.objects.get(username=username))
                    user_profile.save()

                notification = "Thanks to join us."
                return render(request, 'message.html', {'message': notification})
        elif num_fields == 3:
            username = request.POST['username']
            password = request.POST['password']
            # return user object if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return render_to_response('main/task.html', {'user': user}, RequestContext(request))
                    return HttpResponseRedirect(reverse('main:task'))
        return render(request, self.template_name)
        # return HttpResponseRedirect(reverse('main:task'))
