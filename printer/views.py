from django.shortcuts import render, redirect, get_object_or_404
from .forms import ASRequestForm
from printer.models import ASRequest, DeviceInfo

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


def request_success(request):
    return render(request, 'request_success.html')

def request_list(request):
    requests = ASRequest.objects.order_by('-submitted_at')
    return render(request, 'request_list.html', {'requests': requests})

def mark_completed(request, request_id):

    req = get_object_or_404(ASRequest, id=request_id)
    req.is_completed = True
    req.save()
    return redirect('request_list')  # 또는 다른 뷰 이름