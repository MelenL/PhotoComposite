import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="PhotoComposite 10x15 Optimizer", layout="centered")

# --- PRINT SETTINGS ---
# 10x15cm at 300 DPI is approximately 1800x1200 pixels
FINAL_W, FINAL_H = 1800, 1200
MARGIN = 10
SUB_W = (FINAL_W - MARGIN) // 2
SUB_H = (FINAL_H - MARGIN) // 2


def process_image(uploaded_file, target_w, target_h):
    """Resizes and rotates images to fit a 2x2 grid without cropping."""
    img = Image.open(uploaded_file)
    # Correct orientation based on EXIF data
    img = ImageOps.exif_transpose(img)

    # Auto-rotate portrait images to landscape to fit the grid cell
    if img.height > img.width:
        img = img.rotate(90, expand=True)

    # Create white background for the cell
    canvas = Image.new('RGB', (target_w, target_h), (255, 255, 255))

    # Proportional resize (thumbnail ensures no cropping)
    img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

    # Center the image in the cell
    offset_x = (target_w - img.width) // 2
    offset_y = (target_h - img.height) // 2
    canvas.paste(img, (offset_x, offset_y))

    return canvas


# --- USER INTERFACE ---
st.title("📸 PhotoComposite 10x15")
st.write("Upload your photos to generate 4-in-1 print sheets. Save on printing costs while keeping every detail.")

uploaded_files = st.file_uploader("Choose your photos",
                                  accept_multiple_files=True,
                                  type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_files:
    st.info(f"{len(uploaded_files)} photos selected.")

    if st.button("🚀 Generate Print Sheets"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            sheet_count = 0
            # Coordinates for 2x2 grid positions
            positions = [
                (0, 0),
                (SUB_W + MARGIN, 0),
                (0, SUB_H + MARGIN),
                (SUB_W + MARGIN, SUB_H + MARGIN)
            ]

            # Process files in batches of 4
            for i in range(0, len(uploaded_files), 4):
                sheet = Image.new('RGB', (FINAL_W, FINAL_H), (255, 255, 255))
                batch = uploaded_files[i:i + 4]

                for idx, file in enumerate(batch):
                    processed_img = process_image(file, SUB_W, SUB_H)
                    sheet.paste(processed_img, positions[idx])

                sheet_count += 1

                # Save each sheet to a buffer to add to ZIP
                img_io = io.BytesIO()
                sheet.save(img_io, format='JPEG', quality=95)
                zip_file.writestr(f"print_sheet_{sheet_count}.jpg", img_io.getvalue())

        st.success(f"✅ {sheet_count} print sheets successfully generated!")

        st.download_button(
            label="📥 Download ZIP Archive",
            data=zip_buffer.getvalue(),
            file_name="photocomposite_sheets.zip",
            mime="application/zip"
        )