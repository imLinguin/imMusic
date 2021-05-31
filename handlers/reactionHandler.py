from commands import queue as queue_cmd
from commands import back, skip, loop
from lib import utils


async def handle(reaction, member):
    queue = utils.get_queue(reaction.message.guild.id)
    if not queue or not queue.voice_connection:
        return
    if member.voice.channel.id != queue.voice_connection.channel.id or member.id == queue.voice_connection.user.id:
        return
    print(f"REACTION EMOJI: {reaction.emoji} GUILD: {reaction.message.guild.name}")
    if queue.now_playing.id == reaction.message.id:
        if reaction.emoji == "⏮":
            await back.run(reaction.message)
        elif reaction.emoji == "⏯":
            if not utils.get_queue(reaction.message.guild.id).voice_connection.is_paused():
                utils.pause(reaction.message)
            else:
                utils.resume(reaction.message)
        elif reaction.emoji == "⏭":
            await skip.run(reaction.message)
        elif reaction.emoji == "🔃":
            await loop.run(reaction.message)
        elif reaction.emoji == "⏹":
            await utils.destroy_queue(reaction.message.guild.id)
            return
    elif queue.queue_message.id == reaction.message.id:
        # Queue User reacted to our message
        if reaction.emoji == "⬇":
            queue.queue_page += 1
            await queue_cmd.run(queue.first_message)
        elif reaction.emoji == "⬆":
            queue.queue_page -= 1
            await queue_cmd.run(queue.first_message)
        elif reaction.emoji == "❌":
            await queue.queue_message.delete()
            queue.queue_message = None
            return
