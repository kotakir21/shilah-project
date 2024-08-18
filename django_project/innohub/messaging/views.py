from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.mail import EmailMessage  # Use EmailMessage for attachments
from django.urls import reverse  # Import reverse to generate URLs
from .forms import MessageForm
from .models import Message

User = get_user_model()

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def inbox(request):
    search_query = request.GET.get('q')
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    else:
        # Get users who have sent or received messages with the current user
        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        users = User.objects.filter(
            Q(sent_messages__in=messages) | Q(received_messages__in=messages)
        ).distinct().exclude(id=request.user.id)

    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'messaging/inbox.html', context)

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/sent_messages.html', {'messages': sent_messages})

@login_required
def conversation_view(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.get_conversation(request.user, other_user)

    # Mark messages as read
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()

            # Prepare email with attachment (if any)
            email = EmailMessage(
                subject='New Message from {}'.format(request.user.username),
                body='You have received a new message from {}.\n\nMessage: {}\n\nView and reply to the message here: {}'.format(
                    request.user.username,
                    message.content,
                    request.build_absolute_uri(reverse('conversation', args=[request.user.username]))
                ),
                from_email='shilahkyatuhire@gmail.com',  # Replace with your email address
                to=[other_user.email],
            )

            # Attach the file if there is one
            if message.attachment:
                email.attach(message.attachment.name, message.attachment.read(), request.FILES['attachment'].content_type)
            
            email.send(fail_silently=False)

            return redirect('conversation', username=username)
    else:
        form = MessageForm()

    context = {
        'other_user': other_user,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/conversation.html', context)
