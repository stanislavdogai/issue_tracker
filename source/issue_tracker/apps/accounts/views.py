from django.contrib.auth import login
from django.shortcuts import render, redirect


from issue_tracker.apps.accounts.forms import MyUserCreateForm


def register_view(request):
    form = MyUserCreateForm()
    if request.method == 'POST':
        form = MyUserCreateForm(data=request.POST)
        # print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = request.GET.get('next')
            if url:
                return redirect(url)
            return redirect('webapp:home_page')
    return render(request, 'registration/registration.html', {'form' : form})


# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home_page')
#         else:
#             context['has_error'] = True
#     return render(request, 'registration/login.html', context=context)
#
# def logout_view(request):
#     logout(request)
#     return redirect('home_page')