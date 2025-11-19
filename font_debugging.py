import matplotlib.font_manager as fm
from matplotlib import rcParams
import os

print("--- 폰트 캐시 재생성 및 나눔 폰트 이름 확인 ---")

# 폰트 매니저 강제 로드 (캐시 파일이 없으므로 새로 생성됩니다)
# 이것이 폰트를 재스캔하는 핵심 과정입니다.
fm._load_fontmanager(try_read_cache=False)
print("✅ 폰트 매니저 재생성 및 폰트 스캔 완료.")


print("\n--- 설치된 나눔 폰트 이름 확인 ---")
nanum_fonts = []
for font in fm.fontManager.ttflist:
    # 'Nanum'이 포함된 폰트 이름을 찾습니다.
    if 'Nanum' in font.name:
        nanum_fonts.append(font.name)

# 중복 제거
unique_nanum_fonts = sorted(list(set(nanum_fonts)))

if unique_nanum_fonts:
    print("✅ Matplotlib이 인식하는 나눔 폰트 목록:")
    for name in unique_nanum_fonts:
        print(f"- **{name}**")
    
    # 목록에서 NanumGothic을 찾거나, 가장 흔한 이름을 선택
    final_font_name = 'NanumGothic' if 'NanumGothic' in unique_nanum_fonts else unique_nanum_fonts[0]
    
    if 'NanumGothic' in final_font_name:
        print("\n💡 가장 흔히 사용되는 **NanumGothic**을 최종 폰트로 지정합니다.")
    else:
        print(f"\n💡 목록의 첫 번째 폰트 이름인 **{final_font_name}**을 최종 폰트로 지정합니다.")
    
    # 폰트 설정
    rcParams['font.family'] = final_font_name 
    rcParams['axes.unicode_minus'] = False 
    print(f"✅ Matplotlib 폰트 설정 완료: {final_font_name}")

else:
    print("⚠️ 폰트 캐시 재생성 후에도 나눔 폰트가 인식되지 않았습니다. 폰트 설치 경로를 확인해봐야 합니다.")
    # 임시 설정
    rcParams['font.family'] = 'sans-serif' 
    rcParams['axes.unicode_minus'] = False