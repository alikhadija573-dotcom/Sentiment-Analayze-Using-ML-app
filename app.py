# app.py
from textblob import TextBlob
import pandas as pd
import streamlit as st
import cleantext
import emoji
import os

# ---------------- Title & Background ----------------
st.title("Sentiment Web Analyzer")

background_image = background_image = "C:\\Users\\DELL\\Downloads\\pngtree-minimal-simple-design-template-for-3d-floating-twitter-logo-image_3637541.jpg"
if os.path.exists(background_image):
    st.image(background_image, width=900)  # width adjust kar sakte ho
else:
    st.warning("Background image not found. Skipping image display.")

st.header("Now Scale Your Thoughts")

# ---------------- Text Analysis ----------------
with st.expander("Analyze Your Text"):
    text = st.text_input("Text here:")

    if text:
        blob = TextBlob(text)
        p = round(blob.sentiment.polarity, 2)
        st.write('Polarity :', p)
        if p >= 0.1:
            st.write(emoji.emojize("Positive Speech :grinning_face_with_big_eyes:"))
        elif p == 0.0:
            st.write(emoji.emojize("Neutral Speech :zipper-mouth_face:"))
        else:
            st.write(emoji.emojize("Negative Speech :disappointed_face:"))
        st.write('Subjectivity', round(blob.sentiment.subjectivity, 2))

    pre = st.text_input('Clean Your Text: ')
    if pre:
        st.write(cleantext.clean(
            pre,
            clean_all=False,
            extra_spaces=True,
            stopwords=True,
            lowercase=True,
            numbers=True,
            punct=True
        ))

# ---------------- Excel Analysis ----------------
with st.expander('Analyze Excel files'):
    st.write("_**Note**_: Your file must contain the column named 'Tweets' that contains the text to be analyzed.")
    upl = st.file_uploader('Upload file')

    def score(x):
        blob1 = TextBlob(str(x))
        return blob1.sentiment.polarity

    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'

    if upl:
        df = pd.read_excel(upl)
        if 'Tweets' not in df.columns:
            st.error("Uploaded file does not contain a 'Tweets' column.")
        else:
            df['score'] = df['Tweets'].apply(score)
            df['analysis'] = df['score'].apply(analyze)
            st.write(df.head(10))

            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='sentiment.csv',
                mime='text/csv',
            )

# ---------------- Footer ----------------
st.write("\n" * 5)
st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)
st.write("Copy© 2025 Adeel Munir | Made With ❤️ in Pakistan")