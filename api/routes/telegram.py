import os
import json
import ast
from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, status
from telegram import Bot, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.errors import TelegramError, BadRequest, Forbidden
import logging

from ..db import supabase
from ..models import TelegramUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/telegram", tags=["telegram"])

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.warning("No TELEGRAM_BOT_TOKEN provided!")

ADMIN_USER_ID = int(os.environ.get("ADMIN_USER_ID", "0"))

@router.post("/webhook")
async def webhook(request: Request):
    """Handle incoming updates from Telegram."""
    if not TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bot token not configured"
        )

    try:
        # Get update data
        data = await request.json()
        logger.info(f"Received update: {data.get('update_id', 'No update_id')}")

        # Create bot instance
        bot = Bot(token=TOKEN)

        # Process update directly
        update = Update.de_json(data, bot)

        # Handle different update types
        if update.message:
            await handle_message(bot, update)
        elif update.inline_query:
            await handle_inline_query(bot, update)
        elif update.callback_query:
            await handle_callback_query(bot, update)
        elif update.chosen_inline_result:
            await handle_chosen_inline_result(bot, update)

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


async def handle_message(bot: Bot, update: Update):
    """Handle regular messages."""
    message = update.message
    user = message.from_user

    # Store user in database
    await store_user(user.id, None)

    if message.text:
        text = message.text.strip()
        if text.startswith('/start'):
            await send_start_message(bot, message)
        elif text.startswith('/help'):
            await send_help_message(bot, message)
        elif text.startswith('/stats') and user.id == ADMIN_USER_ID:
            await send_stats_message(bot, message)


async def handle_inline_query(bot: Bot, update: Update):
    """Handle inline queries for whisper creation."""
    query = update.inline_query
    query_text = query.query.strip()
    sender_id = query.from_user.id

    # Store user
    await store_user(sender_id, None)

    results = []

    if not query_text:
        # Empty query - show main result
        results = [get_main_result()]
    else:
        # Parse query to extract message and target
        parts = query_text.split()
        if len(parts) >= 2:
            target = parts[-1]
            message = " ".join(parts[:-1])

            try:
                # Try to get target user
                if target.startswith('@'):
                    target_user = await bot.get_chat(target)
                else:
                    target_user = await bot.get_chat(int(target))

                # Create whisper result
                data_list = [sender_id, target_user.id]
                name = target_user.first_name
                if target_user.last_name:
                    name += f" {target_user.last_name}"

                # Store target user info for sender
                target_user_data = {
                    "id": target_user.id,
                    "first_name": target_user.first_name,
                    "last_name": target_user.last_name,
                    "username": target_user.username
                }
                await store_user(sender_id, target_user_data)

                results = [InlineQueryResultArticle(
                    id="whisper",
                    title=f"🔒 Whisper to {name}",
                    description="Only they can open this message",
                    input_message_content=InputTextMessageContent(
                        f"🔒 A whisper message to {target_user.mention_html()} 🔒\nOnly they can open it.",
                        parse_mode="HTML"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔐 Show Message 🔐", callback_data=str(data_list))
                    ]])
                )]
            except Exception as e:
                logger.error(f"Error getting target user: {e}")
                results = await get_previous_target_results(sender_id) or [get_main_result()]
        else:
            # Single word - show previous target or main
            results = await get_previous_target_results(sender_id) or [get_main_result()]

    try:
        await query.answer(results, cache_time=1)
    except Exception as e:
        logger.error(f"Error answering inline query: {e}")


async def handle_callback_query(bot: Bot, update: Update):
    """Handle callback queries for whisper viewing."""
    callback_query = update.callback_query
    user_id = callback_query.from_user.id

    try:
        # Handle navigation callbacks
        if callback_query.data in ["home", "help", "about"]:
            await handle_navigation_callback(bot, callback_query)
            return

        # Parse callback data for whisper access
        data_list = ast.literal_eval(callback_query.data)

        if user_id in data_list:
            # User is authorized to see whisper
            inline_message_id = callback_query.inline_message_id

            if supabase and inline_message_id:
                try:
                    result = supabase.table("whispers").select("message").eq(
                        "inline_message_id", inline_message_id
                    ).execute()

                    if result.data and len(result.data) > 0:
                        message = result.data[0]["message"]
                        await callback_query.answer(f"🔒 Whisper: {message}", show_alert=True)
                    else:
                        await callback_query.answer("❌ Message not found or expired", show_alert=True)
                except Exception as e:
                    logger.error(f"Error fetching whisper: {e}")
                    await callback_query.answer("❌ Error retrieving message", show_alert=True)
            else:
                await callback_query.answer("❌ Database not available", show_alert=True)
        else:
            await callback_query.answer(
                "🚫 Sorry, this whisper is not meant for you!",
                show_alert=True
            )
    except (ValueError, SyntaxError):
        await callback_query.answer("❌ Invalid request", show_alert=True)
    except Exception as e:
        logger.error(f"Error handling callback: {e}")
        await callback_query.answer("❌ Error processing request", show_alert=True)


async def handle_navigation_callback(bot: Bot, callback_query):
    """Handle navigation callback queries."""
    user = callback_query.from_user
    
    if callback_query.data == "home":
        text = f"""
🔒 **Welcome to WhispierBot** 🔒

Hello {user.mention_html()}!

I help you send secret messages (whispers) that only specific people can read, even in public groups!

**How to use me:**
1. Type `@whispierbot` in any chat
2. Write your message followed by the recipient's @username
3. Send it - only they can open the whisper!

**Example:** `@whispierbot Hello there! @username`

Built with ❤️ using PyVueBot by @venopyx
        """
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔒 Try Whisper", switch_inline_query="")],
            [InlineKeyboardButton("📖 Help", callback_data="help")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")]
        ])
    elif callback_query.data == "help":
        text = """
📖 **How to Use WhispierBot**

**Step 1:** Type `@whispierbot` in any chat
**Step 2:** Write your secret message
**Step 3:** Add the recipient's @username or ID at the end
**Step 4:** Send it!

**Example:**
`@whispierbot This is a secret message @john`

**Features:**
✅ Works in any chat or group
✅ Only the recipient can read the message
✅ Messages are secure and private
✅ No one else can see the content

**Note:** The recipient must have started the bot at least once.
        """
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔒 Try Now", switch_inline_query="")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ])
    elif callback_query.data == "about":
        text = """
ℹ️ **About WhispierBot**

**What is this bot?**
WhispierBot allows you to send secret messages that only specific people can read, even in public chats!

**How it works:**
- Your message is securely stored
- Only you and the recipient can access it
- Works in any Telegram chat or group
- Messages expire after 7 days for security

**Technology:**
🚀 Built with FastAPI and PyVueBot
💾 Powered by Supabase database
⚡ Deployed on Vercel for reliability

**Developer:** @venopyx
**Source:** Open source and secure
        """
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔒 Send Whisper", switch_inline_query="")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ])
    
    try:
        await callback_query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except BadRequest:
        # Message content is the same, just answer the callback
        await callback_query.answer()


async def handle_chosen_inline_result(bot: Bot, update: Update):
    """Handle chosen inline results to store whispers."""
    result = update.chosen_inline_result

    if not result.query.strip():
        return

    try:
        parts = result.query.split()
        if len(parts) >= 2:
            target = parts[-1]
            message = " ".join(parts[:-1])

            # Get target user ID
            try:
                if target.startswith('@'):
                    target_user = await bot.get_chat(target)
                else:
                    target_user = await bot.get_chat(int(target))

                recipient_ids = [result.from_user.id, target_user.id]
            except:
                recipient_ids = [result.from_user.id]
        else:
            message = result.query
            recipient_ids = [result.from_user.id]

        # Store whisper in database
        if supabase and result.inline_message_id:
            try:
                supabase.table("whispers").insert({
                    "inline_message_id": result.inline_message_id,
                    "message": message,
                    "sender_id": result.from_user.id,
                    "recipient_ids": recipient_ids
                }).execute()
                logger.info(f"Stored whisper: {result.inline_message_id}")
            except Exception as e:
                logger.error(f"Error storing whisper: {e}")
    except Exception as e:
        logger.error(f"Error processing chosen result: {e}")


async def get_previous_target_results(sender_id: int):
    """Get previous target results for the user."""
    if not supabase:
        return None

    try:
        result = supabase.table("users").select("target_user").eq("id", sender_id).execute()
        
        if result.data and len(result.data) > 0:
            target_user_data = result.data[0].get("target_user")
            if target_user_data:
                receiver_id = target_user_data["id"]
                data_list = [sender_id, receiver_id]
                first_name = target_user_data["first_name"]
                last_name = target_user_data.get("last_name", "")
                name = f"{first_name} {last_name}".strip()
                
                text1 = f"🔒 A whisper message to {name}"
                text2 = "Only they can open it."
                mention = f"[{name}](tg://user?id={receiver_id})"
                
                return [
                    InlineQueryResultArticle(
                        id="previous_target",
                        title=text1,
                        input_message_content=InputTextMessageContent(
                            f"🔒 A whisper message to {mention} 🔒\n{text2}",
                            parse_mode="Markdown"
                        ),
                        description=text2,
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "🔐 Show Message 🔐",
                                callback_data=str(data_list)
                            )
                        ]])
                    ),
                    get_main_result()
                ]
    except Exception as e:
        logger.error(f"Error getting previous target: {e}")
    
    return None


def get_main_result():
    """Get the main inline query result."""
    return InlineQueryResultArticle(
        id="main",
        title="🔒 WhispierBot",
        description="Send secret messages that only specific users can read",
        input_message_content=InputTextMessageContent(
            "🔒 Write your message followed by the recipient's @username or ID\n\n"
            "**Example:** `Hello there! @username`\n\n"
            "Start typing to create your whisper message!"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 Learn More", url="https://t.me/whispierbot?start=help")],
            [InlineKeyboardButton("🔒 Try Whisper", switch_inline_query="")]
        ])
    )


async def store_user(user_id: int, target_user_data: Dict[str, Any] = None):
    """Store or update user in database."""
    if not supabase:
        return

    try:
        # Check if user exists
        result = supabase.table("users").select("id").eq("id", user_id).execute()
        
        if result.data and len(result.data) > 0:
            # User exists, update if target_user_data provided
            if target_user_data:
                supabase.table("users").update({
                    "target_user": target_user_data
                }).eq("id", user_id).execute()
        else:
            # New user
            supabase.table("users").insert({
                "id": user_id,
                "target_user": target_user_data
            }).execute()
    except Exception as e:
        logger.error(f"Error storing user {user_id}: {e}")


async def send_start_message(bot: Bot, message):
    """Send start message."""
    user = message.from_user
    text = f"""
🔒 **Welcome to WhispierBot** 🔒

Hello {user.mention_html()}!

I help you send secret messages (whispers) that only specific people can read, even in public groups!

**How to use me:**
1. Type `@whispierbot` in any chat
2. Write your message followed by the recipient's @username
3. Send it - only they can open the whisper!

**Example:** `@whispierbot Hello there! @username`

Built with ❤️ using PyVueBot by @venopyx
    """

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔒 Try Whisper", switch_inline_query="")],
        [InlineKeyboardButton("📖 Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending start message: {e}")


async def send_help_message(bot: Bot, message):
    """Send help message."""
    text = """
📖 **How to Use WhispierBot**

**Step 1:** Type `@whispierbot` in any chat
**Step 2:** Write your secret message
**Step 3:** Add the recipient's @username or ID at the end
**Step 4:** Send it!

**Example:**
`@whispierbot This is a secret message @john`

**Features:**
✅ Works in any chat or group
✅ Only the recipient can read the message
✅ Messages are secure and private
✅ No one else can see the content

**Note:** The recipient must have started the bot at least once.
    """

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔒 Try Now", switch_inline_query="")],
        [InlineKeyboardButton("🏠 Back to Start", callback_data="home")]
    ])

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending help message: {e}")


async def send_stats_message(bot: Bot, message):
    """Send stats message (admin only)."""
    if not supabase:
        await bot.send_message(message.chat.id, "❌ Database not available")
        return

    try:
        users_result = supabase.table("users").select("id", count="exact").execute()
        whispers_result = supabase.table("whispers").select("inline_message_id", count="exact").execute()

        users_count = users_result.count or 0
        whispers_count = whispers_result.count or 0

        text = f"""
📊 **WhispierBot Statistics**

👥 **Total Users:** {users_count:,}
💬 **Total Whispers:** {whispers_count:,}
🚀 **Status:** Active
⚡ **Platform:** Vercel + Supabase
🛠️ **Developer:** @venopyx

**System Status:** ✅ All systems operational
        """

        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await bot.send_message(message.chat.id, f"❌ Error getting stats: {e}")


@router.get("/setup-webhook")
async def setup_webhook(webhook_url: str = None):
    """Setup webhook for the bot."""
    if not TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bot token not configured"
        )

    if not webhook_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="webhook_url parameter is required"
        )

    try:
        bot = Bot(token=TOKEN)
        # First, delete any existing webhook
        await bot.delete_webhook(drop_pending_updates=True)

        # Set new webhook
        success = await bot.set_webhook(url=webhook_url)
        if success:
            webhook_info = await bot.get_webhook_info()
            logger.info(f"Webhook set to: {webhook_info.url}")
            return {
                "status": "success",
                "message": f"Webhook set to {webhook_url}",
                "webhook_info": {
                    "url": webhook_info.url,
                    "has_custom_certificate": webhook_info.has_custom_certificate,
                    "pending_update_count": webhook_info.pending_update_count,
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to set webhook"
            )
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )