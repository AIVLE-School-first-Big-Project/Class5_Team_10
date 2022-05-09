from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout


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
    return render(request, 'any_request.html', context=context)


# 403 에러(2)
def csrf_failure(request, reason=""):
    auth_logout(request)
    context = {'RequestContext': RequestContext(request)}
    response = render(request, '403.html', context)
    response.status_code = 403
    return response
