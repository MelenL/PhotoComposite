import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="PhotoComposite 10x15 Optimizer", layout="centered")

# --- PRINT SETTINGS ---
FINAL_W, FINAL_H = 1800, 1200
MARGIN = 10

# Configuration for different layouts: (columns, rows)
GRID_CONFIG = {
    2: (2, 1),  # 2 columns, 1 row
    4: (2, 2),  # 2 columns, 2 rows
    8: (4, 2)  # 4 columns, 2 rows
}


def process_image(uploaded_file, target_w, target_h):
    """Resizes and rotates images to fit a grid cell without cropping."""
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)

    if img.height > img.width:
        img = img.rotate(90, expand=True)

    canvas = Image.new('RGB', (int(target_w), int(target_h)), (255, 255, 255))
    img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

    offset_x = int((target_w - img.width) // 2)
    offset_y = int((target_h - img.height) // 2)
    canvas.paste(img, (offset_x, offset_y))

    return canvas


# --- USER INTERFACE ---
st.title("PhotoComposite 10x15")

# Sidebar for parameters
with st.sidebar:
    st.header("Settings")
    division = st.selectbox("Photos per sheet", [2, 4, 8], index=1)
    st.write(f"Layout: {GRID_CONFIG[division][0]} columns x {GRID_CONFIG[division][1]} rows")

# Calculate sub-dimensions based on selection
cols, rows = GRID_CONFIG[division]
SUB_W = (FINAL_W - (cols - 1) * MARGIN) // cols
SUB_H = (FINAL_H - (rows - 1) * MARGIN) // rows

st.write(f"Upload your photos to generate {division}-in-1 print sheets.")

uploaded_files = st.file_uploader("Choose your photos",
                                  accept_multiple_files=True,
                                  type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_files:
    st.info(f"{len(uploaded_files)} photos selected.")

    if st.button("Generate Print Sheets"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            sheet_count = 0

            # Process files in batches based on division
            for i in range(0, len(uploaded_files), division):
                sheet = Image.new('RGB', (FINAL_W, FINAL_H), (255, 255, 255))
                batch = uploaded_files[i:i + division]

                for idx, file in enumerate(batch):
                    # Calculate grid position
                    col_idx = idx % cols
                    row_idx = idx // cols

                    pos_x = col_idx * (SUB_W + MARGIN)
                    pos_y = row_idx * (SUB_H + MARGIN)

                    processed_img = process_image(file, SUB_W, SUB_H)
                    sheet.paste(processed_img, (int(pos_x), int(pos_y)))

                sheet_count += 1
                img_io = io.BytesIO()
                sheet.save(img_io, format='JPEG', quality=95)
                zip_file.writestr(f"print_sheet_{sheet_count}.jpg", img_io.getvalue())

        st.success(f"{sheet_count} print sheets successfully generated!")

        st.download_button(
            label="Download ZIP Archive",
            data=zip_buffer.getvalue(),
            file_name="photocomposite_sheets.zip",
            mime="application/zip"
        )