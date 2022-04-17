
@dispatcher.message_handler(commands='start')
async def start(message: types.Message, user: User):
    await message.answer(f'Hello, {user.full_name}!')
