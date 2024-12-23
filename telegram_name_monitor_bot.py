from telegram import Update
from telegram.ext import Application, ContextTypes, ChatMemberHandler
import os
import asyncio

# 从环境变量获取 bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8083024089:AAFM9bktsdkeUQvKMRYwtp-oXXIP4UqHt-Q")

async def track_chat_member_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理群组成员信息更新"""
    # 确保这是一个成员更新事件
    if not update.chat_member:
        return
    
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

async def main() -> None:
    """启动机器人"""
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()

    # 添加处理程序
    application.add_handler(ChatMemberHandler(track_chat_member_updates))

    # 启动机器人
    print("机器人已启动...")
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            # Get the current event loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main()) 