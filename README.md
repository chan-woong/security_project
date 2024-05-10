-----------------------------------------------
# HACKER KID: 1.0.1 풀이
-----------------------------------------------
## 테스트 환경
- Oracle VM VirtualBox
  - HACKER KID: 1.0.1
  - 설치 경로 https://www.vulnhub.com/entry/hacker-kid-101,719/
 
  - kali-linux-2023.3
  - 설치 파일 kali-linux-2023.3-vmware-amd64.7z
-----------------------------------------------
## 목차
- 정보수집
  - 공격자 IP 확인
  - 공격 서버 IP 탈취
  - 웹페이지 분석
  - 하위 도메인 검색
- 취약점 공격
  - XXE 취약점으로 파일 탈취
  - SSTI 취약점으로 리버스 쉘 공격
- 권한 상승
  - 정보 수집
  - PID를 이용한 root 권한에 바인드 쉘 설치
  - root 권한 탈취
 
-----------------------------------------------

## 정보 수집

### 공격자 IP 확인
HACKER KID: 1.0.1는 ROOT권한을 탈취 하는 것을 목표로 하는 실습 환경이다.

각 단계별로 힌트가 숨겨져있어서 게임을 하는 식으로 풀이를 진행할수 있었다.

![ip확인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/c617aa4b-04d1-4f91-8bb1-33a3f6fbd63d)
![근접 네트워크 확인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/2cce9f6f-6e72-497f-8538-4a1dd896ade1)


### 공격 서버 IP 탈취
공격자 아이피를 확인하여 근접 네트워크를 검색한다.

![근접 네트워크 확인 5](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/daedd54f-59da-4b5e-bf51-5fe42dbba174)
![5-nmap -p 53,80,9999 -sV -sC 10 0 2 5](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/c0b244e2-0064-4a14-8f76-846b388fec72)

의심되는 IP의 포트 정보를 확인하여 정확한 공격 서버 특정 

확인 결과 공격 서버는 10.0.2.5 공격자는 10.0.2.4 서버를 사용하는 것으로 확인되었다.

공격 서버에는 80, 53, 9999번 포트가 열려있어 각각 확인해 보았다.

### 웹페이지 분석

![메인 페이지 80번 포트](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/8bf44cbc-3920-4e87-8238-4d481697729c)

80번 포트는 메인 페이지

![메인 페이지 9999번 포트](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/e5d71b52-4b9f-46f4-9aa7-24109042ae28)

9999번 포트는 로그인을 할수있는 페이지가 출력 되었다.

![메인 페이지 80번 포트-힌트](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/a1e0517c-c9f5-4070-a551-7acb7e3ee9b1)

![메인 페이지 힌트](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/05f64b4f-d69e-4b70-8c36-fba82afc3766)

메인 페이지의 대문자로 표시되어있는 DIG와 HTML코드 주석에 적혀있는 page_no를 통해

메인 페이지에 page_no에 관한 변수를 추가하여 진행해 보았다.

![버프 스위트 변수 추가](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/786616ea-5af3-4e8c-8b09-acca9ec3e400)

![버프 스위트 페이로드 추가](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/2e86aff8-f2b5-45ae-a566-f2e20834ba46)

![page_no 변수 추가한 결과 페이지](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/94d673b4-9521-4cd5-9c67-419306198218)

page_no=21을 추가하자 결과 데이터값이 달라진걸 확인 할수 있었고 메인 페이지 하단에 힌트 문자가 출력되어있었다.

이 힌트를 통해 hackers.blackhat.local 이라는 도메인을 확인 할수 있고 다른 서브 도메인의 존재 또한 알 수 있다.

### 하위 도메인 검색

![서브 도메인 도메인 파일에 추가](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/91b30030-61b6-4f43-b58a-0667307b7f28)

칼리의 hosts파일에 찾은 서브 도메인을 추가한뒤 다른 도메인을 찾아 보자

![하위 도메인 검색](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/48df1dea-013f-47b4-baa6-6d4f413d5fb8)

칼리 리눅스에서 DNS관련 정보를 찾은 많은 플러그인들이 있지만 여기서는 처음 메인페이지에 대문자로 적혀 있었던 DIG 명령어를 사용하였다.

위 작업을 통해 또 다른 hackerkid.blackhat.local 이라는 도메인을 확인하였고 이 도메인 역시 칼리 hosts 파일에 추가해 주었다.


----------------------------------------------
## 취약점 공격

### XXE 취약점으로 파일 탈취

![21-xml형식으로 email이 반영되는걸 확인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/213b5fb2-3f6f-4b3b-9e3e-8d10608befef)

표시된 도메인에 접속하니 회원가입 페이지가 표시되었고 임의값을 입력하니 오류메시지가 출력 되었다.

오류 메시지를 잘 보면 회원가입 데이터의 이메일 데이터가 오류페이지에 그대로 표시되는걸 확인할수 있다.

![23-xxe공격시도](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/327e85f7-af92-4122-8e92-fb5d6f8028d2)

해당 정보를 통해 XXE 취약점이 존재하고 여러 테스트를 통해 서버의 파일을 탈취할수 있다.

유저 정보를 탈취하였고 그 정보를 토대로 saket 유저가 존재하고 /home/saket 폴더에 ubuntu 설정 파일의 유무를 추측할수 있다.

![24-xxe내부의php필터](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/dd9f3dad-8cb5-4dd1-8f8a-c8e5f76434a9)
![유저정보 탈취](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/113b63ad-705f-44d5-a36b-9e1ef5a40c46)

설정 파일의 정보에서 admin/Saket!#$%@!!이라는 유저정보를 알수있다.

### SSTI 취약점으로 리버스 쉘 공격

![admin로그인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/29d3f595-4487-4393-8ecc-d9ea9823e717)
![로그인 실패](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/f4eb3460-6220-48b6-999a-30c65f38df8b)

처음에 얻었던 9999번 포트의 로그인 페이지에 해당 정보를 입력하니 로그인이 실패하였다.

![saket회원 로그인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/d4de32b4-7759-4850-a898-fdc0b7caff48)
![로그인 성공](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/4fa77b71-77f3-4f7e-b8e6-0e68c5211702)

유저의 이름을 admin이 아닌 saket로 진행하니 로그인이 성공하였고 

name이라는 변수를 사용하라는 힌트가 표시됬다.

![name 변수 추가](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/0e2d1426-f664-43d7-9195-d11c0f155a4a)

name 변수를 통해 화면에 name변수가 그대로 출력되는것 확인한뒤 다양한 정보을 넣어보았다.

![xss 공격](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/084c8dce-0647-4305-8f99-241c2b0c1770)
![SSTI 공격 가능](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/6fd2a5c0-4a49-4b4d-84b5-f85466339cd7)

또한 템플릿 코드 또한 사용이 가능하다.

![33-리버스쉘 인코딩](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/574a7c0a-a650-403f-b36d-2c740ef515b2)

9999번 포트가 파이선 Tornado를 사용하고 있는걸 알고 있기에 해당 코드를 통해 리버스 쉘을 통한 접근이 가능하다.

----------------------------------------------
## 권한 상승

### 정보 수집

![35-getcap 사용](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/ce4ceb24-5772-4b37-a54a-3fa159067783)

getcap 명령을 사용하여 서버의 기본적인 정보를 수집하였다.


### PID를 이용한 root 권한에 바인드 쉘 설치

권한상승 방법 중 root 권한에서 실행된 프로세스를 탈취하여 하위 프로세스에 바인드 쉘을 설치가 목표이다.

![36-실행중인 서비스중 root 권한을 사용하는 것 확인](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/cfe1ea8e-b4ca-41b3-afa0-b163ea82a1b0)

getcap의 정보와 프로세스 정보를 통해서 apache2 가 실행 중이다.

![바인드 웹셀 생성 코드 다운로드](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/d6c492e0-4c4a-45f5-8273-2e10c5099cac)

파이선 2.7 버전의 코드로 작성한 바인드 쉘 코드를 다운 받아 사용한다.

코드출처 : https://xz.aliyun.com/t/13182?time__1311=mqmxnDBDcD2AG%3DqDsD7mQ0%3Dt%2B%2B%2BzYeWe4D&alichlgref=https%3A%2F%2Fwww.google.com%2F

![바인딩 웹쉘 생성완료](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/55156015-f432-4ac1-a0e1-4fa60ac2b2b4)

다운 받은 코드를 root 권한에서 실행 중인 프로세스 ID를 사용하여 바인드 쉘을 실행 할수 있다.

### root 권한 탈취

![루트 권한 탈취 성공!!!!](https://github.com/chan-woong/security_project_HACKER-KID-1.0.1/assets/70797394/c8c5906f-ccf7-44fa-8584-8850f6df725d)

공격자가 바인드 쉘에 접속한다면 root권한을 얻을수 있다.







