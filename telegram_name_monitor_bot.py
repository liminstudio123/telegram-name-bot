from telegram import Update
from telegram.ext import Application, ContextTypes, ChatMemberHandler, CommandHandler
import os
import asyncio
import logging

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量获取 bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8083024089:AAFM9bktsdkeUQvKMRYwtp-oXXIP4UqHt-Q")
logger.info(f"Using BOT_TOKEN: {BOT_TOKEN[:10]}...")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令"""
    try:
        user = update.effective_user
        welcome_message = (
            f"👋 你好 {user.first_name}!\n\n"
            "我是名字变更监控机器人。\n"
            "请将我添加到群组并设置为管理员，我会监控群成员的名字变更。"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"Sent welcome message to user {user.id}")
    except Exception as e:
        logger.error(f"Error in start_command: {str(e)}", exc_info=True)

async def track_chat_member_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理群组成员信息更新"""
    try:
        # 确保这是一个成员更新事件
        if not update.chat_member:
            return
        
        logger.info(f"Received chat member update in chat {update.chat_member.chat.id}")
        
        # 获取新旧状态
        old_chat_member = update.chat_member.old_chat_member
        new_chat_member = update.chat_member.new_chat_member
        
        # 检查名字是否发生变化
        if (old_chat_member.user.first_name != new_chat_member.user.first_name or 
            old_chat_member.user.last_name != new_chat_member.user.last_name):
            
            # 构建旧名字
            old_full_name = f"{old_chat_member.user.first_name or ''} {old_chat_member.user.last_name or ''}".strip()
            # 构建新名字
            new_full_name = f"{new_chat_member.user.first_name or ''} {new_chat_member.user.last_name or ''}".strip()
            
            logger.info(f"Name change detected: {old_full_name} -> {new_full_name}")
            
            # 发送通知消息
            message = (
                f"群成员更改了名字\n"
                f"原名字: {old_full_name}\n"
                f"新名字: {new_full_name}"
            )
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text=message
            )
            logger.info("Notification sent successfully")
    except Exception as e:
        logger.error(f"Error in track_chat_member_updates: {str(e)}", exc_info=True)

async def main() -> None:
    """启动机器人"""
    try:
        # 创建应用
        application = Application.builder().token(BOT_TOKEN).build()
        logger.info("Application created successfully")

        # 添加处理程序
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(ChatMemberHandler(track_chat_member_updates))
        logger.info("Handlers added successfully")

        # 启动机器人
        logger.info("Starting bot...")
        await application.run_polling(allowed_updates=["chat_member", "message"])
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)

if __name__ == "__main__":
    try:
        logger.info("Bot script started")
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            logger.info("Event loop already running, using existing loop")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True) 