from intelhex import IntelHex

def patch_hex_file(input_path, output_path, signature: bytes, offset_from_sig: int, new_value: bytes):
    hexfile = IntelHex()
    hexfile.loadhex(input_path)

    # 1. 메모리 영역 전체 검색
    start_addr = min(hexfile.addresses())
    end_addr = max(hexfile.addresses())
    mem = bytes([hexfile[addr] for addr in range(start_addr, end_addr + 1)])

    # 2. 시그니처 찾기
    sig_index = mem.find(signature)
    if sig_index == -1:
        print("❌ 시그니처를 찾을 수 없습니다.")
        return

    print(f"✅ 시그니처 위치: 0x{start_addr + sig_index:X}")

    # 3. 변경할 주소 계산
    target_addr = start_addr + sig_index + offset_from_sig

    for i, b in enumerate(new_value):
        hexfile[target_addr + i] = b

    # 4. 결과 저장
    hexfile.write_hex_file(output_path)
    print(f"✅ 수정된 HEX 파일이 '{output_path}'에 저장되었습니다.")

# 사용 예시
patch_hex_file(
    input_path="input.hex",
    output_path="patched.hex",
    signature=bytes.fromhex("DE AD BE EF"),
    offset_from_sig=4,
    new_value=bytes.fromhex("12 34")
)


from intelhex import IntelHex

def patch_null_terminated_strings(
    hex_path,
    output_path,
    start_addr,
    length,
    replacements  # 딕셔너리 형태: {index: "new string"}
):
    ih = IntelHex(hex_path)

    # 데이터 읽기
    raw = bytes([ih.get(addr, 0x00) for addr in range(start_addr, start_addr + length)])

    # 문자열 분리
    parts = raw.split(b'\x00')

    # 디코딩 (빈 문자열 제외)
    decoded = [p.decode('utf-8', errors='ignore') for p in parts if p or len(p) == 0]

    print(f"🧵 원본 문자열 리스트: {decoded}")

    # 문자열 변경
    for index, new_str in replacements.items():
        if 0 <= index < len(decoded):
            decoded[index] = new_str
            print(f"🔁 {index+1}번째 문자열 → '{new_str}' 로 변경")
        else:
            print(f"⚠️ {index+1}번째 문자열이 존재하지 않음!")

    # 다시 NULL-terminated 문자열로 인코딩
    new_data = b'\x00'.join(s.encode('utf-8') for s in decoded) + b'\x00'

    # 메모리에 덮어쓰기
    for i, b in enumerate(new_data):
        ih[start_addr + i] = b

    # 저장
    ih.write_hex_file(output_path)
    print(f"✅ 수정된 HEX 파일 저장 완료: {output_path}")

# 사용 예시
patch_null_terminated_strings(
    hex_path="input.hex",
    output_path="patched.hex",
    start_addr=0x2000,
    length=128,
    replacements={
        2: "NewThird",   # 3번째 문자열 (index는 0부터 시작)
        4: "ChangedFifth"
    }
)
