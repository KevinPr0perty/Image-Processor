import os
import tempfile
from PIL import Image
import streamlit as st

PPI = 72
MAX_WIDTH_PX = int(35 * PPI)     # 35 cm in pixels
MAX_HEIGHT_PX = int(45 * PPI)    # 45 cm in pixels
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".tif", ".bmp")

# --- Resize while maintaining aspect ratio ---
def resize_to_fit(image, max_width, max_height):
    width, height = image.size
    if width <= max_width and height <= max_height:
        return image

    ratio = min(max_width / width, max_height / height)
    new_size = (int(width * ratio), int(height * ratio))
    return image.resize(new_size, Image.LANCZOS)

# --- Streamlit UI ---
st.title("Batch Image Processor - 72 PPI, Max 35x45 cm")

uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png", "tif", "bmp"], accept_multiple_files=True)

if uploaded_files:
    output_dir = tempfile.mkdtemp()
    st.write(f"Processed images will be saved to: `{output_dir}`")

    for uploaded_file in uploaded_files:
        with Image.open(uploaded_file) as img:
            img = img.convert("RGB")
            img = resize_to_fit(img, MAX_WIDTH_PX, MAX_HEIGHT_PX)

            output_path = os.path.join(output_dir, uploaded_file.name)
            img.save(output_path, dpi=(PPI, PPI))

            st.success(f"Processed: {uploaded_file.name}")
            st.image(img, caption=uploaded_file.name, use_column_width=True)

    st.info("All images processed and saved in temporary directory.")
else:
    st.warning("Please upload images to process.")
