좋습니다! 지금까지 설명한 내용을 바탕으로, MCU 펌웨어에 소프트웨어 정보를 포함하고 After Build에서 자동 패치 및 OTA 연동까지 가능한 전체 작업 명세서를 정리해 드릴게요.

펌웨어 소프트웨어 정보 내장 및 After Build 자동화 명세서

1. 목적

이 시스템은 Keil 기반의 MCU 펌웨어에서 소프트웨어 버전, 모델ID, 펌웨어 코드 등 핵심 정보를 펌웨어 이미지의 끝에 동적으로 포함시키고,
빌드 이후 Python 도구를 통해 HEX 파일을 가공 및 패치하여 OTA 시스템에 사용할 수 있는 형태로 자동 변환하는 것을 목표로 한다.

2. 전체 아키텍처 개요

[MCU 코드] → [Keil 빌드] → [FirmwareInfo 삽입] → [HEX 생성]
                                ↓
                        [After Build Script: hex_tool.py]
                                ↓
                      [HEX 패치 + OTA 패키지 생성]

3. MCU 소스 코드 설계

3.1 구조체 정의

typedef struct {
    char version[8];       // 예: "1.2.3"
    char model_id[8];      // 예: "K1234"
    uint32_t build_date;   // 예: 20250310
} FirmwareInfo;

3.2 ROM 위치 지정

__attribute__((section(".fwinfo"))) const FirmwareInfo fw_info = {
    .version = "1.2.3",
    .model_id = "K1234",
    .build_date = 20250310
};

4. 링커(Scatter) 파일 구성

LR_IROM1 0x08000000 0x00040000  {  ; 예: 256KB Flash

  ER_CODE 0x08000000 0x0003F000  {
    *.o (RESET, +First)
    .ANY (+RO +RW +ZI)
  }

  FWINFO 0x0803F000 0x00001000  {  ; 마지막 4KB에 fwinfo
    KEEP(*(.fwinfo))
  }
}

    .fwinfo는 코드의 마지막에 위치하며 KEEP()을 통해 최적화로 제거되지 않도록 설정.

5. 코드에서 접근 방법

#define FWINFO_ADDR ((const FirmwareInfo*) 0x0803F000)
printf("버전: %s\n", FWINFO_ADDR->version);

또는 링크 심볼 사용:

extern const FirmwareInfo __fwinfo_start__[];
#define FWINFO ((const FirmwareInfo*)__fwinfo_start__)

6. After Build Script (hex_tool.py)

주요 기능:
    •	HEX 파일에서 .fwinfo 위치 자동 추출 또는 고정 주소 접근
    •	특정 필드(version, model_id, build_date 등) 수정
    •	OTA용 메타데이터(metadata.json) 생성
    •	firmware_package.zip으로 묶는 OTA 파일 생성

사용 예시:

python hex_tool.py --input build.hex \
                   --patch-firmware-info version=1.2.4 model=ABC123 firmcode=FW567 \
                   --ota

7. Keil After Build 연동

Project 설정 → Options → User → After Build Command:

python hex_tool.py --input build\project.hex --ota

    빌드 시 자동으로 HEX 파일을 가공하고 OTA 패키지 생성

8. .map 파일 예시 (빌드 결과 확인)

Execution Region FWINFO (Base: 0x0803f000, Size: 0x00000020)
  fwinfo.o(.fwinfo)
  0803f000    00000020  fw_info
Symbol Table:
  0803f000  fw_info

    심볼 주소와 섹션 크기 등 .map 파일로 검증 가능

9. 향후 확장 가능 기능
    •	build_date 자동 삽입 (__DATE__/__TIME__ or CLI 전달)
    •	.bin 지원
    •	CRC, 서명(Signature) 추가
    •	GUI 메뉴 기반 도구 연동

이 명세서 기반으로 펌웨어 구조, 도구 개발, 빌드 연동까지 전체 구현 흐름을 잡을 수 있습니다.
필요하시면 .fwinfo에 CRC 추가, hex_tool.py 시작 코드 등도 바로 도와드릴게요!
추가 항목이 있다면 말씀해 주세요.