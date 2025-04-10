# cmake/abov_toolchain.cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# Keil 설치 경로에 따라 수정하세요
set(ARMCC_PATH "C:/Keil_v5/ARM/ARMCC/bin")

set(CMAKE_C_COMPILER "${ARMCC_PATH}/armcc.exe")
set(CMAKE_ASM_COMPILER "${ARMCC_PATH}/armasm.exe")
set(CMAKE_LINKER "${ARMCC_PATH}/armlink.exe")
set(CMAKE_AR "${ARMCC_PATH}/armar.exe")

# 컴파일 옵션
set(CMAKE_C_FLAGS "--cpu Cortex-M0 -g --apcs=interwork --split_sections --c99")
set(CMAKE_ASM_FLAGS "--cpu Cortex-M0")
set(CMAKE_EXE_LINKER_FLAGS "--scatter=linker/a34m420.sct --info sizes --info totals --map")

# 확장자 설정 (Keil의 fromelf는 .axf를 .hex로 변환함)
set(CMAKE_EXECUTABLE_SUFFIX ".elf")