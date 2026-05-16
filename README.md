# Tele-Salary-Bot

> **Disclaimer:** This is a study/learning project and is not intended for professional or production use. It was built purely for educational purposes to explore Telegram Bot API, automation, and data scraping with Python.

---

## Overview

Tele-Salary-Bot is a Python-based Telegram bot that automatically monitors a Telegram group or channel for salary-formatted forwarded messages. When a matching message is detected, the bot extracts the structured salary data from the message text using Regular Expressions (RegEx) and saves it directly into a `.csv` file.

This bot is designed around a specific salary message format used in talent/agency workflows, where the message contains details like client name, session type, talent income, agency income, and payment links.

---

## Features

- Auto-detection — listens to all messages in a group and filters messages containing the keyword `SALARY`
- Data extraction — uses RegEx to parse structured fields from the message:
  - Percentage
  - Client Name
  - Session Type
  - Talent Income (IDR)
  - Agency Income (IDR)
  - Payment Link
- CSV export — appends extracted data into `data_salary.csv`, auto-creating the file with headers if it does not exist
- Fully automated — runs in the background polling for new messages, no manual trigger needed

---

## Project Structure

```
TeleBot/
│
├── main.py              # Main bot logic (message handler, parser, CSV writer)
├── data_salary.csv      # Output file where scraped salary data is stored
├── requirement.txt      # Python dependencies
├── .gitignore           # Git ignore rules (.env, venv, etc.)
├── .env                 # (Not committed) Stores the bot token secret
└── .venv/               # Python virtual environment folder
```

---

## Expected Message Format

The bot is built to parse forwarded Telegram messages that follow this structure:

```
SALARY. 15%.

1. Client's Name   : Meiora
2. Session Type    : VIP I
   = 34.850 IDR
   Agency Income   = 6.150 IDR
5. Link Payment    :
```

If the message does not contain the word `SALARY`, the bot will ignore it entirely.

---

## CSV Output Example

The extracted data is saved to `data_salary.csv` in the following format:

| Persentase | Client Name | Session Type | Talent Income (IDR) | Agency Income (IDR) | Link Payment |
|------------|-------------|--------------|----------------------|----------------------|--------------|
| 15%        | Meiora      | VIP I        | 34.850               | 6150                 |              |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| python-telegram-bot | Telegram Bot API wrapper for receiving messages |
| python-dotenv | Loads environment variables from `.env` file |
| re (RegEx) | Parses and extracts structured fields from message text |
| csv | Writes extracted data into a CSV file |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))
- The bot must be added as a member or admin to the target Telegram group

### 1. Clone the Repository

```
git clone https://github.com/your-username/tele-salary-bot.git
cd tele-salary-bot
```

### 2. Create a Virtual Environment

```
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS/Linux
```

### 3. Install Dependencies

```
pip install -r requirement.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```
BOT_TOKEN=your_telegram_bot_token_here
```

Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the Bot

```
python main.py
```

The bot is now live and monitoring the group. When a salary message is detected, it will log:

```
Data tersimpan ke CSV | Client: Meiora
```

---

## How It Works

```
Telegram Group Message
        |
        v
  Contains "SALARY"?
    |           |
   YES          NO --> Ignored
    |
    v
RegEx Extraction
  - Percentage
  - Client Name
  - Session Type
  - Talent Income
  - Agency Income
  - Link Payment
        |
        v
  Append row to data_salary.csv
```

---

## Limitations

- The bot only works with messages that strictly follow the expected salary message format
- It only processes text messages — images, stickers, or media without captions are ignored
- The CSV file grows indefinitely with no built-in data management or deduplication
- No web interface or dashboard — data must be viewed by opening the CSV file manually

---

## What I Learned

This project was built to practice and explore:

- How to create and configure a Telegram Bot using `python-telegram-bot`
- Using polling to listen for real-time messages in a Telegram group
- Writing Regular Expressions (RegEx) to extract structured data from unstructured text
- Managing environment variables securely using `.env` and `python-dotenv`
- Automating file I/O operations with Python's built-in `csv` module

---

## License

This project is open-source and available under the [MIT License](LICENSE).
Feel free to fork, study, or modify it, but this is not production-ready.

---

*Made as a personal learning project.*
