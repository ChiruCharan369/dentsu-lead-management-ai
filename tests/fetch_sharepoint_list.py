# fetch_sharepoint_list.py
import os, requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()  # reads .env in cwd

TENANT = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
HOSTNAME = "globalappsportal.sharepoint.com"
SITE_PATH = "/sites/DLQLeadQualificationOps"
LIST_NAME = "LeadManagementQueue"

if not (TENANT and CLIENT_ID and CLIENT_SECRET):
    raise SystemExit("Missing TENANT_ID/CLIENT_ID/CLIENT_SECRET in environment")

authority = f"https://login.microsoftonline.com/{TENANT}"
app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
token_resp = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
access_token = token_resp.get("access_token")
if not access_token:
    raise SystemExit(f"Failed to acquire token: {token_resp}")
headers = {"Authorization": f"Bearer {access_token}"}

# resolve site id by path
site_url = f"https://graph.microsoft.com/v1.0/sites/{HOSTNAME}:{SITE_PATH}"
r = requests.get(site_url, headers=headers)
r.raise_for_status()
site = r.json()
site_id = site["id"]

# get list items (expand fields)
items_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{LIST_NAME}/items?expand=fields&$top=200"
r = requests.get(items_url, headers=headers)
r.raise_for_status()
data = r.json()
print(data)  # or process data['value'] as needed