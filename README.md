# Digital Sovereign Agent (Infrastructure V2.0)

The **Digital Sovereign Agent** is an autonomous marketing infrastructure designed for the "100,000,000x Creator". It automates strategy generation, content creation (videos, slides, infographics), and social media distribution.

## 🚀 Features

*   **Simera Brain**: A psychological narrative engine that pivots from "selling features" to "solving pains" (Risk Aversion, Data Empathy).
*   **Studio Director**: Automatically generates multimedia production briefs (Video Scripts, Slide Decks, Infographics).
*   **AI Refiner**: Uses OpenAI (GPT-4o) to polish content into an "Elite/Tech Titan" voice.
*   **Reddit Detective**: Simulates extensive Reddit research to find viral content angles.
*   **Social Dispatcher**: Connects to X (Twitter), LinkedIn, and Instagram for multi-channel deployment (Infrastructure Ready).

## 🛠 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/dominicrume/social-media-marketing.git
    cd social-media-marketing
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file with your credentials:
    ```ini
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_app_password
    OPENAI_API_KEY=sk-...
    # Optional Social Media Keys
    X_API_KEY=...
    LINKEDIN_ACCESS_TOKEN=...
    ```

## ⚡ Usage

### Run the App (CLI)

**1. Generate a Single Marketing Packet (Immediate):**
```bash
python3 app.py run --email "your_email@gmail.com"
```
*Optional: Force a strategy*
```bash
python3 app.py run --strategy "The Apple Store Standard"
```

**2. Start the 24/7 Automation Daemon:**
```bash
python3 app.py daemon
```
*This will run the agent in the background and execute the workflow every day at 06:00 AM.*

## 🧠 Core Philosophy
*"We don't work harder. We build better engines."*
This tool is not just a script; it is a **Billion Dollar Infrastructure** for the Global South creator.
