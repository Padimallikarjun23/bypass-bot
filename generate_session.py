import os
import sys
from pyrogram import Client
from pathlib import Path

# Use the same API credentials as in by_bypass.py
api_id = 21782093
api_hash = "f5e475cf6683c633ceec9f34a453d39e"

# Clean up old session files
def cleanup_sessions():
    print("Cleaning up old sessions...")
    session_patterns = ["bypass_session.session", "*.session", "*.session-journal"]
    for pattern in session_patterns:
        for file in Path(".").glob(pattern):
            try:
                file.unlink()
                print(f"Deleted {file}")
            except Exception as e:
                print(f"Could not delete {file}: {e}")

async def main():
    # Clean up first
    cleanup_sessions()
    
    print("\nGenerating new session string...")
    print("You will need to log in with your phone number.")
    print("This account will be used to interact with DD_Bypass_Bot\n")
    
    try:
        # Use a unique session name
        async with Client(
            "temp_session",
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True
        ) as app:
            session_string = await app.export_session_string()
            print("\n✅ Successfully generated session string!")
            print("\n----------------------")
            print("Your session string:")
            print("----------------------")
            print(session_string)
            print("----------------------")
            
            print("\n⚠️ IMPORTANT INSTRUCTIONS:")
            print("1. Copy the session string above")
            print("2. Go to your Koyeb dashboard")
            print("3. Add it as an environment variable:")
            print("   Name: BYPASS_SESSION_STRING")
            print("   Value: (the session string above)")
            
            # Also save to a file for backup
            with open("session_string.txt", "w") as f:
                f.write(session_string)
            print("\n✅ Session string has also been saved to 'session_string.txt' for backup")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "AUTH_KEY_DUPLICATED" in str(e):
            print("\nError: Session conflict detected!")
            print("1. Make sure you're not running the bot elsewhere")
            print("2. Try again in a few minutes")
            print("3. If problem persists, contact @ragnarlothbrockV for support")

if __name__ == "__main__":
    try:
        import asyncio
        print("🔄 Starting session generation process...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Process cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Clean up temporary session files
        cleanup_sessions()
        print("\n✨ Cleanup completed")
