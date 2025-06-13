import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import re

st.title("📈 일차함수 그래프 생성기")
st.write("일차함수 식을 입력하세요 (예: `y = 2x + 1`)")

equation = st.text_input("일차함수 식 입력", value="y = 2x + 1")

def parse_equation(equation):
    equation = equation.replace(" ", "")
    match = re.match(r"y=([+-]?\d*)(x)([+-]?\d+)?", equation)
    if not match:
        return None, None
    a_str, _, b_str = match.groups()
    a = int(a_str) if a_str not in ("", "+", "-") else int(f"{a_str}1") if a_str else 1
    b = int(b_str) if b_str else 0
    return a, b

a, b = parse_equation(equation)

if a is not None:
    x = np.linspace(-5, 5, 400)
    y = a * x + b

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, label=f"y = {a}x + {b}", color="blue")

    # 축 교차 (0,0)에서
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 눈금 설정
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(np.arange(-5, 6, 1))
    ax.set_yticks(np.arange(-5, 6, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, linestyle='--', linewidth=0.5)

    # x절편
    if a != 0:
        x_intercept = -b / a
        if -5 <= x_intercept <= 5:
            ax.text(x_intercept, -0.4, f"{int(round(x_intercept))}", ha='center', va='top', color='red', fontsize=10)

    # y절편
    if -5 <= b <= 5:
        ax.text(0.4, b, f"{int(round(b))}", ha='left', va='center', color='green', fontsize=10)

    ax.set_title("일차함수 그래프")
    st.pyplot(fig)

    # 다운로드용 이미지 버퍼
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)

    st.download_button(
        label="📥 그래프 이미지 다운로드 (PNG)",
        data=buf,
        file_name="linear_function.png",
        mime="image/png"
    )
else:
    st.error("⚠️ 올바른 형식의 일차함수 식을 입력해주세요. 예: `y = -3x + 2`")
