from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render


def main(request):
    return render(request, 'main.html')


def page_not_found(request, exception):
    return render(request, '404.html', {})


def server_error(request):
    return render(request, '500.html', {})


# 403 에러(1)
def any_request(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('any_request.html', context=context)


# 403 에러(2)
def csrf_failure(request, reason=""):
    context = {'RequestContext': RequestContext(request)}
    response = render_to_response('403.html', context)
    response.status_code = 403
    return response
