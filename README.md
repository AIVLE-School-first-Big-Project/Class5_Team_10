<img src="static\images\readme.png"  width="100%" height="auto%">

<br/>

## 1. 팀 소개
- 소속: AI 수도권 5반 1조(10조)
- 조원: 이정현(조장), 김상훈, 김희준, 박유진(서기), 서승우, 송정우


<br/>

## 2. 프로젝트 소개
### 프로젝트 기간
 - 2022.04.11 ~ 2022.05.11
### 주제 선정 배경
 - 아이가 건강하게 자라길 바라는 것은 모든 부모의 바람이다. 부모는 아이가 균형 잡힌 음식을 먹고 성장하기를 바라지만 모든 부모가 영양 지식을 갖춘 것은 아니다. ‘밀키드’ 서비스는 부모에게 자신이 만든 음식의 영양 구성 정보를 알려준다. 부모는 이를 통해 아이에게 부족한 영양이 무엇인지 알고 균형 잡힌 식단을 구성할 수 있을 것이다.
 - 유아기는 발육이 왕성한 시기이며 영양소 필요량을 체중 kg당으로 환산하였을 때 성인보다 2~3배의 영양소 공급이 필요한 시기이다. 또한 아직 장기의 발달이 완성되지 않아 소화흡수 능력이 떨어지고, 면역력이 약하기 때문에 적절한 식품섭취가 중요하다. 우리의 서비스를 통해 아이들은 부족한 영양을 채워줄 적절한 식품을 추천 받을 수 있을 것이다. 

### 주요 서비스 대상
 - 영양 섭취가 매우 중요한 시기인 4 ~ 7세에 자녀를 둔 부모님

### 주요 기능
 - 아이 등록 및 식단 관리 기능
 - 음식 이미지를 분석해 섭취한 영양소 정보 제공
 - 게시판을 통해 사용자들에게 영양 관련 정보 제공

### 서비스 사용 방법
 1. Python 가상환경은 3.8 버전 이상을 사용해주세요.
 2. 사용하시는 DB가 있을 경우 Config Settings에서 설정해주세요. 저희 프로젝트는 MySQL로 설정되어 있습니다.
 3. pip install -r requirements.txt를 실행시켜 필요한 모듈을 설치해주세요.
 4. 서비스를 시작할 때 python manage.py runserver --insecure 로 실행시켜주세요.

<br/>

## 3. Service Flow
<img src="static\images\service_flow.PNG"  width="100%" height="auto%">

<br/>

## 4. Architecture (3 - tier)
<img src="static\images\architecture.png"  width="100%" height="auto%">

<br/>

## 5. ERD
<img src="static\images\ERD.PNG"  width="100%" height="auto%">

## 6. Tech
### Front-End
 <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a>
### Back-End
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://www.djangoproject.com/m/img/logos/django-logo-negative.png" alt="django" width="40" height="40"/> </a>
<a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a>
### Modeling
<a href="https://pytorch.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="40" height="40"/> </a> <a href="https://opencv.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg" alt="opencv" width="40" height="40"/> </a>