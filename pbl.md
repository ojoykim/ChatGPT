
# Post Build Library (PBL)

Post Build Library는 **MCU의 Compile 이후 과정**에서 생성된 HEX 파일 및 소프트웨어 시그니처 정보를 기반으로  
**오류 없는 Hex / OTN / OTA 파일 생성을 자동화**하기 위한 Python 기반 도구입니다.

---

## 주요 목적

- Compile 완료 후 HEX 파일 및 관련 정보 기반 자동화
- OTN/OTA 생성 시 발생 가능한 수작업 실수 방지
- S/W 정보 시그니처 기반 MCU 상태 확인 및 패치 자동화

---

## 제공 기능

### 1. Hex File 생성

- **통합 HEX (Integration HEX)**
    - 여러 컴포넌트 또는 Bank를 통합한 Hex 파일 생성
- **OTN Test용 HEX**
    - OTN 테스트용으로 커스터마이징된 HEX 출력

### 2. OTN 파일 생성

- **OTN Server 등록용**
    - OTA 서버에 업로드할 수 있는 구조의 파일 패키징
- **HASS Update 용**
    - 스마트홈 연동을 위한 HASS 호환 OTA 패키지 생성

---

## MCU ROM 내 소프트웨어 서명 구조

MCU의 고정된 ROM 위치에 다음과 같은 **Software Signature 구조체**를 삽입하여  
펌웨어의 식별성과 무결성을 확보합니다.

### Signature 구성 항목

- `Software Info Signature` (예: `PBL_SIGNATURE`)
- `Project Name`
- `Version`
- `MCU` (예: STM32F407)
- `Bank Type` (Single / Dual)
- `Bootloader Length`
- `Build Date`
- `Assy Micom Code`
- `Class B CRC` (안전 검증용)

> 이 정보는 HEX 파일에 기록되며, PBL 툴에서 자동 분석/활용됩니다.

---

## 자동 파일 생성 흐름

1. **빌드 완료 후 HEX 파일 생성**
2. **Post Build 단계에서 `PBL` 실행**
3. HEX 파일에서 소프트웨어 서명 정보 추출
4. **OTA/OTN 파일 자동 생성**

```bash
# 예시 CLI 사용
pbl patch-info --input firmware.hex --version 1.2.3 --modelid ABC123 --firmcode 456789
pbl make-ota --input firmware.hex --output firmware_ota.zip
```

---

## 요약

- Post Build 자동화를 통해 실수 감소, 유지보수 효율 향상
- 시그니처 기반 소프트웨어 추적 가능
- OTA/OTN 생성 표준화로 배포 효율성 증가