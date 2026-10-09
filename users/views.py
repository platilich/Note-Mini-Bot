from logging import log

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from .models import TelegramUser




@staff_member_required
def custom_admin(request):
    users = TelegramUser.objects.all().order_by('-created_at')


    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action and user_id:
            try:
                user = TelegramUser.objects.get(user_id=user_id)

                if action == 'ban':
                    user.is_banned = True


                elif action == 'unban':
                    user.is_banned = False



                user.save()

            except Exception as e:
                print(e)


    return render(request, 'index.html', {
        'users': users,
    })
