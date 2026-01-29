from flask import Blueprint, render_template
import json
import threading
from discord.ext import commands
import asyncio

discord_routes = Blueprint("discord", __name__)

bot_instance = None
bot_thread = None
bot_loop = None
user_data = {}  

def start_discord_bot(token):
    global bot_instance, bot_loop

    bot_instance = commands.Bot(command_prefix="!", self_bot=True)

    @bot_instance.command()
    async def userinfo(ctx, user_id: int):
        try:
            user = await bot_instance.fetch_user(user_id)
            user_data.clear()
            user_data.update({
                "username": f"{user.name}#{user.discriminator}",
                "id": user.id,
                "created_at": user.created_at,
                "avatar": user.avatar.url
            })
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")

    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    bot_loop.run_until_complete(bot_instance.start(token))

@discord_routes.route('/discord')
def discord_route():
    global bot_thread

    with open("./config.json", "r") as f:
        config = json.load(f)
    discord_token = config["discord"]["token"]

    if not discord_token:
        return render_template("error.html", error_title="Required Field Missing!", error_description="You have not placed your token in the config file.", redirect="index")

    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=start_discord_bot, args=(discord_token,))
        bot_thread.start()

    return render_template('discord.html', user_data=user_data)

@discord_routes.route('/discord/stop')
def stop_discord_bot():
    global bot_instance, bot_loop, bot_thread

    if bot_instance and bot_loop and bot_thread and bot_thread.is_alive():
        asyncio.run_coroutine_threadsafe(bot_instance.close(), bot_loop)
        bot_thread.join()
        bot_instance = None
        bot_loop = None
        bot_thread = None
        return render_template('home.html')
    else:
        return render_template('discord.html', user_data=user_data)

# Display userinfo
@discord_routes.route('/discord/user_data')
def get_user_data():
    if not user_data:
        html = '''
        <div class="p-5 bg-neutral-900 border border-neutral-700 rounded"> 
            <h1 class="text-white font-semibold text-[23px]">No Users Found</h1>
            <p class="text-neutral-500 font-semibold text-[14px]">
                You have not looked up any users on Discord yet. To lookup a user, type !userinfo [user_id]
            </p>
        </div>
        <div class="p-5 bg-neutral-900 border border-neutral-700 rounded mt-3"> 
            <a href="/discord/stop" class="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-md font-semibold">
                Stop Discord Bot
            </a>
        </div>
        '''
    else:
        html = '''
        <div class="p-5 bg-neutral-900 border border-neutral-700 rounded flex space-x-5 items-center"> 
            <img src="{user_data.get('avatar')}" alt="Avatar" class="w-16 h-16 rounded-full">
            <div>
                <h1 class="text-white font-semibold text-[23px]">{user_data.get('username')}</h1>
                <p class="text-neutral-500 font-semibold text-[14px]">ID: {user_data.get('id')}</p>
                <p class="text-neutral-500 font-semibold text-[14px]">Created at: {user_data.get('created_at')}</p>
            </div>
        </div>
        <div class="p-5 bg-neutral-900 border border-neutral-700 rounded mt-3"> 
            <a href="/discord/stop" class="bg-red-500 hover:bg-red-500 text-white px-4 py-2 rounded-md font-semibold">
                Stop
            </a>
        </div>
        '''
    return html
