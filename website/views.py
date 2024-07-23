from django.views import View
from django.shortcuts import render

class HomeView(View):
    template_name = 'website/index.html'

    def get(self, request):
        
        return render(request, self.template_name)
    
def handler404(request, exception):
    return render(request, 'website/error404.html', status=404)

