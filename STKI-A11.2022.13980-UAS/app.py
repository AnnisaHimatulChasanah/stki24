import streamlit as st
from rank_bm25 import BM25Okapi
import pandas as pd
import os

#load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Mendapatkan jalur direktori saat ini
df_ayam = pd.read_pickle(os.path.join(BASE_DIR, 'processed/df_indoRecipesAyam.pkl'))
df_kambing = pd.read_pickle(os.path.join(BASE_DIR, 'processed/df_indoRecipesKambing.pkl'))
df_telur = pd.read_pickle(os.path.join(BASE_DIR, 'processed/df_indoRecipesTelur.pkl'))
df_udang = pd.read_pickle(os.path.join(BASE_DIR, 'processed/df_indoRecipesUdang.pkl'))

# Menggabungkan semua DataFrame
df_combined = pd.concat([df_ayam, df_kambing, df_telur, df_udang], ignore_index=True)

# Tokenisasi kolom clean_instructions
tokenized_corpus = [doc.split() for doc in df_combined['clean_instructions'].apply(lambda x: ' '.join([' '.join(step) for step in x]))]

# Inisialisasi algoritma BM25
bm25 = BM25Okapi(tokenized_corpus)

# Header dengan gradien
st.markdown(
    """
    <div style="
        background: linear-gradient(to right, #B9BDB1, #D6D5C3); 
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: white;">
        <h1>🍳 Resep Makanan Indonesia 🍳</h1>
        <p>Masak jadi lebih mudah dengan resep berdasarkan bahan yang kamu punya!🍤</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Pengguna memasukkan kata kunci
#query = st.text_input("🔍 Masukkan kata kunci pencarian resep (contoh: ayam, telur, kambing dan udang.):", placeholder="Cari resep favoritmu...")
#st.markdown("<hr style='border: 1px solid #B9BDB1;'>", unsafe_allow_html=True)

# Inisialisasi session state untuk query dan clear state
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''

# Fungsi callback untuk clear button
def clear_search():
    st.session_state.search_query = ''
    st.session_state.search_input = ''

# Membuat container untuk search box
search_container = st.container()

# Layout untuk search box dan clear button
col1, col2 = search_container.columns([6, 1])

# Text input di kolom pertama
with col1:
    st.markdown("""
        <style>
        .stTextInput {
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    query = st.text_input( 
        "🔍 Masukkan kata kunci pencarian resep (contoh: ayam, telur, kambing dan udang) :",
        key="search_input",
        placeholder="Cari resep favoritmu..."
    )

# Clear button di kolom kedua
with col2:
    st.markdown("""
    <style>
    .buttonx {
        margin-top: 32px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .buttonx button {
        background-color: red;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        width: 100%;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="buttonx">', unsafe_allow_html=True)

    if st.button("❌", key="clear_button", help="Hapus pencarian", on_click=clear_search):
        st.session_state.search_query = ''

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #B9BDB1;'>", unsafe_allow_html=True)

# Update query pencarian dalam session state
if query:
    st.session_state.search_query = query

# Normalisasi teks di clean_instructions dan Title
df_combined['clean_instructions'] = df_combined['clean_instructions'].apply(
    lambda x: ' '.join([' '.join(step) for step in x]).lower()
)
df_combined['Title'] = df_combined['Title'].str.lower()

# Menampilkan hasil berdasarkan query dalam session state
if st.session_state.search_query:
    tokenized_query = st.session_state.search_query.lower().split()  # Pastikan lowercase
    doc_scores = bm25.get_scores(tokenized_query)
    top_n = bm25.get_top_n(tokenized_query, df_combined.index, n=10)

    # Simulasi hasil ideal (misalnya, semua resep yang mengandung query di Title)
    ideal_results = df_combined[df_combined['Title'].str.contains(query.lower(), case=False, na=False)].index

    # Tampilkan rekomendasi
    st.markdown("<h3 style='color: #B7CBC0;'>✨ Top 10 Rekomendasi:</h3>", unsafe_allow_html=True)
    recipe_titles =  df_combined.loc[top_n, 'Title'].apply(str.title).tolist()

    # Buat tombol untuk setiap resep
    for idx, title in zip(top_n, recipe_titles):
        if st.button(title, key=idx):
            ingredients = df_combined.loc[idx, 'Ingredients']
            steps = df_combined.loc[idx, 'Steps']

            # Menampilkan ingredients
            st.markdown("<h3 style='color: #7A9B71;'>📝 Bahan-Bahan:</h3>", unsafe_allow_html=True)
            ingredients_list = ingredients.split('--')
            st.markdown("<ul>", unsafe_allow_html=True)
            for ingredient in ingredients_list:
                if ingredient.strip():
                    st.markdown(f"<li style='font-size: 16px;'>{ingredient.strip()}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            # Menampilkan steps
            st.markdown("<h3 style='color: #7A9B71;'>🍜 Langkah-Langkah:</h3>", unsafe_allow_html=True)
            steps_list = steps.split('--')
            for i, step in enumerate(steps_list):
                if step.strip():
                    st.markdown(f"<p><strong>Langkah {i + 1}:</strong> {step.strip()}</p>", unsafe_allow_html=True)

            st.markdown("<hr style='border: 1px dashed #4F684D;'>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: #002911;">
        <p>Dibuat oleh Annisa 🌿</p>
    </div>
    """,
    unsafe_allow_html=True,)
