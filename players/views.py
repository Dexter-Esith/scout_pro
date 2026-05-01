from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Player
from reports.models import Report
from django.core.paginator import Paginator
from .models import Player, Shortlist
from django.contrib.auth import update_session_auth_hash




@login_required
def dashboard(request):
    from django.contrib.auth.models import User
    from django.db.models import Count

    # Stats
    total_players = Player.objects.count()
    total_reports = Report.objects.count()
    total_scouts = User.objects.count()

    # Position breakdown
    positions = Player.objects.values('position').annotate(count=Count('position')).order_by('-count')

    # Latest reports
    latest_reports = Report.objects.select_related('player', 'scout').all()[:5]

    # Recently added players
    recent_players = Player.objects.all()[:5]

    context = {
        'total_players': total_players,
        'total_reports': total_reports,
        'total_scouts': total_scouts,
        'positions': positions,
        'latest_reports': latest_reports,
        'recent_players': recent_players,
    }
    return render(request, 'players/dashboard.html', context)

@login_required
def player_list(request):
    players = Player.objects.all()

    # Search
    query = request.GET.get('q', '')
    if query:
        players = players.filter(full_name__icontains=query)

    # Filter by position
    position = request.GET.get('position', '')
    if position:
        players = players.filter(position=position)

    # Filter by nationality
    nationality = request.GET.get('nationality', '')
    if nationality:
        players = players.filter(nationality__icontains=nationality)

    # Filter by added_by
    added_by = request.GET.get('added_by', '')
    if added_by:
        players = players.filter(created_by__id=added_by)

    # Pagination — 10 მოთამაშე გვერდზე
    paginator = Paginator(players, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'players': page_obj,
        'page_obj': page_obj,
        'query': query,
        'position': position,
        'nationality': nationality,
    }
    return render(request, 'players/player_list.html', context)

@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    reports = player.report_set.select_related('scout').all()
    in_shortlist = Shortlist.objects.filter(user=request.user, player=player).exists()
    context = {
        'player': player,
        'reports': reports,
        'in_shortlist': in_shortlist,
    }
    return render(request, 'players/player_detail.html', context)

@login_required
def player_add(request):
    if request.method == 'POST':
        Player.objects.create(
            full_name=request.POST['full_name'],
            date_of_birth=request.POST['date_of_birth'],
            nationality=request.POST['nationality'],
            club=request.POST['club'],
            position=request.POST['position'],
            preferred_foot=request.POST['preferred_foot'],
            height=request.POST['height'],
            weight=request.POST['weight'],
            market_value=request.POST.get('market_value') or None,
            contract_expiry=request.POST.get('contract_expiry') or None,
            agent=request.POST.get('agent') or '',
            photo=request.FILES.get('photo'),
            created_by=request.user,  # ← ეს დაამატე
        )
        return redirect('player_list')
    return render(request, 'players/player_add.html')

@login_required
def player_photo_upload(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST' and request.FILES.get('photo'):
        player.photo = request.FILES['photo']
        player.save()
    return redirect('player_detail', pk=pk)

@login_required
def player_compare(request):
    player_ids = request.GET.getlist('players')
    player_ids = [pid for pid in player_ids if pid]  # ცარიელები გავფილტროთ
    players = []

    for pid in player_ids[:4]:
        try:
            player = Player.objects.get(pk=pid)
            reports = player.report_set.all()
            avg = round(sum(float(r.rating) for r in reports) / len(reports), 1) if reports else None
            players.append({'player': player, 'avg': avg, 'report_count': len(reports)})
        except Player.DoesNotExist:
            pass

    all_players = Player.objects.all()

    # 4 slot — ცარიელი იქნება თუ არ არის არჩეული
    selected = player_ids + [''] * (4 - len(player_ids))

    return render(request, 'players/player_compare.html', {
        'players': players,
        'all_players': all_players,
        'selected': selected,
    })

@login_required
def player_edit(request, pk):
    player = get_object_or_404(Player, pk=pk)

    # მხოლოდ admin ან ვინც დაამატა
    if not request.user.is_staff and player.created_by != request.user:
        return redirect('player_detail', pk=pk)

    if request.method == 'POST':
        player.full_name = request.POST['full_name']
        player.date_of_birth = request.POST['date_of_birth']
        player.nationality = request.POST['nationality']
        player.club = request.POST['club']
        player.position = request.POST['position']
        player.preferred_foot = request.POST['preferred_foot']
        player.height = request.POST['height']
        player.weight = request.POST['weight']
        player.market_value = request.POST.get('market_value') or None
        player.contract_expiry = request.POST.get('contract_expiry') or None
        player.agent = request.POST.get('agent') or ''
        if request.FILES.get('photo'):
            player.photo = request.FILES['photo']
        player.save()
        return redirect('player_detail', pk=pk)

    return render(request, 'players/player_edit.html', {'player': player})

@login_required
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)

    # მხოლოდ admin ან ვინც დაამატა
    if not request.user.is_staff and player.created_by != request.user:
        return redirect('player_detail', pk=pk)

    if request.method == 'POST':
        player.delete()
        return redirect('player_list')

    return render(request, 'players/player_delete.html', {'player': player})

@login_required
def shortlist(request):
    items = Shortlist.objects.filter(user=request.user).select_related('player')
    return render(request, 'players/shortlist.html', {'items': items})

@login_required
def shortlist_toggle(request, pk):
    player = get_object_or_404(Player, pk=pk)
    item, created = Shortlist.objects.get_or_create(user=request.user, player=player)
    if not created:
        item.delete()
    return redirect('player_detail', pk=pk)

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
            update_session_auth_hash(request, request.user)

        return redirect('profile')

    return render(request, 'accounts/profile.html')