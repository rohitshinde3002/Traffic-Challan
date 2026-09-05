

````markdown
# 🚦 AI Traffic Challan System

An AI-powered Traffic Challan Management System that uses Generative AI to detect traffic violations, identify vehicle number plates, retrieve registered vehicle information, and generate challan details automatically.

## 📌 Project Overview

The AI Traffic Challan System is designed to automate the traffic violation and challan generation process.

The system allows users to upload a traffic violation image. The application uses AI-based image analysis to identify the type of traffic violation and detect the vehicle number plate. It then checks the registered vehicle database and displays the vehicle owner's information along with the applicable fine.

## ✨ Features

- 🚨 Traffic violation detection using Generative AI
- 🔍 Vehicle number plate detection
- 👤 Registered vehicle/owner lookup
- 💰 Automatic fine calculation
- 📄 Challan summary generation
- 📱 WhatsApp challan sharing
- 🔗 Official eChallan verification link
- 🖥️ Interactive Streamlit web interface
- 🗄️ SQLite database for vehicle records
- 🔐 Secure API key management using environment variables

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Generative AI**
- **Groq API**
- **SQLite**
- **python-dotenv**
- **Git & GitHub**

## 📂 Project Structure

```text
Traffic-Challan/
│
├── app1.py
├── violation_detection.py
├── create_database.py
├── Chalan.database.py
├── Chalan.db
├── user.db
├── requirements.txt
│
├── drivers/
│   ├── driver1.jpg
│   ├── driver2.jpg
│   ├── driver3.jpg
│   └── driver4.jpg
│
├── images/
│   ├── no_helmet.jpg
│   ├── no_parking.jpg
│   ├── over_Sped.jpg
│   └── triple riding.jpg
│
└── pages/
    └── User_Database.py
````

## ⚙️ How It Works

```text
Upload Violation Image
        ↓
AI analyzes the image
        ↓
Traffic Violation Detection
        ↓
Vehicle Number Plate Detection
        ↓
Vehicle Database Lookup
        ↓
Owner & Vehicle Details
        ↓
Fine Calculation
        ↓
Challan Summary
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rohitshinde3002/Traffic-Challan.git
```

### 2. Navigate to the Project

```bash
cd Traffic-Challan
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file or API keys to GitHub.

## ▶️ Run the Application

```bash
python -m streamlit run app1.py
```

The application will open in your browser.

## 🖥️ Application Workflow

1. Upload a traffic violation image.    
2. Click **Generate Challan**.
3. AI detects the traffic violation.
4. AI extracts the vehicle number plate.
5. The system searches the registered vehicle database.
6. Owner and vehicle details are displayed.
7. Applicable fine is calculated.
8. A challan summary is generated.
9. The challan can be shared through WhatsApp or verified through the official eChallan portal.

## 🔐 Security

API keys are stored using environment variables and are excluded from Git tracking using `.gitignore`.

```text
.env
venv/
__pycache__/
*.pyc
temp/
```

## 🚀 Deployment

The application can be deployed as a Streamlit application on cloud platforms such as Render.

For production use, a cloud database and persistent storage should be considered instead of local SQLite storage.

## 🎯 Future Enhancements

* Real-time authorized vehicle information API integration
* Online challan payment integration
* Advanced number plate recognition using dedicated OCR
* Admin dashboard
* Cloud database integration
* User authentication and role-based access
* Challan PDF generation
* Cloud image storage
* Analytics and reporting dashboard

## 👨‍💻 Author

**Rohit Shinde**

GitHub: [rohitshinde3002](https://github.com/rohitshinde3002)

## 📄 License

This project is intended for educational and demonstration purposes.

````



