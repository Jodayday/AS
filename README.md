# 🖨️ 임대 프린터 A/S 접수 시스템

> 각 학교에 설치된 임대 프린터의 A/S 요청을 웹에서 간편하게 관리할 수 있는 Django 기반 웹 애플리케이션입니다.
> chatgpt를 이용함
---

## 🔍 주요 기능

### 1️⃣ A/S 접수 리스트 페이지  
- 각 학교에서 요청한 A/S 내역을 **표 형식으로 정리**
- **학교명**, **제품명**, **설치위치**, **IP**, **증상**, **내용**, **접수자**, **상태** 표시
- "⏳ 미처리" 상태일 경우 `"⬜ 완료처리"` 버튼을 눌러 `"✅ 완료"` 상태로 변경 가능
- 테스트 이미지
![image](https://github.com/user-attachments/assets/7a29476c-89a0-452f-b4a8-1f9e852d18fa)
---

### 2️⃣ A/S 접수 등록 페이지  
- 접수하려는 프린터의 **기본정보 자동 표시 (학교, 제품명, 설치 위치, IP)**  
- 증상 선택(1~5번 콤보박스) 후 **필요시 추가 내용 입력** 가능
- 프린터마다 고유 URL로 접속 → 예: `/submit/eungye/1/`
- 테스트 이미지
![image](https://github.com/user-attachments/assets/68c40743-f110-4436-aefc-3851e5d1223f)
---

## ⚙️ 기술 스택

| 항목 | 기술 |
|------|------|
| 백엔드 | Python 3.12.5 / Django 5.2 |
| 프론트엔드 | TailwindCSS |
| 데이터베이스 | SQLite (개발)|
| 배포 | Gunicorn + Nginx (Ubuntu 기준) |

---

## 🚀 기능 요약

- [x] 각 프린터별 고유 URL 접수
- [x] 학교/제품/위치/IP 자동 표기
- [x] 접수 리스트 확인 및 완료 처리
- [x] 접수 상태별 필터링
- [ ] 관리자 로그인 기능 (예정)
- [ ] 검색/필터 기능 (예정)
- [ ] 이메일 알림 기능 (예정)

---

## 🗃️ 프로젝트 구조

```
AS/
├── AS/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
├── printer/
│   ├── models.py
│   ├── views.py
│   ├── templates/
├── .env
├── db.sqlite3
├── manage.py
```

---

## 🛡️ 보안 및 배포 주의사항

- `.env` 파일로 민감 정보 분리  
- Git 업로드 전 `.gitignore`에 다음 포함:
  ```gitignore
  .env
  *.sqlite3
  venv/
  __pycache__/
  ```

---

## 🧠 개선 해볼만 한것 (자동화/편의성)

| 제안 | 설명 |
|------|------|
| 접수 완료 시 자동 알림 | 메일, 슬랙, SMS 등 |
| 관리자 전용 대시보드 | 수정/삭제, 검색 기능 |
| 프린터별 상태 통계 | 가장 많이 발생하는 증상 분석 등 |
| QR 코드 출력 | 프린터에 부착 → 바로 URL 접속 가능 |

---
