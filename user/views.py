from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms import formset_factory, inlineformset_factory
from user.forms import UserCreationForm, KidRegisterForm, UpdateUserForm, UpdateKidForm
from user.models import User, Kid
from user.decorators import *


# 회원가입
@logout_message_required
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        id = request.POST.get('id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        name = request.POST.get('name')      
        # 사용자 아이디가 이미 존재하는 아이디인 경우
        try: 
            if User.objects.get(id=id):
                id_error_msg = '이미 존재하는 아이디입니다.'
            context={
                'form' : form,
                'id_error_msg' : id_error_msg,
            }
            return render(request, 'user/signup.html', context)        
        except:
            # 비밀번호와 비밀번호 확인이 일치하지 않는 경우
            if password1 != password2:
                password_error_msg = '비밀번호가 일치하지 않습니다. 다시 입력해주세요.'
                return render(request, 'user/signup.html', {'form': form, 'password_error_msg': password_error_msg})
            else:
                if form.is_valid():
                    User.objects.create_user(id=id, username=id, password=password1, email=email, name=name)
                    user = authenticate(username=id, password=password1)  # 사용자 인증
                    auth_login(request, user)  # 로그인
                    return redirect('/')
                else:
                    email_error_msg = '이메일 양식이 맞지 않습니다.'
                    context = {
                        'form' : form,
                        'email_error_msg' : email_error_msg,
                    }
                    return render(request, 'user/signup.html', {'form': form, 'email_error_msg': email_error_msg})
    else:
        form = UserCreationForm()
    context={
        'form' : form,
    }
    return render(request, 'user/signup.html', context)


# 아이디 중복체크
def id_check(request):
    id = request.GET.get('user_id')
    result = 'fail'
    try:
        check_result =  User.objects.get(id=id)
    except:
        check_result = None
    if check_result is None:
        result = 'possible'
    return JsonResponse({ 'result': result })


# 로그인
@logout_message_required
def CustomLogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        user_id = request.POST.get('username')
        try:
            User.objects.get(username=user_id)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('user:kid_select')
            else:
                password_error_msg = '비밀번호가 일치하지 않습니다. 다시 입력해주세요.'
                context = {
                    'form' : form,
                    'password_error_msg' : password_error_msg,
                }
                return render(request, 'user/login.html', context)
        except:
            id_error_msg = '일치하는 아이디가 없습니다.'
            context = {
                    'form' : form,
                    'id_error_msg' : id_error_msg,
            }
            return render(request, 'user/login.html', context)
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'user/login.html', context)


# 아이등록
@login_message_required
def kid_register(request):
    if request.method == "POST":
        form = KidRegisterForm(request.POST, request.FILES)
        print(request)
        if form.is_valid():
            kid_regit = form.save(commit=False)
            kid_regit.user = request.user
            kid_regit.save()
            return redirect('user:kid_select')
    else:
        form = KidRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)


# 아이선택
@login_message_required
def kid_select(request):
    if request.user.is_authenticated:
        user_id = request.session['_auth_user_id']
        kid_set = Kid.objects.filter(user_id = user_id)
    context = {
        'kid_set' : kid_set,
    }
    return render(request, 'user/select.html', context)


# 회원 정보 수정
@login_message_required
def user_update(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('user:kid_select')
        else:
            email_error_msg = '이메일 양식이 맞지 않습니다.'
            context = {
                'form' : form,
                'email_error_msg' : email_error_msg,
            }
            return render(request, 'user/user_update.html', context)  
    else:
        form = UpdateUserForm()
    context = {
        'form' : form,
        'user' : user,
    }
    return render(request, 'user/user_update.html', context)


# 아이 정보 수정
# def kid_update(request):
#     user_id = request.session['_auth_user_id']
#     kid_set = Kid.objects.filter(user_id = user_id)
#     KidRegisterFormSet = formset_factory(KidRegisterForm, extra=0)
#     if request.method == 'POST':
#         formset = KidRegisterFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             formset.save()
#             messages.success(request, '아이정보가 수정되었습니다.')
#             # do something with the formset.cleaned_data
#             return redirect('/')
#         else:
#             context = {
#                 'formset' : formset,
#             }
#             return render(request, 'user/kid_update.html', context)
#     else:
#         formset = KidRegisterFormSet(initial=[
#             {"name" : kid.name, 
#              "birthday" : kid.birthday,
#              "img" : kid.img, 
#              "height" : kid.height, 
#              "weight" : kid.weight}
#              for kid in kid_set
#         ])
#     context = {'formset' : formset}
#     return render(request, 'user/kid_update.html', context)

# 아이 정보 수정
@login_message_required
def kid_update(request):
    user_id = request.session['_auth_user_id']
    user = User.objects.get(pk = user_id)
    KidRegisterFormSet = inlineformset_factory(User, Kid, extra=0, fields=(
        'name', 'birthday', 'img', 'height', 'weight'
    ))
    print('1')
    if request.method == 'POST':
        formset = KidRegisterFormSet(request.POST, request.FILES, instance=user)
        print('2')
        if formset.is_valid():
            formset.save()
            messages.success(request, '아이정보가 수정되었습니다.')
            # do something with the formset.cleaned_data
            return redirect('/')
    else:
        print('3')
        formset = KidRegisterFormSet(instance=user)
    context = {'formset' : formset}
    
    ##테스트
    for form in formset:
        print(form.as_table())
    ###
    print('4')
    
    
    return render(request, 'user/kid_update.html', context)


# 회원탈퇴
@login_message_required
def member_del(request):
    user_id = request.session['_auth_user_id']
    data = User.objects.get(pk=user_id)
    data.delete()
    logout(request)
    return redirect('/')


# 로그아웃
# @logout_message_required
def CustomLogout(request):
    logout(request)
    return redirect('/')


# 아이디 찾기 메일링 서비스
@login_message_required
def ForgotIDView(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                template = render_to_string('user/find_username_email_template.html', 
                                            {'name': user.name, 'id':user.username})
                method_email = EmailMessage(
                    '[밀키드] 요청하신 ID입니다.',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                method_email.send(fail_silently=False)
                return render(request, 'user/find_username_done.html', context)
        except:
            messages.info(request, "등록된 이메일이 없습니다.")
    context = {}
    return render(request, 'user/find_username_form.html', context)


# 아이 정보 수정
@login_message_required
def kid_update_test(request):
    user_id = request.session['_auth_user_id']
    kid_set = Kid.objects.filter(user_id = user_id)
    KidRegisterFormSet = formset_factory(KidRegisterForm, extra=0)
    if request.method == 'POST':
        formset = KidRegisterFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            messages.success(request, '아이정보가 수정되었습니다.')
            # do something with the formset.cleaned_data
            return redirect('/')
        else:
            context = {
                'formset' : formset,
            }
            return render(request, 'user/kid_update_test.html', context)
    else:
        formset = KidRegisterFormSet(initial=[
            {"name" : kid.name, 
             "birthday" : kid.birthday,
             "img" : kid.img, 
             "height" : kid.height, 
             "weight" : kid.weight}
             for kid in kid_set
        ])
    context = {'formset' : formset}
    return render(request, 'user/kid_update_test.html', context)


# 아이 정보 삭제
@login_message_required
def kid_del(request):
    kid_id = request.session['_auth_user_id'] # 아이 세션 정보를 받아와야 함
    data = Kid.objects.get(pk=kid_id)
    data.delete()
    return redirect('/')


# 아이 정보 수정(각자)
@login_message_required
def kid_update_each(request):
    kid_id = request.session['kid_id']
    kid = Kid.objects.get(pk=kid_id)
    if request.method == 'POST':
        form = UpdateKidForm(request.POST, instance=kid)
        if form.is_valid():
            form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('user:kid_select')
        else:
            email_error_msg = '이메일 양식이 맞지 않습니다.'
            context = {
                'form' : form,
                'email_error_msg' : email_error_msg,
            }
            return render(request, 'user/kid_update_each.html', context)  
    else:
        form = UpdateKidForm()
    context = {
        'form' : form,
        'kid' : kid,
    }
    return render(request, 'user/kid_update_each.html', context)