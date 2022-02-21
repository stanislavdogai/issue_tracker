from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from django.conf import settings

from issue_tracker.apps.accounts.forms import MyUserCreateForm


def register_view(request):
    form = MyUserCreateForm()
    if request.method == 'POST':
        form = MyUserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = request.GET.get('next')
            if url:
                return redirect(url)
            return redirect('webapp:home_page')
    return render(request, 'registration/registration.html', {'form' : form})


class ProfileDetailView(LoginRequiredMixin ,DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    paginated_by = 3
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        paginator = Paginator(
            self.get_object().projects.all(),
            self.paginated_by,
            self.paginate_related_orphans
        )
        print(settings.BASE_DIR)
        page_number = self.request.GET.get('page', '1')
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super(ProfileDetailView, self).get_context_data(**kwargs)

class ProfilesView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'profiles.html'
    context_object_name = 'user_obj'
    permission_required = 'accounts.view_profile'

