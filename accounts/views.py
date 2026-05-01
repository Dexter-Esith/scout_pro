from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import InviteCode, Profile

def register(request):
    if request.method == 'POST':
        code = request.POST.get('invite_code', '').strip().upper()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        error = None

        try:
            invite = InviteCode.objects.get(code=code, is_used=False)
        except InviteCode.DoesNotExist:
            error = 'Invalid or already used invite code.'

        if not error and password != password2:
            error = 'Passwords do not match.'

        if not error and User.objects.filter(email=email).exists():
            error = 'Email already registered.'

        if not error and len(password) < 6:
            error = 'Password must be at least 6 characters.'

        if not error and not first_name:
            error = 'First name is required.'

        if not error and not last_name:
            error = 'Last name is required.'

        if not error:
            # username-ად email გამოვიყენოთ
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
            )
            invite.is_used = True
            invite.used_by = user
            invite.save()
            InviteCode.objects.create(
                code=InviteCode.generate_code(),
                created_by=invite.created_by
            )
            login(request, user)
            return redirect('/dashboard/')

        return render(request, 'accounts/register.html', {
            'error': error,
            'code': code,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        error = None

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('/dashboard/')
            else:
                error = 'Invalid email or password.'
        except User.DoesNotExist:
            error = 'Invalid email or password.'

        return render(request, 'accounts/login.html', {'error': error})

    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.username = request.POST.get('email', '')
            request.user.save()

        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')

            if not request.user.check_password(old_password):
                return render(request, 'accounts/profile.html', {'error_password': 'Current password is incorrect.'})
            if new_password != new_password2:
                return render(request, 'accounts/profile.html', {'error_password': 'Passwords do not match.'})
            if len(new_password) < 6:
                return render(request, 'accounts/profile.html', {'error_password': 'Password must be at least 6 characters.'})

            request.user.set_password(new_password)
            request.user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)

        return redirect('profile')

    return render(request, 'accounts/profile.html')

@login_required
def scout_list(request):
    from django.contrib.auth.models import User
    scouts = User.objects.all().order_by('first_name')
    return render(request, 'accounts/scout_list.html', {'scouts': scouts})

@login_required
def scout_profile(request, pk):
    from django.contrib.auth.models import User
    from players.models import Player
    from reports.models import Report
    scout = get_object_or_404(User, pk=pk)
    reports = Report.objects.filter(scout=scout).select_related('player')[:10]
    added_players = Player.objects.filter(created_by=scout)[:10]
    report_count = Report.objects.filter(scout=scout).count()
    return render(request, 'accounts/scout_profile.html', {
        'scout': scout,
        'reports': reports,
        'added_players': added_players,
        'report_count': report_count,
    })