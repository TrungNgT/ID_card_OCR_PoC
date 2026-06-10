import concurrent.futures
import time

import streamlit as st
from PIL import Image
from ocr_processor import process, fit_image, parse_front, parse_back

def render_front_result(data):
    st.markdown("### Thông tin CCCD")

    st.markdown(f"**Số CCCD:** {data.get('so', '')}")
    st.markdown(f"**Họ và tên:** {data.get('ho_va_ten', '')}")
    st.markdown(f"**Ngày sinh:** {data.get('ngay_sinh', '')}")
    st.markdown(f"**Giới tính:** {data.get('gioi_tinh', '')}")
    st.markdown(f"**Quốc tịch:** {data.get('quoc_tich', '')}")
    st.markdown(f"**Quê quán:** {data.get('que_quan', '')}")
    st.markdown(f"**Địa chỉ thường trú:** {data.get('dia_chi_thuong_tru', '')}")

def render_back_result(data):
    st.markdown("### Thông tin bổ sung")

    st.markdown(
        f"**Đặc điểm nhận dạng:** {data.get('dac_diem_nhan_dang', '')}"
    )

    st.markdown(
        f"**Ngày cấp:** {data.get('ngay_cap', '')}"
    )

st.set_page_config(page_title="OCR Demo", layout="wide")

st.markdown("<h1 style='text-align:center'>📄 OCR ID Card Demo</h1>", unsafe_allow_html=True)

if 'processed' not in st.session_state:
    st.session_state['processed'] = False

if 'front_result' not in st.session_state:
    st.session_state['front_result'] = None

if 'back_result' not in st.session_state:
    st.session_state['back_result'] = None


def _set_processed():
    st.session_state['processed'] = True
    st.session_state['front_result'] = None
    st.session_state['back_result'] = None

col1, col2 = st.columns(2)
with col1:
    st.subheader("Mặt trước")
    front_file = st.file_uploader(
        "Upload front image",
        type=["jpg", "jpeg", "png"],
        key="front_file"
    )
    #front_prompt = st.text_area(
    #    "Prompt (mặt trước)",
    #    value="Extract text from the front side of the ID card.",
    #    key="front_prompt",
    #    height=120
    #)

with col2:
    st.subheader("Mặt sau")
    back_file = st.file_uploader(
        "Upload back image",
        type=["jpg", "jpeg", "png"],
        key="back_file"
    )
    #back_prompt = st.text_area(
    #    "Prompt (mặt sau)",
    #    value="Extract text from the back side of the ID card.",
    #    key="back_prompt",
    #    height=120
    #)

process_button_cols = st.columns([3, 4, 3])
with process_button_cols[1]:
    st.write("")
    st.button(
        "🚀 Process",
        type="primary",
        on_click=_set_processed,
        width='stretch'
    )

if st.session_state['processed']:
    if front_file is None or back_file is None:
        st.warning("Please upload both the front and back images before processing.")
    else:
        front_image = Image.open(front_file).convert("RGB")
        back_image = Image.open(back_file).convert("RGB")

        # =========================
        # FRONT
        # =========================
        st.markdown("## Mặt trước")

        front_img_col, front_result_col = st.columns([1, 1])

        with front_img_col:
            st.image(fit_image(front_image))

        with front_result_col:
            front_result_placeholder = st.empty()

            if st.session_state['front_result'] is not None:
                front_result_placeholder.json(
                    st.session_state['front_result']
                )
            else:
                front_status = st.empty()

                with st.spinner("Processing front image..."):
                    start_time = time.perf_counter()

                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(process, front_image, 0)

                        while not future.done():
                            elapsed = int(time.perf_counter() - start_time)
                            front_status.markdown(
                                f"⏳ Processing front image... {elapsed}s"
                            )
                            time.sleep(0.2)

                        try:
                            st.session_state['front_result'] = future.result()

                            elapsed = int(time.perf_counter() - start_time)
                            front_status.success(
                                f"✅ Front image processed in {elapsed}s"
                            )

                            render_front_result(parse_front(st.session_state['front_result']))

                        except Exception as e:
                            st.error(f"Error processing front image: {e}")
                            st.session_state['front_result'] = None

        st.divider()

        # =========================
        # BACK
        # =========================
        st.markdown("## Mặt sau")

        back_img_col, back_result_col = st.columns([1, 1])

        with back_img_col:
            st.image(fit_image(back_image))

        with back_result_col:
            back_result_placeholder = st.empty()

            if st.session_state['back_result'] is not None:
                back_result_placeholder.json(
                    st.session_state['back_result']
                )

            elif st.session_state['front_result'] is not None:
                back_status = st.empty()

                with st.spinner("Processing back image..."):
                    start_time = time.perf_counter()

                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(process, back_image, 1)

                        while not future.done():
                            elapsed = int(time.perf_counter() - start_time)
                            back_status.markdown(
                                f"⏳ Processing back image... {elapsed}s"
                            )
                            time.sleep(0.2)

                        try:
                            st.session_state['back_result'] = future.result()

                            elapsed = int(time.perf_counter() - start_time)
                            back_status.success(
                                f"✅ Back image processed in {elapsed}s"
                            )

                            render_back_result(parse_back(st.session_state['back_result']))

                        except Exception as e:
                            st.error(f"Error processing back image: {e}")
                            st.session_state['back_result'] = None


