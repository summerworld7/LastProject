import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import re

st.title("📈 일차함수 그래프 생성기")
st.write("아래 입력창에 일차함수 식을 입력하세요. (예: `y = 2x + 1`)")

# 함수 입력
equation = st.text_input("일차함수 식 입력", value="y = 2x + 1")

# 식 파싱 함수
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
    # x, y 값 계산
    x = np.linspace(-10, 10, 400)
    y = a * x + b

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, label=f"y = {a}x + {b}", color="blue")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("일차함수 그래프")
    ax.legend()

    # Streamlit에 출력
    st.pyplot(fig)

    # 이미지 다운로드용 버퍼
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
