from datetime import datetime
import os
import re
import json
import gspread
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# --- KONFIGURASI ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Hubungkan ke Google Sheets menggunakan koneksi aman (Deployment-Friendly)
try:
    # 1. Cek apakah ada file credentials.json di folder (untuk laptop lokal)
    if os.path.exists("credentials.json"):
        gc = gspread.service_account(filename="credentials.json")
        print("✅ [Lokal] Berhasil terhubung ke Google Sheets menggunakan file json!")
    
    # 2. Jika file tidak ada, berarti sedang jalan di Render (menggunakan .env)
    else:
        creds_json = os.getenv("GOOGLE_CREDENTIALS")
        creds_dict = json.loads(creds_json)
        gc = gspread.service_account_from_dict(creds_dict)
        print("✅ [Cloud] Berhasil terhubung ke Google Sheets menggunakan Env Variable!")
    
    # Buka Google Sheets berdasarkan ID
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
except Exception as e:
    print(f"❌ Gagal terhubung ke Google Sheets: {e}")

# Fungsi untuk mengekstrak data dari teks dengan RegEx
import re

def parse_text(text):
    # Inisialisasi dictionary (Typo 'presentase' sudah diperbaiki jadi 'persentase')
    data = {
        "periods": "", "persentase": "", "talent_name": "", "client_name": "",
        "session_type": "", "talent_income": "", "agency_income": "", "feeq": "", "link_payment": ""
    }

    data["periods"] = datetime.now().strftime("%d-%m-%Y")

    # 2. Ambil Persentase SALARY
    perc_match = re.search(r"SALARY\.\s*(\d+)%", text, re.IGNORECASE)
    if perc_match: data["persentase"] = perc_match.group(1) + "%"
        
    # 3. Ambil Talent's Name
    talent_match = re.search(r"Talent['’]s\s+Name\s*[:=]\s*(.*)", text, re.IGNORECASE)
    if talent_match: data["talent_name"] = talent_match.group(1).strip()

    # 4. Ambil Client's Name
    client_match = re.search(r"1\. Client['’]s\s+Name\s*[:=]\s*(.*)", text, re.IGNORECASE)
    if client_match: data["client_name"] = client_match.group(1).strip()
        
    # 5. Ambil Session Type
    session_match = re.search(r"2\. Session\s+Type\s*[:=]\s*(.*)", text, re.IGNORECASE)
    if session_match: data["session_type"] = session_match.group(1).strip()
        
    # 6. Ambil FEEQ
    feeq_match = re.search(r"FEEQ\s*[:=]\s*([\d.]+)", text, re.IGNORECASE)
    if feeq_match: data["feeq"] = feeq_match.group(1).strip()
        
    # 7. Ambil Talent's Income
    income_match = re.search(r"=\s*([\d.]+)\s*IDR", text, re.IGNORECASE)
    if income_match: data["talent_income"] = income_match.group(1).strip()
        
    # 8. Ambil Agency Income
    agency_match = re.search(r"Agency\s+Income\s*[:=]\s*([\d.]+)\s*IDR", text, re.IGNORECASE)
    if agency_match: data["agency_income"] = agency_match.group(1).strip()
        
    # 9. Ambil Link Payment
    link_match = re.search(r"6\. Link\s+payment\s*[:=]\s*(.*)", text, re.IGNORECASE)
    if link_match: data["link_payment"] = link_match.group(1).strip()
        
    return data

def run_dummy_server():
    port = int(os.getenv("PORT", 8080))
    server_addres=s = ('', port)
    httpd = HTTPServer(server_addres, SimpleHTTPRequestHandler)
    print(f"🚀 Dummy server berjalan di port {port} untuk menjaga koneksi tetap hidup...")
    httpd.serve_forever()


# Handler ketika ada pesan masuk ke grup
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    text = update.message.text or update.message.caption
    if not text:
        return
    
    if "SALARY" in text.upper():
        parsed_data = parse_text(text)
        try:
            sheet.append_row([
                parsed_data["periods"],
                parsed_data["persentase"],
                parsed_data["talent_name"],
                parsed_data["client_name"],
                parsed_data["session_type"],
                parsed_data["feeq"],
                parsed_data["talent_income"],
                parsed_data["agency_income"],
                parsed_data["link_payment"]
            ])
            print(f"✅ Data tersimpan ke Google Sheets | Client: {parsed_data['client_name']}, Talent: {parsed_data['talent_name']}")
        except Exception as err:
            print(f"❌ Gagal menulis ke Google Sheets: {err}")

# Fungsi utama untuk menjalankan bot
def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()

    app = Application.builder().token(TOKEN).connect_timeout(30.0).read_timeout(30.0).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot sedang berjalan dan memantau grup...")
    app.run_polling()

if __name__ == "__main__":
    main()