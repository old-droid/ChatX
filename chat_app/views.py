from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models # Import models for Q objects
from .models import UserProfile, Message
import rsa
import base64

# IMPORTANT: Storing private keys on the server-side (even in the database) is INSECURE for a real-world application.
# For a production chat app, private keys should be generated and stored ONLY on the client-side (e.g., in browser's local storage or a secure enclave).
# This implementation is for demonstration purposes to show the encryption/decryption flow within Django.

def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key.save_pkcs1().decode('utf-8'), private_key.save_pkcs1().decode('utf-8')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            public_key_str, private_key_str = generate_key_pair()
            UserProfile.objects.create(user=user, public_key=public_key_str, private_key=private_key_str) # Storing private key for demo
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    users = UserProfile.objects.exclude(user=request.user)
    return render(request, 'chat_app/home.html', {'users': users})

@login_required
@require_POST
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        message_content = request.POST.get('message_content')

        if not recipient_id or not message_content:
            return JsonResponse({'status': 'error', 'message': 'Recipient and message content are required.'}, status=400)

        try:
            sender_profile = request.user.userprofile
            recipient_profile = get_object_or_404(UserProfile, id=recipient_id)

            # Encrypt the message using the recipient's public key
            recipient_public_key = rsa.PublicKey.load_pkcs1(recipient_profile.public_key.encode('utf-8'))
            encrypted_message = rsa.encrypt(message_content.encode('utf-8'), recipient_public_key)
            encrypted_message_b64 = base64.b64encode(encrypted_message).decode('utf-8')

            Message.objects.create(
                sender=sender_profile,
                recipient=recipient_profile,
                encrypted_message=encrypted_message_b64
            )
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
def get_messages(request, recipient_id=None):
    user_profile = request.user.userprofile
    messages_data = []

    if recipient_id:
        # Get messages between current user and a specific recipient
        recipient_profile = get_object_or_404(UserProfile, id=recipient_id)
        messages = Message.objects.filter(
            (models.Q(sender=user_profile) & models.Q(recipient=recipient_profile)) |
            (models.Q(sender=recipient_profile) & models.Q(recipient=user_profile))
        ).order_by('timestamp')
    else:
        # Get all messages for the current user (sent and received)
        messages = Message.objects.filter(
            models.Q(sender=user_profile) | models.Q(recipient=user_profile)
        ).order_by('timestamp')

    # Decrypt messages
    private_key = rsa.PrivateKey.load_pkcs1(user_profile.private_key.encode('utf-8'))
    for msg in messages:
        try:
            decrypted_content = rsa.decrypt(base64.b64decode(msg.encrypted_message), private_key).decode('utf-8')
            messages_data.append({
                'sender': msg.sender.user.username,
                'recipient': msg.recipient.user.username,
                'content': decrypted_content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            messages_data.append({
                'sender': msg.sender.user.username,
                'recipient': msg.recipient.user.username,
                'content': f"[Error decrypting message: {e}]",
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'messages': messages_data})
