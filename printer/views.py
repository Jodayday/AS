from django.shortcuts import render, redirect, get_object_or_404
from .forms import ASRequestForm
from printer.models import ASRequest, DeviceInfo
from django.db.models import Q
from django.utils.timezone import now
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
import openpyxl
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# views.py에 공통 함수로 추출
def filter_requests(queryset, request):
    school = request.GET.get("school")
    symptom = request.GET.get("symptom")
    status = request.GET.get("status")

    if school:
        queryset = queryset.filter(device__school_name=school)
    if symptom:
        queryset = queryset.filter(symptom=symptom)
    if status:
        if status == 'done':
            queryset = queryset.filter(is_completed=True)
        elif status == 'pending':
            queryset = queryset.filter(is_completed=False)

    return queryset


def export_as_excel(request):
    # 기존 필터 조건과 동일하게 적용

    queryset = filter_requests(ASRequest.objects.all().order_by('-submitted_at'), request)


    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "AS 목록"

    # 헤더에 코멘트 추가
    ws.append(["학교명", "제품명", "설치위치", "IP 주소", "증상", "내용", "접수자", "접수일", "상태", "완료일", "코멘트"])

    for req in queryset:
        ws.append([
            req.device.school_name,
            req.device.product_name,
            req.device.location,
            req.device.ip_address,
            req.get_symptom_display(),
            req.detail or "-",
            req.submitter,
            req.submitted_at.strftime("%Y-%m-%d %H:%M"),
            "완료" if req.is_completed else "미처리",
            req.completed_at.strftime("%Y-%m-%d %H:%M") if req.completed_at else "-",
            req.comment or "-",  # ✅ 코멘트 추가
        ])

    # 응답으로 Excel 파일 반환
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=as_list.xlsx'
    wb.save(response)
    return response

def latest_request_time(request):
    latest = ASRequest.objects.order_by('-submitted_at').first()
    if latest:
        return JsonResponse({"timestamp": latest.submitted_at.isoformat()})
    return JsonResponse({"timestamp": None})


def submit_request(request, school_slug, device_id):
    device = get_object_or_404(DeviceInfo, id=device_id, school_slug=school_slug)

    if request.method == 'POST':
        form = ASRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.device = device
            req.save()
            return redirect('request_success')
    else:
        form = ASRequestForm()

    return render(request, 'as_form.html', {'form': form, 'device': device})

def mark_completed(request, request_id):
    req = get_object_or_404(ASRequest, id=request_id)
    req.is_completed = True
    req.completed_at = now()
    req.save()

    # ✅ 사용자가 있던 페이지로 다시 이동
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)



def request_success(request):
    return render(request, 'request_success.html')

@csrf_exempt
def save_comment(request, request_id):
    """
    ✅ A/S 요청에 대한 관리자 코멘트 저장용 Ajax 뷰
    """
    if request.method == "POST":
        comment = request.POST.get("comment", "")
        req = get_object_or_404(ASRequest, pk=request_id)
        req.comment = comment
        req.save()
        return JsonResponse({"success": True, "comment": req.comment})
    return JsonResponse({"success": False}, status=400)


class ASRequestListView(ListView):
    model = ASRequest
    template_name = "request_list.html"
    context_object_name = "requests"
    paginate_by = 20  # 기본 페이지네이션 처리

    def get_queryset(self):
        """
        ✅ 필터링 로직 분리: filter_requests() 호출
        self.request는 CBV 내부에서 사용되는 HttpRequest 객체
        """
        base_qs = super().get_queryset().order_by("-submitted_at")
        return filter_requests(base_qs, self.request)

    def get_context_data(self, **kwargs):
        """
        ✅ 추가적으로 템플릿에서 필요한 context 데이터 전달
        - 학교 리스트, 증상 선택 목록 등
        """
        context = super().get_context_data(**kwargs)
        context["schools"] = DeviceInfo.objects.values_list("school_name", flat=True).distinct()
        context["symptoms"] = ASRequest.SYMPTOM_CHOICES
        return context