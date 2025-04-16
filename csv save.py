# csv형식
# school_name,product_name,location,ip_address
# 은계중학교,MZ4000i,2층 본교무실 정보부,10.121.142.205
# 서울고등학교,HP4203dn,3층 교무실,10.121.130.12
# 창원초등학교,GX7092,1층 교장실,10.121.150.5


# 아래 코드를 python manage.py shell에서 실행하세요:
import csv
from unidecode import unidecode
from django.utils.text import slugify
from printer.models import DeviceInfo  # 앱 이름에 맞게 수정하세요

def custom_slug(school_name):
    return slugify(unidecode(school_name))

with open('devices.csv', newline='', encoding='cp949') as csvfile:  # UTF-8 저장 시 'utf-8'
    reader = csv.DictReader(csvfile)
    for row in reader:
        slug = custom_slug(row['school_name'])
        DeviceInfo.objects.create(
            school_name=row['school_name'],
            school_slug=slug,
            product_name=row['product_name'],
            location=row['location'],
            ip_address=row['ip_address']
        )
