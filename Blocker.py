import pyfiglet
from datetime import datetime, timedelta
import json
import os

hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
dataFile = os.path.join(os.path.expanduser("~"), "blocked_sites.json")

print(pyfiglet.figlet_format("WEBSITE BLOCKER", font = "big"))
print("by Cantilero, Cayabyab, Pasamanero, Quiblat")

def load_data():
    try:
        with open(dataFile, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(dataFile, 'w') as f:
        json.dump(data, f)

def block_site(sites, end_time):
    try:
        with open(hostsPath, 'a') as f:
            for site in sites:
                f.write(f"{redirect} {site}\n")
        
        data = load_data()
        for site in sites:
            data[site] = end_time.isoformat()
        save_data(data)
        print(f"Blocked: {sites}")
    except PermissionError:
        print("Run as administrator")

def unblock_site(sites):
    try:
        with open(hostsPath, 'r') as f:
            lines = f.readlines()
        
        with open(hostsPath, 'w') as f:
            for line in lines:
                if not any(site in line for site in sites):
                    f.write(line)
        
        data = load_data()
        for site in sites:
            data.pop(site, None)
        save_data(data)
        print(f"Unblocked: {sites}")
    except PermissionError:
        print("Run as administrator")

def check_expired():
    data = load_data()
    now = datetime.now()
    expired = []
    
    for site, end_time_str in data.items():
        end_time = datetime.fromisoformat(end_time_str)
        if now >= end_time:
            expired.append(site)
    
    if expired:
        print(f"Time's up! Unblocking: {expired}")
        unblock_site(expired)

def get_block_duration():
    print("\n1 - Hours")
    print("2 - Minutes")
    print("3 - Hours and Minutes")
    
    choice = input("Choose duration type: ")
    
    try:
        if choice == "1":
            hours = int(input("Enter hours: "))
            return datetime.now() + timedelta(hours=hours)
        elif choice == "2":
            minutes = int(input("Enter minutes: "))
            return datetime.now() + timedelta(minutes=minutes)
        elif choice == "3":
            hours = int(input("Enter hours: "))
            minutes = int(input("Enter minutes: "))
            return datetime.now() + timedelta(hours=hours, minutes=minutes)
        else:
            print("Invalid choice")
            return get_block_duration()
    except ValueError:
        print("Invalid input")
        return get_block_duration()

while True:
    check_expired()
    
    sites = [s.strip() for s in input("\nSites (comma-separated): ").split(",") if s.strip()]
    choice = input("Block (1) or Unblock (2)? ")
    
    if choice == "1":
        end_time = get_block_duration()
        block_site(sites, end_time)
    elif choice == "2":
        unblock_site(sites)
    
    if input("Continue? (y/n): ").lower() != 'y':
        break