import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile
import os

st.set_page_config(page_title="Optimiseur de Tirage 10x15", layout="centered")

# --- CONFIGURATION ---
FINAL_W, FINAL_H = 1800, 1200
MARGE = 10
SUB_W = (FINAL_W - MARGE) // 2
SUB_H = (FINAL_H - MARGE) // 2


def preparer_image(uploaded_file, cible_w, cible_h):
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    if img.height > img.width:
        img = img.rotate(90, expand=True)

    fond = Image.new('RGB', (cible_w, cible_h), (255, 255, 255))
    img.thumbnail((cible_w, cible_h), Image.Resampling.LANCZOS)
    offset_x = (cible_w - img.width) // 2
    offset_y = (cible_h - img.height) // 2
    fond.paste(img, (offset_x, offset_y))
    return fond


st.title("📸 Générateur de Planches 10x15")
st.write("Importez vos photos pour créer des planches de 4 photos prêtes à imprimer.")

uploaded_files = st.file_uploader("Choisissez vos photos", accept_multiple_files=True,
                                  type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_files:
    if st.button("🚀 Générer les fichiers"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            nb_planches = 0
            positions = [(0, 0), (SUB_W + MARGE, 0), (0, SUB_H + MARGE), (SUB_W + MARGE, SUB_H + MARGE)]

            for i in range(0, len(uploaded_files), 4):
                planche = Image.new('RGB', (FINAL_W, FINAL_H), (255, 255, 255))
                batch = uploaded_files[i:i + 4]

                for idx, file in enumerate(batch):
                    img_prete = preparer_image(file, SUB_W, SUB_H)
                    planche.paste(img_prete, positions[idx])

                nb_planches += 1
                img_io = io.BytesIO()
                planche.save(img_io, format='JPEG', quality=95)
                zip_file.writestr(f"planche_{nb_planches}.jpg", img_io.getvalue())

        st.success(f"✅ {nb_planches} planches générées !")
        st.download_button(
            label="📥 Télécharger le ZIP",
            data=zip_buffer.getvalue(),
            file_name="tirages_10x15.zip",
            mime="application/zip"
        )