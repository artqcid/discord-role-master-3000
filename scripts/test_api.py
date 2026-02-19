import requests
import json

BASE_URL = "http://localhost:8001/api"

try:
    # 1. Get Guild ID
    resp = requests.get(f"{BASE_URL}/guild")
    resp.raise_for_status()
    guild = resp.json()
    guild_id = guild.get("id")
    print(f"Guild ID: {guild_id}")
    
    if not guild_id:
        print("ERROR: No Guild ID in response!")
        exit(1)
        
    # 2. Get Roles
    roles_url = f"{BASE_URL}/guild/{guild_id}/roles"
    print(f"Calling Roles: {roles_url}")
    
    resp_roles = requests.get(roles_url)
    print(f"Status Code: {resp_roles.status_code}")
    
    if resp_roles.status_code == 200:
        roles = resp_roles.json()
        print(f"Roles count: {len(roles)}")
        if roles:
            print(f"First role: {roles[0]}")
    else:
        print(f"Error Body: {resp_roles.text}")
        
except Exception as e:
    print(f"CRASH: {e}")
