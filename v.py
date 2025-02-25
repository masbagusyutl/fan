import requests
import random
import time
from datetime import datetime
import chardet

def read_accounts(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def decode_response(response):
    """
    Decode response content based on detected encoding.
    """
    result = chardet.detect(response.content)
    encoding = result['encoding'] if result['encoding'] else 'utf-8'
    try:
        return response.content.decode(encoding)
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try some common encodings
        for enc in ['latin1', 'iso-8859-1', 'cp1252']:
            try:
                return response.content.decode(enc)
            except UnicodeDecodeError:
                continue
        # If all decoding attempts fail, return the raw bytes
        return response.content

def login(telegram_data):
    url = "https://www.vanadatahero.com/api/player"
    headers = {
        "authority": "www.vanadatahero.com",
        "method": "GET",
        "path": "/api/player",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://www.vanadatahero.com/home",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "X-Telegram-Web-App-Init-Data": telegram_data
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            decoded_content = decode_response(response)
            print("Invalid JSON response")
            print(decoded_content)
            return None
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def check_tasks(telegram_data):
    url = "https://www.vanadatahero.com/api/tasks"
    headers = {
        "authority": "www.vanadatahero.com",
        "method": "GET",
        "path": "/api/tasks",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://www.vanadatahero.com/challenges",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "X-Telegram-Web-App-Init-Data": telegram_data
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            decoded_content = decode_response(response)
            print("Invalid JSON response")
            print(decoded_content)
            return None
    else:
        print(f"Task check failed: {response.status_code}")
        print(response.text)
        return None

def complete_task(task_id, points, telegram_data):
    url = f"https://www.vanadatahero.com/api/tasks/{task_id}"
    headers = {
        "authority": "www.vanadatahero.com",
        "method": "POST",
        "path": f"/api/tasks/{task_id}",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "35",
        "Content-Type": "application/json",
        "Origin": "https://www.vanadatahero.com",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://www.vanadatahero.com/home",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "X-Telegram-Web-App-Init-Data": telegram_data
    }
    payload = {
        "status": "completed",
        "points": points
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Task {task_id} completed successfully with {points} points.")
    else:
        print(f"Failed to complete task {task_id}: {response.status_code}")
        print(response.text)

def main():
    accounts = read_accounts('data.txt')
    total_accounts = len(accounts)
    for index, account in enumerate(accounts):
        print(f"\nProcessing account {index + 1} of {total_accounts}")
        
        account_info = login(account)
        if account_info:
            # Simpan informasi akun atau lakukan apa pun yang diperlukan dengan data ini
            # Untuk demonstrasi, kita hanya mencetak data teks mentah
            print(account_info)
        
            tasks = check_tasks(account)
            if tasks:
                # Proses setiap task yang ditemukan
                print(tasks)
                for _ in range(random.randint(5, 10)):  # Ulangi tugas secara acak antara 5 dan 10 kali
                    for task in tasks:
                        if task.get('name') in ["Refer a friend", "Connect Wallet", "Connect Telegram Wallet"]:
                            continue
                        points = random.uniform(0.8, 2.0)
                        print(f"Completing task: {task.get('name')} with {points:.2f} points (iteration)")
                        complete_task(task.get('id'), points, account)
                        time.sleep(2)
        
        time.sleep(5)

    print("\nAll accounts processed. Waiting for 1 hour before restarting...")
    for remaining in range(3600, 0, -1):
        print(f"\r{remaining//60:02}:{remaining%60:02} remaining", end="")
        time.sleep(1)

if __name__ == "__main__":
    main()
