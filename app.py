import streamlit as st
import boto3
import time
from PIL import Image, ImageDraw
import pandas as pd

# AWS clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

BUCKET = "YOUR BUCKET NAME"  # 🔁 replace

# Upload
def upload_to_s3(file, filename):
    s3.upload_fileobj(file, BUCKET, filename)

# Detect labels
def detect_labels(filename):
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': BUCKET, 'Name': filename}},
        MaxLabels=10
    )
    return response

# Draw boxes
def draw_boxes(image, labels):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for label in labels:
        for instance in label.get("Instances", []):
            box = instance["BoundingBox"]
            left = box["Left"] * width
            top = box["Top"] * height
            right = left + (box["Width"] * width)
            bottom = top + (box["Height"] * height)

            draw.rectangle([left, top, right, bottom], outline="#d63384", width=3)
            draw.text((left, top), label["Name"], fill="#d63384")

    return image


# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Image Label Generator", layout="centered")


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffe4ec, #ffd6e8);
}

/* Buttons */
.stButton>button {
    background-color: #d63384;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #d63384;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color:#d63384;'>AI Image Label Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by AWS Rekognition</p>", unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:

    uploaded_file.seek(0)
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Preview", width=300)

    if st.button("Analyze Image"):

        with st.spinner("Analyzing..."):
            filename = str(int(time.time())) + "_" + uploaded_file.name

            uploaded_file.seek(0)
            upload_to_s3(uploaded_file, filename)

            response = detect_labels(filename)
            labels = response["Labels"]

        st.success("Analysis Complete")

        # Bounding boxes
        boxed_image = draw_boxes(image.copy(), labels)
        st.image(boxed_image, caption="Detected Objects", width=300)

        st.subheader("Results")

        results = []

        for label in labels:
            if label['Confidence'] > 70:
                name = label['Name']
                confidence = round(label['Confidence'], 2)

                
                st.markdown(f"**{name} ({confidence}%)**")
                st.progress(int(confidence))

                results.append({"Label": name, "Confidence": confidence})

        # Download button
        if results:
            df = pd.DataFrame(results)
            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Results",
                data=csv,
                file_name="labels.csv",
                mime="text/csv"
            )
