#!/usr/bin/env python3
"""
PDF 생성 헬퍼 스크립트
Python One-Liners Cheat Sheet을 PDF로 변환합니다.
"""

import os
from pathlib import Path

def generate_pdf():
    """Markdown을 PDF로 변환 (pandoc 필요)"""
    
    base_dir = Path(__file__).parent
    input_file = base_dir / "python-one-liners-cheat-sheet.md"
    output_file = base_dir / "python-one-liners-cheat-sheet.pdf"
    
    if not input_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        return False
    
    # pandoc 설치 확인
    if os.system("which pandoc > /dev/null 2>&1") != 0:
        print("❌ pandoc이 설치되지 않았습니다.")
        print("\n설치 방법:")
        print("  macOS: brew install pandoc")
        print("  Ubuntu: sudo apt install pandoc")
        print("\n또는 온라인 도구 사용:")
        print("  - https://md2pdf.netlify.app")
        print("  - https://www.markdowntopdf.com")
        return False
    
    print("📄 PDF 생성 중...")
    cmd = f'pandoc "{input_file}" -o "{output_file}" --pdf-engine=xelatex'
    
    result = os.system(cmd)
    
    if result == 0:
        print(f"✅ PDF 생성 완료: {output_file}")
        return True
    else:
        print(f"❌ PDF 생성 실패 (exit code: {result})")
        return False

if __name__ == "__main__":
    print("🐍 Python One-Liners Cheat Sheet PDF 생성기\n")
    
    success = generate_pdf()
    
    if success:
        print("\n다음 단계:")
        print("1. PDF 파일을 Gumroad에 업로드")
        print("2. 상품 URL 확인: jacksonstudio.gumroad.com/l/python-one-liners")
        print("3. Dev.to 링크 테스트")
    else:
        print("\n대안:")
        print("1. Gumroad에 markdown 파일 직접 업로드")
        print("2. 온라인 도구로 PDF 변환 후 업로드")
