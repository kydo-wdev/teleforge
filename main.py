import os
import threading
from flask import Flask
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

load_dotenv()

# --- 1. HTTP SERVER PARA SA BACK4APP HEALTH CHECK ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_http_server():
    # Kukunin ang port mula sa environment, default ay 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. ORIGINAL BOT LOGIC ---
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))

# Members to receive the link via DM
MEMBERS_TO_NOTIFY = ['prakhargupta', 'edrianzeropenny']

client = TelegramClient('teleforge_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/creategroup (.+)'))
async def create_group(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return 

    group_name = event.pattern_match.group(1).strip()
    status_msg = await event.respond(f"⏳ Creating: **{group_name}**...")

    try:
        # 1. Create the group (Just you)
        result = await client(CreateChatRequest(title=group_name, users=['me']))
        
        # 2. Extract Chat ID
        new_chat_id = None
        if hasattr(result, 'chats') and result.chats:
            new_chat_id = result.chats[0].id
        elif hasattr(result, 'updates') and isinstance(result.updates, list):
            for u in result.updates:
                if hasattr(u, 'chat_id'):
                    new_chat_id = u.chat_id
                    break
        
        if not new_chat_id:
            # Search fallback
            async for dialog in client.iter_dialogs(limit=5):
                if dialog.name == group_name:
                    new_chat_id = dialog.id
                    break

        # 3. Get the Invite Link
        invite = await client(ExportChatInviteRequest(peer=new_chat_id))
        invite_link = invite.link

        # 4. DM the link to the members
        dm_log = []
        for username in MEMBERS_TO_NOTIFY:
            try:
                message = f"Hello! You've been invited to join the group: **{group_name}**\nJoin here: {invite_link}"
                await client.send_message(username, message)
                dm_log.append(f"📩 DM sent to @{username}")
            except Exception as e:
                dm_log.append(f"❌ Failed to DM @{username} (User must message bot first or blocked)")

        # 5. Final Report
        await status_msg.edit(
            f"🚀 **Group Created!**\n\n"
            f"**Name:** {group_name}\n"
            f"{'\n'.join(dm_log)}\n\n"
            f"🔗 **Group Link:** {invite_link}"
        )

    except Exception as e:
        await status_msg.edit(f"⚠️ **Error:** `{str(e)}`")

# --- 3. RUNNING THE BOT AND SERVER ---
if __name__ == '__main__':
    # Patatakbuhin ang Flask sa background thread
    threading.Thread(target=run_http_server, daemon=True).start()
    
    print("HTTP Server started on port 8080. TeleForge is starting...")
    
    client.start()
    client.run_until_disconnected()