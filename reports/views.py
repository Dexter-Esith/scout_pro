from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Report
from players.models import Player

@login_required
def report_list(request):
    reports = Report.objects.select_related('player', 'scout').all()

    query = request.GET.get('q', '')
    if query:
        reports = reports.filter(player__full_name__icontains=query)

    scout_filter = request.GET.get('scout', '')
    if scout_filter:
        reports = reports.filter(scout__username=scout_filter)

    scout_ids = Report.objects.values_list('scout_id', flat=True).distinct()
    scouts = User.objects.filter(id__in=scout_ids)

    context = {
        'reports': reports,
        'query': query,
        'scout_filter': scout_filter,
        'scouts': scouts,
    }
    return render(request, 'reports/report_list.html', context)

@login_required
def add_report(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        Report.objects.create(
            player=player,
            scout=request.user,
            match_name=request.POST['match_name'],
            rating=request.POST['rating'],
            strengths=request.POST['strengths'],
            weaknesses=request.POST['weaknesses'],
            notes=request.POST.get('notes', ''),
        )
        return redirect('player_detail', pk=player_id)
    return render(request, 'reports/add_report.html', {'player': player})

@login_required
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if not request.user.is_staff and report.scout != request.user:
        return redirect('player_detail', pk=report.player.pk)
    if request.method == 'POST':
        report.match_name = request.POST['match_name']
        report.rating = request.POST['rating']
        report.strengths = request.POST['strengths']
        report.weaknesses = request.POST['weaknesses']
        report.notes = request.POST.get('notes', '')
        report.save()
        return redirect('player_detail', pk=report.player.pk)
    return render(request, 'reports/report_edit.html', {'report': report})

@login_required
def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if not request.user.is_staff and report.scout != request.user:
        return redirect('player_detail', pk=report.player.pk)
    if request.method == 'POST':
        player_id = report.player.pk
        report.delete()
        return redirect('player_detail', pk=player_id)
    return render(request, 'reports/report_delete.html', {'report': report})