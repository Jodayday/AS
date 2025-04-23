from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

class DeviceInfo(models.Model):
    school_name = models.CharField(max_length=100)
    school_slug = models.SlugField(max_length=100, null=True)  # 예: eungye
    product_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()

    def save(self, *args, **kwargs):
        if not self.school_slug:
            self.school_slug = slugify(unidecode(self.school_name))
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.school_name} - {self.product_name}"

class ASRequest(models.Model):
    SYMPTOM_CHOICES = [
        ('1', '1. 잉크 및 토너 부족'),
        ('2', '2. 스캔'),
        ('3', '3. 출력물이 깨끗하지 않음'),
        ('4', '4. 에러발생'),
        ('5', '5. 기타'),
    ]
    device = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE, null=True)
    symptom = models.CharField(max_length=1, choices=SYMPTOM_CHOICES, default="")
    detail = models.TextField(blank=True, null=True)
    submitter = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)  # ✅ 완료 여부 추가
    completed_at = models.DateTimeField(null=True, blank=True)  # ✅ 추가
    comment = models.TextField(blank=True, null=True, help_text="관리자 코멘트")
    
    def __str__(self):
        return f"{self.get_symptom_display()} - {self.submitter}"


