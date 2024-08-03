import requests
import json
import random
import time
from datetime import datetime

def read_accounts(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

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
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return None
    else:
        print(f"Login failed: {response.status_code}")
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
            return response.json().get('tasks', [])
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return []
    else:
        print(f"Task check failed: {response.status_code}")
        return []

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
            print(f"tgUsername: {account_info.get('tgUsername', 'N/A')}")
            print(f"points: {account_info.get('points', 'N/A')}")
            print(f"tgWalletAddress: {account_info.get('tgWalletAddress', 'N/A')}")
            print(f"vanaWalletAddress: {account_info.get('vanaWalletAddress', 'N/A')}")
        
            tasks = check_tasks(account)
            for task in tasks:
                if task['name'] in ["Refer a friend", "Connect Wallet", "Connect Telegram Wallet"]:
                    continue
                if task['name'] == "Play game":
                    repetitions = random.randint(5, 10)
                    for _ in range(repetitions):
                        points = random.uniform(0.8, 2.0)
                        print(f"Completing task: {task['name']} with {points} points (iteration)")
                        complete_task(task['id'], points, account)
                        time.sleep(2)
                else:
                    points = task['points']
                    print(f"Completing task: {task['name']} with {points} points")
                    complete_task(task['id'], points, account)
                    time.sleep(2)
        
        time.sleep(5)

    print("\nAll accounts processed. Waiting for 1 hour before restarting...")
    for remaining in range(3600, 0, -1):
        print(f"\r{remaining//60:02}:{remaining%60:02} remaining", end="")
        time.sleep(1)

if __name__ == "__main__":
    main()
