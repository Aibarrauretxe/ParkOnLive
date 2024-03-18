from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, redirect
from .users.forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.
def home(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())

def user_register(request):
	if request.method =='POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()

			return redirect('')
		else:
			args = {'form': form}
			return render(request, '../templates/register/user.html', args)
	else:
		form = CustomUserCreationForm()

	args = {'form': form}
	return render(request, '../templates/register/user.html', args)

def user_list(request):
    users = CustomUser.objects.all()
 
    context = {
        'usersList': users,
    }
    return render(request, '../templates/users/list.html', context)