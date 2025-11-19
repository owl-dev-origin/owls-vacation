import streamlit as st

# st.title("🎈Owls vacation")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
from datetime import datetime
import matplotlib.font_manager as fm

# 데이터 불러오기
use_data_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSoSeQ-ieKryWqCXKqMNZ4GZunnBPGnC_Ici4YDomIRk-huOBDCzeQ8wp0SkLkxGO4x_rRwoKmU48hk/pub?gid=0&single=true&output=csv'
df_a = pd.read_csv(use_data_url)
df_a["기안일"] = pd.to_datetime(df_a["기안일"]).dt.date
df_a["사용일"] = pd.to_datetime(df_a["사용일"]).dt.date

base_data = {
    "이름": ["정원선", "신해원", "김경숙", "신지희", "원희정", "진미혜", "고혜림"],
    "기준일": ["2025-09-17", "2022-11-02", "2022-07-14", "2022-02-17", "2025-06-02", "2025-11-03", "2024-04-25"]
}
df_b = pd.DataFrame(base_data)
df_b["기준일"] = pd.to_datetime(df_b["기준일"]).dt.date

# 1. 입사일 기준 정렬
df_b['정렬용_월일'] = df_b["기준일"].apply(lambda x: (x.month, x.day))
ordered_names = df_b.sort_values("정렬용_월일")["이름"].tolist()
latest_df = df_a.sort_values("기안일").groupby("이름").tail(1)
latest_df = latest_df.set_index("이름").reindex(ordered_names).reset_index()

# ordered_names = df_b.sort_values("기준일")["이름"].tolist()
# latest_df = df_a.sort_values("기안일").groupby("이름").tail(1)
# latest_df = latest_df.set_index("이름").reindex(ordered_names).reset_index()


# 2. 가로 막대그래프 시각화
# st.subheader("구성원별 연차 사용/남은 연차 현황")
st.markdown("입사일 기준으로 연차의 사용 현황을 시각화합니다. 각자의 연차 갱신일은 그래프의 오른쪽 축을 참고해주세요.")
st.markdown("연차 갱신일은 입사일을 기준으로 매년 동일한 월, 일에 갱신됩니다.")
st.markdown("연차 갱신일이 빠른 순서대로 정렬되어 있습니다.")

# # 한글 폰트 설정 (Pretendard)
# font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"  # Pretendard 경로
# font_prop = fm.FontProperties(fname=font_path)
# print(font_prop.get_name())

rcParams['font.family'] = 'NanumGothic' #font_prop.get_name()
rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(15, 7))
# plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

names = latest_df["이름"]
used = latest_df["총 소진량"]
remaining = latest_df["남은연차수"]
total = latest_df["보유연차수"]

current_year = datetime.now().year
# 기준일에서 월, 일을 가져와 현재 연도 + 1년으로 갱신일 생성
def make_renewal_date(date):
    # 월, 일 유지, 연도는 현재년도 + 1
    return datetime(current_year + 1, date.month, date.day).strftime('%Y-%m-%d')
merged_df = latest_df.merge(df_b, on="이름")
renewal_dates = merged_df["기준일"].apply(make_renewal_date)
# hire_dates = latest_df.merge(df_b, on="이름")["기준일"].dt.strftime('%Y-%m-%d')

bar_height = 0.5

# 가로 막대: 사용 연차(회색)
ax.barh(names, used, color='#e4e1dd', label='사용 연차', height=bar_height) # edgecolor='black',

# 가로 막대: 남은 연차(민트)
ax.barh(names, remaining, left=used, color='#39f3aa', label='남은 연차', height=bar_height) # edgecolor='black',

# 막대 위에 숫자 표시
for i, (u, r) in enumerate(zip(used, remaining)):
    ax.text(u/2, i, f"{u:.2f}", va='center', ha='center', color='black', fontsize=15)  # 사용 연차
    ax.text(u + r/2, i, f"{r:.2f}", va='center', ha='center', color='black', fontsize=15)  # 남은 연차

ax.invert_yaxis()  # 가장 많은 연차가 위로

# 그래프 디테일 설정
ax.spines['top'].set_visible(False)
ax.tick_params(axis='y', which='major', labelsize=20)

# 오른쪽 기준일 y축 추가
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())  # 왼쪽 y축 범위와 맞추기
ax2.set_yticks(range(len(names)))  # y축 위치
ax2.set_yticklabels(renewal_dates)  # y축 라벨을 입사일로
# ax2.set_ylabel("갱신일")
ax2.tick_params(axis='y', which='major', labelsize=20)
ax2.spines['top'].set_visible(False)

ax.legend(loc='upper left', bbox_to_anchor=(1.15, 1), frameon=False, fontsize=12)

plt.subplots_adjust(left=0.08, right=0.85, bottom=0.08, top=0.95)

st.pyplot(fig)

# 3. 개인별 상세 이력 조회
st.subheader("개인별 상세 이력 조회")
selected_member = st.selectbox("구성원을 선택하세요", df_a["이름"].unique())
member_df = df_a[df_a["이름"] == selected_member]
st.dataframe(member_df)

