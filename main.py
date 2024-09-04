import streamlit as st
from konlpy.tag import Okt
from collections import Counter
import pandas as pd

# Inisialisasi objek Okt
okt = Okt()

# Fungsi untuk mendeteksi eomi (akhiran) dari kalimat
def deteksi_eomi(teks):
    # Daftar eomi yang mungkin terdiri dari beberapa kata
    # eomi_patterns = [
    #     '고 싶', ' 거예요', '게요', '래요'
    # ]

    eomi_patterns = [
    "습니다", "습니까", "이다", "입니까", "ㅂ니다", "십니다", "셨습니다", "셨습니까", 
    "았습니다", "었습니다", "는습니다", "입니다", "이었습니다", "였습니다", "합니다", 
    "하십니다", "하셨습니다", "하셨습니까", "하시겠습니까", "하세요", "하고 있습니다", 
    "고 있습니다", "고 계십니다", "고 계시다", "하시다", "하시다", "고 있", 
    "하고 있", "하고 계신다", "하신다", "어 주십시오", "아 주십시오", "주십시오", "어 주세요", "주세요", 
    "아 주세요", "지 않습니까", "지 않", "는지", "인지", "입니까", "니", 
    "지 않습니다", "지 않", "하겠습니까", "할까요", "해 드릴까요", "드릴까요", "해요", 
    "해요", "어야 하다", "아야 하", "해도 좋습니다", "해도 됩니다", "만큼", 
    "만한", "만큼", "만한", "것입니다", "이라는 것", "인 것", "이었습니다", "였습니다", 
    "하신 것", "하실 것", "하신 분", "하실 분", "하시고", "하시지만", "하시면서", 
    "하고 나서", "한 후", "하고는", "하면서", "하고는", "에 대해", 
    "에 대해", "에 관해서", "세요",

    "아요", "어요", "니", "네", "지요", 
    "죠", "라", "면", "고 나서", "고 싶", "해", "해요", "하시다", "하자", 
    "하자고", "하는 것", "해야", "할까요", "해도", "아도", "어도", 
    "는 게", "게", "다는", "다고", "한", "했던", "할", "한",
    "으로서", "로서", "때문에", "이기 때문에", "거든", "거든요", "때문에", "이기 때문에", 
    "느냐", "더니", "고서", "아서", "어서", "으로서", "로서",
    "하고도", "한테도", "에게도", "보다", "는 것",
]

    
    eomi_data = []
    
    # Tokenisasi kalimat
    tokens = okt.morphs(teks)
    
    # Mencari gabungan kata yang mengandung eomi
    i = 0
    while i < len(tokens):
        for pattern in eomi_patterns:
            if i + len(pattern.split()) <= len(tokens):
                phrase = ' '.join(tokens[i:i + len(pattern.split())])
                if pattern in phrase:
                    eomi_data.append((phrase, pattern))
                    break
        i += 1
    
    return eomi_data

# Judul aplikasi
st.title("Analisis Frekuensi Kosakata Bahasa Korea dengan Kata Dasar dan Eomi")

# Input teks dari pengguna
teks_korea = st.text_area("Masukkan teks bahasa Korea di bawah ini:")

if teks_korea:
    try:
        # Melakukan analisis morfologi dan mendapatkan pasangan (kata, jenis_kata)
        hasil_analisis = okt.pos(teks_korea)
        
        # Menghitung frekuensi kosakata
        kosakata_counts = Counter(hasil_analisis)
        
        # Membuat dataframe dari hasil frekuensi
        data = []
        for (kata, jenis), freq in kosakata_counts.items():
            # Mendapatkan kata dasar (lemmatization)
            kata_dasar = okt.morphs(kata)[0] if jenis in ['Verb', 'Adjective'] else kata
            
            # Menyimpan ke dalam data list
            data.append([kata, jenis, kata_dasar, freq])
        
        # Konversi ke DataFrame
        df = pd.DataFrame(data, columns=["Kosakata", "Jenis", "Kata Dasar", "Frekuensi"])
        
        # Urutkan berdasarkan frekuensi dari yang terbesar
        df = df.sort_values(by="Frekuensi", ascending=False).reset_index(drop=True)
        
        # Memisahkan DataFrame berdasarkan jenis kosakata
        kata_benda = df[df["Jenis"] == "Noun"]
        kata_kerja = df[df["Jenis"] == "Verb"]
        kata_keterangan = df[df["Jenis"] == "Adverb"]
        partikel = df[df["Jenis"] == "Josa"]

        # Deteksi eomi di seluruh kalimat
        eomi_data = deteksi_eomi(teks_korea)
        
        # Menghitung frekuensi eomi
        eomi_freq = Counter([eomi for _, eomi in eomi_data])
        
        # Menyusun data eomi
        eomi_list = []
        for text, eomi in eomi_data:
            eomi_list.append([text, eomi_freq[eomi], eomi])
        
        # Konversi ke DataFrame
        df_eomi = pd.DataFrame(eomi_list, columns=["Gabungan Kata", "Frekuensi", "Eomi"])
        df_eomi = df_eomi.drop_duplicates().reset_index(drop=True)
        
        # Menampilkan hasil dalam tabel terpisah
        st.subheader("Kata Benda (Noun)")
        st.table(kata_benda)

        st.subheader("Kata Kerja (Verb)")
        st.table(kata_kerja)

        st.subheader("Kata Keterangan (Adverb)")
        st.table(kata_keterangan)

        st.subheader("Partikel (Josa)")
        st.table(partikel)

        st.subheader("Eomi (Akhiran)")
        st.table(df_eomi)
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
