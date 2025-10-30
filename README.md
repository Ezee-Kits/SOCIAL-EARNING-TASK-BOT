# 🤖 SOCIAL-EARNING-TASK-BOT — Complete Task Performer for Facebook, Twitter (X), Instagram, YouTube, YouTube Music & Threads

## 🚀 Overview
The **SOCIAL-EARNING-TASK-BOT** is a full Python-based automation system that performs **all social earning tasks automatically** — without any human effort.  
It automates every major social media task on the **[SocialEarning.org](https://socialearning.org)** platform, such as:

- Facebook Page Likes, Comments, Follows, Shares, Reviews, and Video Views  
- Twitter (X) Follows, Likes, Retweets, and Replies  
- Instagram Follows, Likes, and Comments  
- YouTube Video Likes, Comments, and Subscriptions  
- YouTube Music Tasks  
- Threads (Meta) Follows and Likes  

The bot automatically logs in, retrieves all available tasks, performs them accurately, uploads proof, and submits them — fully hands-free.

---

## 🧩 Supported Platforms
| Platform | Automated Actions |
|-----------|--------------------|
| **Facebook** | Page Follow, Post Like, Comment, Share, Review, Video View |
| **Twitter (X)** | Follow, Like, Retweet, Reply |
| **Instagram** | Follow, Like, Comment |
| **YouTube** | Like, Comment, Subscribe |
| **YouTube Music** | Follow, Like |
| **Threads** | Follow, Like |

---

## 🎯 Key Features
✅ **Full browser automation** using `pyppeteer` (Chromium-based)  
✅ **Auto-login** with stored credentials and smart 5-hour cooldowns  
✅ **Smart task detection** using dynamic page parsing  
✅ **Proof upload automation** (screenshot handling)  
✅ **CSV data logging** for all daily activities  
✅ **Multi-platform support** (Facebook, X, Instagram, YouTube, Threads, etc.)  
✅ **Task execution from multiple pages** (pagination support)  
✅ **Automatic retries and smooth scrolling for dynamic UIs**  
✅ **User-friendly login interface** (Tkinter pop-up for email and password entry)  
✅ **Cross-platform compatible** (Windows, Linux, Android via Termux)  

---

## 🏗️ How It Works — Step by Step

1. **Login System**
   - Opens [socialearning.org](https://socialearning.org/sign-in)
   - Uses a **secure Tkinter dialog** to input your email and password  
   - Logs in and checks the last login time — skips login if within 5 hours  

2. **URL Scraper**
   - Visits all task pages (1–15)
   - Extracts every task (social media platform, URL, and rate)
   - Saves all tasks to CSV file:  
     `CSV FILES/<today’s date> Files/tasks_urls.csv`

3. **Task Executor**
   - Opens each URL one by one  
   - Detects which platform the task belongs to (Facebook, Twitter, etc.)
   - Executes the appropriate action via automation scripts (e.g., Like, Follow, Comment)
   - Takes a screenshot after performing the task  
   - Uploads the screenshot to SocialEarning proof input  
   - Selects the right username  
   - Submits the task automatically  

4. **Data Logging**
   - Saves timestamp logs, URLs, and task status  
   - Automatically removes duplicate entries  
   - Organizes all files into daily folders (for performance tracking)

---

## 📂 Repository Structure
```
SocialEarningBot/
│── PY FILES
|  ├──── func.py                  # Core utility functions (clicking, scrolling, CSV saving)
|  ├── sign_url.py               # Handles login + task URL extraction
|  ├── posting_bot.py            # Main automation controller
|  │
|  ├── fb_task.py                # Facebook automation module
|  ├── twitter_task.py           # Twitter (X) automation module
|  ├── insta_task.py             # Instagram automation module
|  ├── yt_task.py                # YouTube automation module
|  ├── yt_music_task.py          # YouTube Music automation module
|  ├── threads_task.py           # Threads automation module
│
├── CSV FILES/                # Daily logs and data output folder
   |── YYYY-MM-DD Files/     # Tasks and data for that day
│
└── README.md                 # Documentation
```

---

## ⚙️ Installation Guide

### 🧠 Requirements
- Python 3.10 or higher  
- Google Chrome or Chromium Browser  
- Internet connection  
- Basic knowledge of running Python scripts  

---

### 🪟 Windows Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SOCIAL-EARNING-TASK-BOT.git
   cd SocialEarning-Automation-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install pyppeteer pandas lxml beautifulsoup4 tk asyncio
   ```

3. **Set up Chrome user profile**
   - Go to Chrome → `chrome://version`
   - Copy the **Profile Path**
   - Use that path as your `userDataDir` in `posting_bot.py`
   - Example:
     ```python
     'userDataDir': r"C:\Users\HP\Documents\SE_ChromeProfile"
     ```

4. **Run the bot**
   ```bash
   python posting_bot.py
   ```

---

### 📱 Termux (Android) Setup
1. **Install Termux & Python**
   ```bash
   pkg update && pkg upgrade -y
   pkg install python git chromium -y
   ```

2. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/SocialEarning-Automation-Bot.git
   cd SocialEarning-Automation-Bot
   ```

3. **Install libraries**
   ```bash
   pip install pyppeteer pandas asyncio beautifulsoup4 lxml
   ```

4. **Run it**
   ```bash
   python posting_bot.py
   ```

---

## 🧰 Example Workflow

### 1️⃣ Login Phase
```text
>>> Opening SocialEarning.org login page
>>> Enter your email and password in the popup window
✅ Successfully logged in!
```

### 2️⃣ Task Collection
```text
Collecting available tasks...
✅ 150 tasks saved to /CSV FILES/2025-10-19 Files/tasks_urls.csv
```

### 3️⃣ Automation Execution
```text
Executing Facebook/Page Like
✅ Liked post successfully!
✅ Screenshot captured
✅ Proof uploaded
✅ Task submitted
```

---

## 🧠 Technical Details

### Core Automation Libraries
| Library | Purpose |
|----------|----------|
| **pyppeteer** | Browser control (Chromium engine) |
| **asyncio** | Asynchronous task handling |
| **pandas** | Data processing and CSV logging |
| **BeautifulSoup4 / lxml** | HTML parsing |
| **tkinter** | GUI input dialog for secure login |
| **os / time / datetime** | File management and task scheduling |

### File Management
- Each day’s operations are stored in a new folder automatically  
- Logs are deduplicated and sorted chronologically  

---

## 💾 Data Output Example
```
/CSV FILES/2025-10-19 Files/tasks_urls.csv

| socialMedia | url                                  | rate  | status  |
|--------------|--------------------------------------|--------|----------|
| Facebook     | https://facebook.com/...             | ₦20    | Pending  |
| Instagram    | https://instagram.com/...            | ₦15    | Pending  |
| YouTube      | https://youtube.com/...              | ₦25    | Pending  |
```

---

## 💡 Future Updates
- ✅ Add Telegram task automation  
- ✅ Add multi-account management  
- ✅ Integrate stealth anti-bot engine  
- ✅ Enable cloud synchronization of logs  

---

## 📺 Full Video Tutorial  
I have created a **complete YouTube tutorial** explaining everything —  
from setup, dependencies, configuration, to full demo of how the bot automates all tasks seamlessly.

👉 **Watch it on YouTube:** [Ezee Kits Channel](https://www.youtube.com/@Ezee_Kits)  
🎥 Subscribe, Like, and Comment to support more amazing projects like this!

---

## 👨‍💻 Author  
**Ezee Kits (Peter)**  
🎓 Electrical and Electronics Engineer  
📍 Nigeria 🇳🇬  
💡 Automation | AI | Web Scraping | Data Engineering  
📧 **Email:** ezeekits@gmail.com  
📺 **YouTube:** [Ezee Kits Channel](https://www.youtube.com/@Ezee_Kits)

---

## ⚖️ License  
**MIT License**  
This project is open-source for personal and educational use.  
You may modify or improve it freely but must credit **Ezee Kits** as the original author.

---

**GitHub Short Description:**
> Fully automated SocialEarning bot using Pyppeteer — performs Facebook, Twitter (X), Instagram, YouTube, YouTube Music & Threads tasks automatically with proof upload and task submission. Developed by Ezee Kits.
> The Script is still under development, so any suggestions are welcomed
