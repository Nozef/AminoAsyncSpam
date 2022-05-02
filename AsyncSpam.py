import aminoed
from asyncio import gather, create_task

async def auth(client: aminoed.Client):
    try:
        await client.login(email=input("Email >> "), password=input("Password >> "))
    except Exception as e:
        print(e)
        await auth(client)

async def choise_community(client : aminoed.Client):
    clients = await client.get_account_communities(start=0, size=100)
    for x, community in enumerate(clients, 1):
        print(f"{x}.{community.name}")
    select = int(input("Select community >> "))
    comId = clients[select - 1].comId
    return comId 

async def choise_chat(subclient: aminoed.CommunityClient):
    chats = await subclient.get_chat_threads(start=0, size=100)
    for z, chat in enumerate(chats, 1):
        print(f"{z}.{chat.title}")
    select = int(input("Select chat >> "))
    chatId = chats[select - 1].chatId
    return chatId

async def send_message(subclient: aminoed.CommunityClient, chatId: str, message: str, messageType: int):
    while True:
        await gather(*[create_task(subclient.send_message(chatId=chatId, message=message, type=messageType)) for _ in range(350)])

@aminoed.run_with_client()
async def main(client: aminoed.Client):
    await auth(client)
    subclient = aminoed.CommunityClient(comId=await choise_community(client))
    await send_message(subclient, await choise_chat(subclient), message=input("Message >> "), messageType=input("Message type >> "))
