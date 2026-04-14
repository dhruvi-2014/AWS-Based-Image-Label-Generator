# AI Image Label Generator (AWS Rekognition)

An AI-powered web app that detects objects in images using **AWS Rekognition** and displays results with bounding boxes and confidence scores.



## 🚀 Features

* 📤 Upload any image
* 🤖 Detect objects using AI
* 📊 Show confidence scores
* 🟥 Draw bounding boxes on detected objects
* 📥 Download results as CSV



## 🛠️ Tech Stack

* Python
* Streamlit
* AWS Rekognition
* Amazon S3



## ⚙️ How to Run

1. Clone the repository

```
git clone https://github.com/dhruvi-2014/AWS-Based-Image-Label-Generator.git
cd AWS-Based-Image-Label-Generator
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Configure AWS

```
aws configure
```

4. Run the app

```
streamlit run app.py
```



## 🔐 Security Note

AWS credentials are NOT stored in code.
Authentication is handled using AWS CLI configuration.

---

## 🌟 Future Improvements

* Deploy on cloud (Streamlit Cloud / AWS EC2)
* Add batch image processing
* Improve UI/UX

---
