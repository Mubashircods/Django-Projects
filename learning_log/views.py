from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """Return a home page of learning_log"""
    return render(request, 'learning_log/index.html')

@login_required
def topic(request):
    """Return all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log/topic.html', context)

@login_required
def topics(request, topic_id):
    """Return all topics"""
    topics = Topic.objects.get(id=topic_id)
    if topics.owner != request.user:
        raise Http404
    entry = topics.entry_set.order_by('-date_added')
    context = {'topics': topics, 'entries': entry}
    return render(request, 'learning_log/topics.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_log:topic')
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add new entries"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_log:topics', topic_id = topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_log/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_log:topics', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log/edit_entry.html', context)

