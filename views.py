from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from core.models import *
from core.forms import *
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from hitcount.views import HitCountDetailView

class BlogView(generic.ListView):
    template_name = 'blog/blog.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context.update({
            'top_hits': Post.objects.filter(published_date__lte=timezone.now()).order_by("-hit_count_generic__hits")[:10],
        })
        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class DetailView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'blog/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        form = CommentForm()
        context.update({
            'form': form,
            'comments': comments,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.author = request.user
            comment.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(comment.post.id,)))

class DraftView(generic.ListView):
    template_name = 'blog/draft_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
    def get_context_data(self, *args, **kwargs):
        context = super(DraftView, self).get_context_data(**kwargs)
        contacts = Contact.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        top_hits = Post.objects.filter(published_date__lte=timezone.now()).order_by("-hit_count_generic__hits")[:10]
        form = PostForm()
        context.update({
            'form': form,
            'contacts': contacts,
            'top_hits': top_hits
        })
        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return HttpResponseRedirect(reverse('core:index'))

@login_required
def publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))

@login_required
def remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return HttpResponseRedirect(reverse('core:index'))

@login_required
def edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
		return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/form.html', {'form': form})
