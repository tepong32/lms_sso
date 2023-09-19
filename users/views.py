# from django.shortcuts import render

# # Create your views here.

# def userIndexView(request):
#     context = {
#         # insert context dictionary here
#     }
#     return render(request, 'users/users_index.html', context)


from django.views import View
from django.views.generic import TemplateView, ListView


class UsersIndex(TemplateView):
    template_name = 'users_index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ### add context data here like below:
        # context['my_data'] = 'Hello, World!'

        ### or use the old method:
        # ___wait! I forgot how to do that.
        return context