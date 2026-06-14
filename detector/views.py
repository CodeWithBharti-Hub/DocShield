import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import ScanReport
from .analyzer import analyze_file


def home(request):
    total_scans = ScanReport.objects.count()
    fake_count = ScanReport.objects.filter(verdict='fake').count()
    real_count = ScanReport.objects.filter(verdict='real').count()
    suspicious_count = ScanReport.objects.filter(verdict='suspicious').count()
    recent = ScanReport.objects.all()[:5]

    context = {
        'total_scans': total_scans,
        'fake_count': fake_count,
        'real_count': real_count,
        'suspicious_count': suspicious_count,
        'recent': recent,
    }
    return render(request, 'detector/home.html', context)


@require_POST
def analyze(request):
    uploaded_file = request.FILES.get('file')
    file_type = request.POST.get('file_type', 'document')

    if not uploaded_file:
        return JsonResponse({'error': 'Koi file nahi mili'}, status=400)

    if file_type not in ('document', 'photo', 'video'):
        file_type = 'document'

    # Run analysis
    result = analyze_file(uploaded_file, file_type)

    # Save to DB
    report = ScanReport.objects.create(
        file_name=uploaded_file.name,
        file_type=file_type,
        file_size=uploaded_file.size // 1024,
        verdict=result['verdict'],
        fake_score=result['fake_score'],
        issues_found=result['issues_found'],
        warnings_found=result['warnings_found'],
        checks_json=json.dumps(result['checks']),
        summary=result['summary'],
    )

    return JsonResponse({
        'report_id': report.pk,
        'file_name': report.file_name,
        'verdict': report.verdict,
        'fake_score': report.fake_score,
        'issues_found': report.issues_found,
        'warnings_found': report.warnings_found,
        'checks': result['checks'],
        'summary': report.summary,
    })


def history(request):
    reports = ScanReport.objects.all()
    return render(request, 'detector/history.html', {'reports': reports})


def report_detail(request, pk):
    report = get_object_or_404(ScanReport, pk=pk)
    checks = json.loads(report.checks_json)
    return render(request, 'detector/report_detail.html', {'report': report, 'checks': checks})
