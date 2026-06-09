import concurrent.futures
import time

import streamlit as st
from PIL import Image
from ocr_processor import process_pair

st.set_page_config(page_title="OCR Demo", layout="wide")

st.markdown("<h1 style='text-align:center'>📄 OCR ID Card Demo</h1>", unsafe_allow_html=True)

if 'processed' not in st.session_state:
    st.session_state['processed'] = False

if 'ocr_result' not in st.session_state:
    st.session_state['ocr_result'] = None


def _set_processed():
    st.session_state['processed'] = True
    st.session_state['ocr_result'] = None

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

        if st.session_state['ocr_result'] is None:
            status_placeholder = st.empty()
            with st.spinner("Processing both images..."):
                start_time = time.perf_counter()
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        process_pair,
                        front_image=front_image,
                        back_image=back_image,
                    )
                    while not future.done():
                        elapsed = int(time.perf_counter() - start_time)
                        status_placeholder.markdown(f"Processing both images... {elapsed}s")
                        time.sleep(0.2)
                    try:
                        st.session_state['ocr_result'] = future.result()
                    except Exception as e:
                        st.error(f"Error processing images: {str(e)}")
                        st.session_state['ocr_result'] = None
                elapsed = int(time.perf_counter() - start_time)
                status_placeholder.markdown(f"Processing both images... {elapsed}s")

        if st.session_state['ocr_result'] is not None:
            result = st.session_state['ocr_result']

            result_cols = st.columns([4, 2, 4])
            with result_cols[0]:
                st.markdown("<h3 style='text-align:center'>Input Images</h3>", unsafe_allow_html=True)
                st.markdown("**Mặt trước**")
                st.image(front_image, width='stretch')
                st.markdown("**Mặt sau**")
                st.image(back_image, width='stretch')

            with result_cols[2]:
                st.markdown("<h3 style='text-align:center'>OCR Result</h3>", unsafe_allow_html=True)
                st.json(result)

