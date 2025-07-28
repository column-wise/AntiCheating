# AntiCheating


**2021 Konkuk Univ. Smart ICT Convergence Engineering Capstone Design**

**SW 경진대회 최우수상 🏅 수상작**
  
<sup>![AntiCheating](https://github.com/user-attachments/assets/5a8aba48-12b1-45dc-b437-43a121b39ccb)</sup>

## **프로젝트 소개**

**AntiCheating**은 원격 시험 환경에서 공정성과 신뢰성을 보장하기 위해 설계된 시스템입니다.  
학생은 실시간 웹캠 모니터링을 통해 시험을 응시하고, 감독관은 부정행위를 실시간으로 감지하고 관리할 수 있습니다.

---

## **주요 기능**

- **로그인 및 회원가입**: 사용자 인증 시스템.
- **시험 생성 및 응시**: 관리자는 시험 문제를 생성하고, 학생은 해당 시험에 응시 가능.
- **실시간 웹캠 모니터링**: OpenCV와 머신러닝 기반의 부정행위 탐지.
- **부정행위 탐지**:
  - 시선 추적 및 머리 위치 계산.
  - 얼굴 비가시성, 화면 초점 이탈, 부적절한 시야각 감지.
- **시험 관리**:
  - 감독관은 다중 학생 화면을 동시에 모니터링.
  - 실시간 경고 시스템.

---

## **시스템 아키텍처**

<sup>**![System Architecture](https://github.com/user-attachments/assets/b1c341fa-9b8b-47c9-9f55-1bdfb4267f50)**</sup>
<sup>**![System Architecture](https://github.com/user-attachments/assets/d80a2da3-2dea-4793-9337-14f36db4cbff)**</sup>

---

## **기능 시연**

### 1. **로그인 및 회원가입**

<sup>**![image](https://github.com/user-attachments/assets/93f4fd7e-9c98-4fbd-a366-291715be06f8)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/b6f94721-e933-4361-844e-36b20411fdaa)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/430e5b50-9211-4256-b2ea-c71e8568fff9)**</sup>

### 2. **시험 생성**

<sup>**![image](https://github.com/user-attachments/assets/4ee03f61-1530-4d9f-81d2-073fa17b9c2b)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/ea38624f-be30-49b7-bf8b-bdddc07768f3)**</sup>

### 3. **시험 응시**

<sup>**![image](https://github.com/user-attachments/assets/cc3121b2-d933-495d-b708-3e6730b76589)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/617c34fb-3469-4aa1-af44-faf269fc8095)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/5908f398-364e-43e8-b1f4-8608d5514682)**</sup>

### 4. **시험 감독**

<sup>**![image](https://github.com/user-attachments/assets/82ee8f9d-45a4-4280-b385-a32e0d7e582f)**</sup>
<sup>**![image](https://github.com/user-attachments/assets/16986ac9-1da5-4431-aa19-8cb8d6cb6877)**</sup>

---

## **폴더 구조**

```plaintext
AntiCheating/
├── client.py                # 클라이언트 코드 (UI 및 웹캠 처리)
├── server.py                # 서버 코드 (소켓 통신 및 DB 처리)
├── cheat_detector.py        # 부정행위 탐지 모듈
├── ui/                      # PyQt5 UI 파일
│   ├── first.ui
│   ├── signup.ui
│   ├── createExam.ui
│   └── takeExam.ui
├── requirements.txt         # 필수 패키지 목록
└── README.md                # 프로젝트 설명
```

---

## **데모 영상**

<sup>[AntiCheating](https://youtu.be/cTiqiq_2mag)</sup>

## **문의**

질문이나 제안 사항이 있다면 아래로 연락 주세요  
이메일: columnwise99@gmail.com  
GitHub Issues를 통해서도 문의 가능합니다.
