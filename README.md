# 🏥 AI Ibound Caller Receptionist for Hospital

An intelligent, voice-based hospital receptionist assistant powered by AI, enabling seamless patient interactions for appointments, doctor scheduling, and emergency services.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🚀 Getting Started](#-getting-started)
- [� Project Structure](#-project-structure)
- [🤖 Available Tools](#-available-tools)
- [📚 Database Models](#-database-models)
- [🎤 Voice Features](#-voice-features)
- [📖 Usage Guide](#-usage-guide)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- 🎙️ **Voice-Based Interaction** - Natural language processing for hands-free communication
- 👨‍⚕️ **Doctor & Schedule Management** - Check doctor availability and specializations
- 📅 **Appointment Booking** - Real-time appointment scheduling and cancellations
- 🏢 **Department Information** - Get details about hospital departments and services
- 🚑 **Emergency Services** - Immediate emergency routing and ambulance service
- ⏰ **Real-Time Information** - Current date, time, and weather information
- 🌍 **Multilingual Support** - Turn detection for multiple languages
- 📊 **Database Integration** - MongoDB backend for persistent data storage
- 🎛️ **Natural Conversation Flow** - Human-like receptionist behavior
- 🔊 **Professional Voice Synthesis** - High-quality text-to-speech output
- 🎧 **Noise Cancellation** - Clear audio processing with background noise reduction
- 📞 **Browser-Based Calling** - Make Twilio calls directly from web browser
- 🚀 **LiveKit Integration** - SIP protocol for seamless call management

---

## 🛠️ Tech Stack

### Backend Framework
- ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** - Modern, fast web framework for building APIs
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-00BFFF?style=flat&logoColor=white) **Uvicorn** - ASGI web server for Python

### AI & Voice Processing
- ![LiveKit Agents](https://img.shields.io/badge/LiveKit%20Agents-1f3a93?style=flat&logoColor=white) **LiveKit Agents** - Real-time communication platform with AI capabilities
  - **Deepgram** - Speech-to-Text (STT) with Flux General model
  - **Groq** - LLM inference (GPT-OSS-120B model)
  - **Cartesia** - Text-to-Speech (TTS) with Sonic-3 voice
  - **Silero** - Voice Activity Detection (VAD)
  - **Turn Detector** - Multilingual conversation detection

### Telephony & Communication
- ![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=flat&logo=twilio&logoColor=white) **Twilio** - Phone call management and VoIP integration
- ![SIP Protocol](https://img.shields.io/badge/SIP-Protocol-blueviolet?style=flat) **SIP** - Session Initiation Protocol for call routing

### Database
- ![MongoDB](https://img.shields.io/badge/MongoDB-13AA52?style=flat&logo=mongodb&logoColor=white) **MongoDB** - NoSQL database for patient, doctor, and appointment data
- ![Motor](https://img.shields.io/badge/Motor-13AA52?style=flat&logoColor=white) **Motor** - Async MongoDB driver
- ![PyMongo](https://img.shields.io/badge/PyMongo-13AA52?style=flat&logoColor=white) **PyMongo** - MongoDB Python client

### Utilities & Tools
- ![Python-dotenv](https://img.shields.io/badge/python--dotenv-EDB83D?style=flat&logoColor=white) **python-dotenv** - Environment variable management
- ![PyTZ](https://img.shields.io/badge/PyTZ-3776AB?style=flat&logoColor=white) **PyTZ** - Timezone support
- ![Pydantic](https://img.shields.io/badge/Pydantic-EF362F?style=flat&logo=pydantic&logoColor=white) **Pydantic** - Data validation and serialization
- ![IPython Kernel](https://img.shields.io/badge/IPython-Kernel-F37726?style=flat&logoColor=white) **ipykernel** - Interactive notebook support

### Runtime
- ![Python 3.12](https://img.shields.io/badge/Python-3.12.7%2B-3776AB?style=flat&logo=python&logoColor=white)

---

## 📦 Installation

### Prerequisites
- Python 3.12.7 or higher
- MongoDB instance running
- Twilio account with credentials
- LiveKit server instance
- Deepgram, Groq, and Cartesia API keys

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/AI_Receptionist_For_hospital.git
cd AI_Receptionist_For_hospital
```

### Step 2: Install uv Package Manager
```bash
pip install uv
```

### Step 3: Install Dependencies
```bash
uv sync
```

This will install all dependencies specified in `pyproject.toml`.

---

## ⚙️ Configuration

### Step 2: Create `.env` File
Create a `.env` file in the project root with the following variables:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_API_KEY=your_twilio_api_key
TWILIO_API_SECRET=your_twilio_api_secret
TWILIO_TWIML_APP_SID=your_twilio_twiml_app_sid
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# LiveKit Configuration
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_SIP_HOST=your_sip_host
LIVEKIT_SIP_USERNAME=your_sip_username
LIVEKIT_SIP_PASSWORD=your_sip_password
LIVEKIT_AGENTS_PORT=8081

# AI Services
DEEPGRAM_API_KEY=your_deepgram_api_key
GROQ_API_KEY=your_groq_api_key
CARTESIA_API_KEY=your_cartesia_api_key

# Database Configuration
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=hospital_receptionist
```

### Step 3: Database Setup
Initialize your MongoDB with sample data as needed for your hospital information.

---

## 🚀 Getting Started

### Step 1: Start the FastAPI Server
```bash
uv run main.py
```
The server will be available at `http://localhost:8000`

### Step 2: Start the LiveKit Agent (in another terminal)
```bash
uv run agent.py dev
```

### Step 3: Access the Web Interface
Open your browser and navigate to `http://localhost:8000` to:
- 📱 **Place a Twilio call** directly from your browser
- 🎤 Speak naturally to the AI receptionist
- 📊 View call status in real-time

---

## 📱 How to Make a Call

1. Open `http://localhost:8000` in your browser
2. Click the **"Call"** button on the web interface
3. A Twilio WebRTC call will be established
4. Speak naturally to the AI receptionist - no phone needed!
5. The system responds with natural, human-like voice interaction
6. Click **"Hang Up"** to end the call

---

## 🔧 Project Structure

```
AI_Receptionist_For_hospital/
│
├── 📄 main.py                 # FastAPI application & Twilio endpoints
├── 🤖 agent.py                # LiveKit agent configuration & session management
├── 📋 pyproject.toml          # Project dependencies & metadata
├── 📖 README.md               # This file
│
├── 📂 database/
│   ├── models.py              # Pydantic models (Doctor, Patient, Appointment, etc.)
│   └── mongodb.py             # MongoDB connection & operations
│
├── 📂 tools/
│   ├── __init__.py            # Tools package exports
│   ├── appointment.py         # 📅 Appointment booking & management
│   ├── datetime_tool.py       # ⏰ Date & time utilities
│   ├── department_info.py     # 🏢 Department information queries
│   ├── doctor_schedule.py     # 👨‍⚕️ Doctor & schedule management
│   ├── emergency.py           # 🚑 Emergency services
│   └── weather.py             # 🌤️ Weather information
│
├── 📂 prompts/
│   ├── __init__.py            # Prompts package exports
│   └── assistant_prompts.py   # 💬 System instructions & prompts
│
├── 📂 static/
│   └── twilio.min.js          # Twilio client library
│
└── 📄 dispatch-rule.json      # Twilio SIP dispatch rules
   inbound-trunk.json         # Twilio SIP trunk configuration
```

---

## 🤖 Available Tools

The AI receptionist has access to the following tools for handling various tasks:

### 👨‍⚕️ Doctor & Schedule Management
- **`get_doctor_schedule`** - Retrieve a doctor's schedule for specific dates
- **`check_doctor_availability`** - Check if a doctor is available at a given time
- **`list_all_departments`** - Get list of all hospital departments

### 📅 Appointment Management
- **`book_appointment`** - Schedule a new appointment for a patient
- **`check_patient_appointments`** - View patient's upcoming appointments
- **`cancel_appointment`** - Cancel an existing appointment

### 🏢 Department Information
- **`get_department_info`** - Get detailed information about a department
- **`get_visiting_hours`** - Retrieve hospital visiting hours

### 🚑 Emergency Services
- **`get_emergency_info`** - Get emergency contact information
- **`get_ambulance_service`** - Request ambulance service details

### ⏰ Utilities
- **`get_weather`** - Get current weather information
- **`get_current_datetime`** - Get current date and time
- **`get_current_date`** - Get current date only
- **`get_current_time`** - Get current time only

---

## 📚 Database Models

### 🏥 Doctor Model
```python
{
  "doctor_id": "str",
  "name": "str",
  "specialization": "str",
  "department": "str",
  "phone": "str",
  "email": "str",
  "working_hours": [
    {
      "day": "Monday",
      "start_time": "09:00",
      "end_time": "17:00",
      "is_available": true
    }
  ],
  "consultation_duration": 30  # minutes
}
```

### 🏢 Department Model
```python
{
  "department_id": "str",
  "name": "str",
  "description": "str",
  "location": "Building A, Floor 2",
  "phone": "str",
  "services": ["list", "of", "services"]
}
```

### 👤 Patient Model
```python
{
  "patient_id": "str",
  "name": "str",
  "phone": "str",
  "email": "str",
  "date_of_birth": "str",
  "address": "str",
  "medical_history": ["array", "of", "conditions"]
}
```

### 📅 Appointment Model
```python
{
  "appointment_id": "str",
  "patient_id": "str",
  "doctor_id": "str",
  "appointment_date": "2026-01-28",
  "appointment_time": "10:30",
  "reason": "str",
  "status": "scheduled",  # or "completed", "cancelled"
  "created_at": "datetime"
}
```

---

## 🎤 Voice Features

### Speech-to-Text (STT)
- **Provider**: Deepgram
- **Model**: Flux General (Multi-language support)
- **Eager EOT Threshold**: 0.4 (optimized for natural conversation flow)
- **Real-time processing**: Immediate transcription feedback

### Text-to-Speech (TTS)
- **Provider**: Cartesia
- **Model**: Sonic-3 (High-quality voice synthesis)
- **Voice ID**: f786b574-daa5-4673-aa0c-cbe3e8534c02 (Professional female voice)
- **Natural prosody**: Realistic intonation and pacing

### Voice Activity Detection (VAD)
- **Provider**: Silero
- **Model**: Lightweight, efficient VAD
- **Purpose**: Detect when user starts/stops speaking

### Turn Detection
- **Provider**: LiveKit Turn Detector (Multilingual)
- **Capability**: Detects natural conversation turns across multiple languages
- **Benefit**: Enables natural back-and-forth dialogue

### Noise Cancellation
- **Technology**: LiveKit Noise Cancellation Plugin
- **Purpose**: Clean audio in noisy environments
- **Use Case**: Hospital environments with ambient noise

---

## 🔐 Security & Environment Variables

### Security Best Practices
1. ✅ Never commit `.env` file to version control
2. ✅ Use environment variables for all sensitive data
3. ✅ Rotate API keys regularly
4. ✅ Use HTTPS for all external communications
5. ✅ Validate all patient data before processing
6. ✅ Implement rate limiting on endpoints

### Required Environment Variables
All variables must be set before running the application. Missing variables will cause the application to fail.

---

## 📖 Usage Guide

### 1️⃣ Making a Call from Browser
1. Open `http://localhost:8000` in your web browser
2. Click the **"Call"** button
3. Speak naturally to the AI receptionist (Alina)
4. The system responds with a human-like voice
5. End the call by clicking **"Hang Up"**

### 2️⃣ Booking an Appointment
**You**: "I'd like to book an appointment with Dr. Smith"

**Receptionist**:
- Asks for your name and contact information
- Checks Dr. Smith's availability
- Confirms appointment time and details

### 3️⃣ Checking Doctor Availability
**You**: "Is Dr. Johnson available tomorrow?"

**Receptionist**:
- Checks the doctor's schedule
- Provides available time slots
- Offers to book an appointment if interested

### 4️⃣ Department Information
**You**: "What services does the cardiology department offer?"

**Receptionist**:
- Provides department details
- Lists available services
- Explains visiting hours and location

### 5️⃣ Emergency Assistance
**You**: "This is an emergency!"

**Receptionist**:
- Immediately routes to emergency services
- Provides emergency contact information
- Offers ambulance service if needed

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ for healthcare excellence**

Last Updated: January 28, 2026 | Version: 0.1.0
