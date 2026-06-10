import streamlit as st

st.title("Đánh giá khả năng trích xuất thông tin của hệ thống")

# =========================
# Dataset
# =========================
st.subheader("Dữ liệu thử nghiệm")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Tổng số hình ảnh", "553")

with c2:
    st.metric("Mặt trước", "350")
    st.caption("63.3%")

with c3:
    st.metric("Mặt sau", "203")
    st.caption("36.7%")

#st.caption(
#    "Evaluation conducted on 553 Vietnamese ID card images "
#    "(350 front-side, 203 back-side)."
#)

st.divider()

# =========================
# Evaluation Setup
# =========================
st.subheader("Phương pháp đánh giá: LLM-as-a-Judge")

st.code(
    """
Gemini 2.5 Flash (~400 tỷ tham số)
              │
              ▼
         LLM-as-a-Judge
              ▲
              │
      Mô hình OCR của chúng tôi (1 tỷ tham số)
""",
    language="text",
)

st.info(
    "Nhờ một chuyên gia (Gemini 2.5 Flash) đánh giá kết quả trích xuất thông tin bởi hệ thống của chúng tôi"
)

st.divider()

# =========================
# Accuracy
# =========================
st.subheader("Độ chính xác tổng quan")

st.metric(
    label="Trung bình điểm được chấm trên tất cả các ảnh",
    value="95.18 / 100"
)

#st.success(
#    "The 1B-parameter OCR model achieved 95.18% average accuracy "
#    "across 553 ID card images."
#)

st.divider()

st.subheader("Trung bình độ trễ phản hồi")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        'Chờ phản hồi mặt trước',
        '13.26s'
    )

with c2:
    st.metric(
        'Chờ phản hồi mặt sau',
        '8.41s'
    )

st.divider()

# =========================
# Evaluation Statistics
# =========================
st.subheader("Các thông số của quá trình đánh giá")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Trung bình số đơn vị tính toán gửi đi",
        "1,484.48"
    )

with c2:
    st.metric(
        "Trung bình số đơn vị tính toán nhận về",
        "160.93"
    )

with c3:
    st.metric(
        "Độ trễ của mỗi lần đánh giá",
        "1.75s"
    )

#st.caption(
#    "Average metrics per evaluation request."
#)
