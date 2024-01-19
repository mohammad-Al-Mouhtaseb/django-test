from django.http import HttpResponse,Http404

def handler404(request,exception):
    return HttpResponse("not found")