import cv2
import streamlit as st
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input,decode_predictions
from PIL import Image

def load_model():
    model = MobileNetV2(weights="imagenet")
    return model 

def preprocess_image(image):
    img = np.array(image)
    img =cv2.resize(img,(224,224))
    img =preprocess_input(img)
    img =np.expand_dims(img,axis=0)
    return img

def classify_image(model,image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        decoder = decode_predictions(predictions,top=3)[0]
        return decoder
    except Exception as e:
        st.error(f"Errror classifying image: {str(e)}")

def main():
    st.set_page_config(page_title="AI image classifier",layout="centered")

    st.title("AI Image classifer")
    st.write("Upload an image and let AI tell you what it is.")

    @st.cache_resource
    def load_cached_model():
        return load_model()
    
    model=load_cached_model()
    uploaded_file=st.file_uploader("Choose an image.", type=["jpg","png"])

    if uploaded_file is not None:
        image = st.image(
            uploaded_file,caption="Uploaded Image", use_container_width=True
        )
        btn=st.button("Classify image")

        if btn:
            with st.spinner("Analzying image..."):
                image=Image.open(uploaded_file).convert("RGB")
                predictions =classify_image(model,image)

                if predictions:
                    st.subheader("Predictions")
                    for _,label,score in predictions:
                        st.write(f"**{label}**:{score:.2%}")

if __name__=="__main__":
    main()