# 📲 카카오톡 디벨로퍼스 설정 및 메시지 API 송신

## 1️⃣ 카카오 디벨로퍼스 앱 설정

### 🔧 앱 생성

1. [Kakao Developers](https://developers.kakao.com/)에 로그인
2. 상단 메뉴에서 **내 애플리케이션 > 애플리케이션 추가**
3. 앱 이름 입력 후 생성

### 🔐 REST API 키 확인

1. **앱 > 앱 설정 > 앱 > 일반**
2. REST API 키: 복사

### ⚙️ 플랫폼 등록

1. **앱 > 앱 설정 > 앱 > 일반**
2. 웹 플랫폼 등록
3. 사이트 도메인 등록: `http://localhost:5000`
   > ✅ **서버 릴리스** URI를 HTTPS로 변경

### 🔐 카카오 로그인 활성화

1. **앱 > 제품 설정 > 카카오 로그인 > 일반**
2. 사용상태: ON
3. 리다이렉트 URI 등록: `http://localhost:5000/kakao/oauth`
   > ⚠️ **리다이렉트 URI** 카카오 인증할 때만 필요(매회 인증코드 발행하지 않기 위해)
4. Client Secret: 보안 강화, 임의 설정

---

## 2️⃣ 메시지 API 사용 권한 설정

### 권한 설정

1. **앱 > 제품 설정 > 카카오 로그인 > 동의항목**
2. ✅ 권한 동의 항목 설정

| 권한           | ID               | 상태         | 비고                        |
| -------------- | ---------------- | ------------ | --------------------------- |
| 메시지 전송    | **talk_message** | 선택 동의    | 카카오톡 메시지 전송        |
| 친구 목록 조회 | **friends**      | 이용 중 동의 | 친구에게 메시지 전송시 필요 |

### 토큰 발행

1. 인증코드 URL 엑세스
2. 메시지 전송 권한 동의를 요청하는 화면이 표시
3. 동의하면 앱으로 리다이렉트되며, 인증 코드가 전달
4. 앱은 인증 코드를 이용해 액세스 토큰을 발급

> ⚠️ **권한 동의** 카카오톡 메시지 전송 권한에 동의해야 메시지전송 가능

---

## 3️⃣ 메시지 API 송신

### 📤 나에게 메시지 보내기 (기본 템플릿)

#### ✅ 요청 URL

```
POST https://kapi.kakao.com/v2/api/talk/memo/default/send
```

#### 🧾 요청 헤더

```http
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/x-www-form-urlencoded;charset=utf-8
```

#### 🧱 요청 바디 예시

```json
template_object={
  "object_type": "feed",
  "content": {
    "title": "오늘의 디저트",
    "description": "아메리카노, 빵, 케익",
    "image_url": "https://example.com/image.jpg",
    "image_width": 640,
    "image_height": 640,
    "link": {
      "web_url": "https://www.daum.net",
      "mobile_web_url": "http://m.daum.net"
    }
  }
}
```

<!-- #### 🖥️ CURL 예시

```bash
curl -v -X POST "https://kapi.kakao.com/v2/api/talk/memo/default/send" \
-H "Authorization: Bearer {ACCESS_TOKEN}" \
-H "Content-Type: application/x-www-form-urlencoded;charset=utf-8" \
--data-urlencode 'template_object={...}'
``` -->

---

## 4️⃣ 친구에게 메시지 보내기

> ⚠️ **추가 권한 신청 필요**: 친구 목록 조회 및 메시지 전송 권한

### 주요 절차

1. 친구 목록 조회 API 사용
2. 수신 대상 선택
3. 메시지 전송 API 호출

> ⚠️ **쿼터 제한**: 한 번에 최대 5명에게 전송 가능, 일일30건

---

### 팀원등록

1. **앱 > 앱 설정 > 앱 > 멤버 > 멤버 추가**
2. 초대할 멤버의 이메일 주소(카카오톡 계정) 입력
3. 앱 권한 설정 (**Editor** / Message Editor / Viewer)
4. 팀원: 카카오톡 계정 이메일에서 팀원 초대 메일 확인
5. 팀원: 1회 이상 로그인 필요 (목적: 메시지 수신 권한에 동의 체크)

## 📚 참고 문서

- [🔧카카오 API 시작하기 튜토리얼](https://developers.kakao.com/docs/latest/ko/tutorial/start)
- [🔧카카오톡 메시지 REST API 공식 문서](https://developers.kakao.com/docs/latest/ko/kakaotalk-message/rest-api)
- [🔧카카오 앱](https://developers.kakao.com/console/app)
- [[Python] FastAPI로 카카오톡 메시지 전송](https://dev-grace.tistory.com/)
