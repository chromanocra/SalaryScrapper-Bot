import csv
import re
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# --- KONFIGURASI ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CSV_FILE = "data_salary.csv"

# Fungsi untuk membuat file CSV dan header jika belum ada
def setup_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Persentase", "Client Name", "Session Type", 
                "Talent Income (IDR)", "Agency Income (IDR)", "Link Payment"
            ])

# Fungsi untuk mengekstrak data dari teks dengan RegEx
def parse_text(text):
    data = {
        "persentase": "",
        "client_name": "",
        "session_type": "",
        "talent_income": "",
        "agency_income": "",
        "link_payment": ""
    }
    
    # 1. Ambil Persentase (contoh: SALARY. 15%.)
    perc_match = re.search(r"SALARY\.\s*(\d+)%", text)
    if perc_match:
        data["persentase"] = perc_match.group(1) + "%"
        
    # 2. Ambil Nama Client
    client_match = re.search(r"1\. Client's Name:\s*(.+)", text)
    if client_match:
        data["client_name"] = client_match.group(1).strip()
        
    # 3. Ambil Session Type
    session_match = re.search(r"2\. Session Type:\s*(.+)", text)
    if session_match:
        data["session_type"] = session_match.group(1).strip()
        
    # 4. Ambil Talent Income (mengambil angka setelah '=' pertama yang diikuti 'IDR')
    talent_match = re.search(r"=\s*([\d.]+)\s*IDR", text)
    if talent_match:
        data["talent_income"] = talent_match.group(1).strip()
        
    # 5. Ambil Agency Income
    agency_match = re.search(r"Agency Income\s*=\s*([\d.]+)\s*IDR", text, re.IGNORECASE)
    if agency_match:
        data["agency_income"] = agency_match.group(1).strip()
        
    # 6. Ambil Link Payment (jika ada isinya)
    link_match = re.search(r"5\. Link Payment\s*:\s*(.*)", text)
    if link_match:
        data["link_payment"] = link_match.group(1).strip()
        
    return data

# Handler ketika ada pesan masuk ke grup
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pastikan pesan memiliki teks (bukan cuma stiker/foto tanpa caption)
    if not update.message or not update.message.text:
        return
        
    text = update.message.text
    
    # Filter: Hanya proses pesan yang mengandung kata "SALARY"
    if "SALARY" in text:
        parsed_data = parse_text(text)
        
        # Tulis data yang sudah diekstrak ke dalam file CSV
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                parsed_data["persentase"],
                parsed_data["client_name"],
                parsed_data["session_type"],
                parsed_data["talent_income"],
                parsed_data["agency_income"],
                parsed_data["link_payment"]
            ])
            
        print(f"Data tersimpan ke CSV | Client: {parsed_data['client_name']}")

# Fungsi utama untuk menjalankan bot
def main():
    setup_csv()
    
    # Inisialisasi bot
    app = Application.builder().token(TOKEN).build()
    
    # Tambahkan listener untuk pesan teks
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("Bot sedang berjalan dan memantau grup...")
    app.run_polling()

if __name__ == "__main__":
    main()