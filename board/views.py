from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from .models import Post, Board, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import PostForm, CommentForm
from decorators import login_message_required, staff_member_required
import os


@login_message_required
def post_list(request):  # 게시물 목록 조회 함수
    page = request.GET.get('page', '1')   # 페이지
    kw = request.GET.get('kw', '')   # 검색어
    type = request.GET.get('type', '')  # 카테고리
    post_list = Post.objects.order_by('-regdate')
    if kw:
        if type == 'title':
            post_list = post_list.filter(Q(title__icontains=kw))  # 제목 검색
        if type == 'content':
            post_list = post_list.filter(Q(content__icontains=kw))  # 내용 검색
        if type == 'category':
            post_list = post_list.filter(Q(board__ctg__icontains=kw))

    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'post_list': page_obj, 'page': page, 'kw': kw, 'type': type}
    return render(request, 'board/post_list.html', context)


@login_message_required
def post(request, post_id):  # 게시물 상세 조회 함수
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post_id)
    comments_list = comments.order_by('-regdate')

    # 댓글 페이징 처리
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(comments_list, 5)  # 페이지당 5개씩 보여주기
    comments_obj = paginator.get_page(page)
    context = {'post': post, 'comments_list': comments_obj, 'page': page}

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(pk=post_id)
            comment.regdate = timezone.now()
            comment.save()
            return HttpResponseRedirect('/board/' + str(post.id))
        else:
            return render(request, 'board/post.html', context)
    return render(request, 'board/post.html', context)


@staff_member_required
def post_create(request):  # 게시물 작성 함수
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.regdate = timezone.now()
            post.img = request.FILES.get('image')
            post.user = request.user
            try:
                Board.objects.get(ctg=request.POST['category'])
            except Exception:
                board = Board(ctg=request.POST['category'])
                board.save()

            post.board = Board.objects.get(ctg=request.POST['category'])
            post.save()
            return redirect('board:post', post_id=post.id)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'board/post_create.html', context)


@staff_member_required
def post_modify(request, post_id):  # 게시물 수정 함수
    post = get_object_or_404(Post, pk=post_id)
    pre_img = post.img
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.moddate = timezone.now()
            if request.FILES.get('image'):
                post.img = request.FILES.get('image')
                # 이미지 삭제 요청이 있으면
            elif request.POST.get('check'):
                post.img = None
                try:
                    root = "media/board_images/"
                    ctg = post.board.ctg
                    os.remove(root + '{}/{}_{}'.format(ctg, pre_img, '.png'))
                except Exception:
                    pass
            else:
                post.img = pre_img
            post.board = Board.objects.get(ctg=request.POST['category'])
            post.save()
            return redirect('board:post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'board/post_modify.html', context)


@staff_member_required
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('board:post_list')


@login_message_required
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    comment.content = request.POST.get('comment')
    comment.moddate = timezone.now()
    comment.save()
    return redirect('board:post', post_id=post_id)


@login_message_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect('board:post', post_id=post_id)
