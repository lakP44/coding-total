# 패키지 설치
pip install -r requirements.txt

# DB 연동
cd game
python manage.py makemigrations mainapp
python manage.py migrate mainapp
python manage.py makemigrations core
python manage.py migrate core
python manage.py migrate

# 서버 실행
python manage.py runserver

# 게임 실행
http://localhost:8000/mainapp/main

# 관리자 계정
python manage.py createsuperuser
http://localhost:8000/admin
