import discord
from discord.ext import commands
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import warnings
CREDENTIALS_FILE = 'crafty-hook-366323-29052cd4b0a9.json' #Данные сервисного аккаунта
spreadsheet_id = 'enter your sheet id here' #ID таблицы
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
@commands.has_any_role('ADM','MOD')
async def кик(ctx, member: discord.Member, *, reason):
    discordtag = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='D1:D1000',  # Столбец с дискордами
        majorDimension='ROWS'
    ).execute()
    rownum = discordtag.get('values').index([f'{member}'])
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"G{rownum+1}",
                 "majorDimension": "ROWS",
                 "values": [["FALSE"]]},
                {"range": f"H{rownum+1}",
                 "majorDimension": "COLUMNS",
                 "values": [[reason]]}
            ]
        }
    ).execute()



@bot.event
async def on_member_join(member):
    print(f'На сервер вошел участник {member}.')
    print(f'Поиск фамы')
    family = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='B1:B10', #Столбец с фамой
        majorDimension='ROWS'
    ).execute()
    print(f'Поиск никнейма')
    nickname = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='C1:C10', #Столбец с никами
        majorDimension='ROWS'
    ).execute()
    print(f'Поиск тега')
    discordtag = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='D1:D10', #Столбец с дискордами
        majorDimension='ROWS'
    ).execute()
    print(f'Проверка галки')
    infamily = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='G1:G10', #Столбец с галочками
        majorDimension='ROWS'
    ).execute()

    def makenickname(tag):
        rownum = discordtag.get('values').index([f'{tag}'])
        name = str(nickname.get('values')[rownum])[2:-2]
        purename = name.split(' ')[0]
        familytag = str(family.get('values')[rownum])[2:-2]
        nicknameequals = f'[{familytag}] {purename}'
        return (nicknameequals)

    try:
        dtag = member
        rownum = discordtag.get('values').index([f'{dtag}'])
        infam = str(infamily.get('values')[rownum])[2:-2]
        print(f'{dtag} в фаме - {infam}')
        print('Присваиваю никнейм...')
        await member.edit(nick=makenickname(dtag))
        await member.send('Вы присоединились к серверу Альянса. Никнейм назначен автоматически.')
        print(f'Присвоен ник {makenickname(dtag)}.')

        if infam == "TRUE":
            print('Выдаю роли...')
            familytag = str(family.get('values')[rownum])[2:-2]
            role = discord.utils.get(member.guild.roles, name=f'.{familytag}')
            role2 = discord.utils.get(member.guild.roles, name="FAMQ")
            await member.add_roles(role)
            await member.add_roles(role2)
            await member.send('Роли также выданы автоматически')
            print(f'Выданы роли FAMQ и {familytag}')
            print("----------------------------------------")

        else:
            print('Заявка участника еще не рассмотрена, выдать роли невозможно.')
            print("----------------------------------------")
            await member.send('Ваша заявка еще не проверена, поэтому роли будут выданы вам вручную овнером вашей фамы.')

    except:
        print('Участника нет в списках, либо возникла ошибка.')
        print("----------------------------------------")
        await member.send(f'Здравствуйте, {member.mention}! К сожалению, ваc нет в списке участников. Вам нужно заполнить форму, которую можно получить у овнера вашей фамы.')
# @bot.event
# async def on_member_remove(member):
#     discordtag = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheet_id,
#         range='D1:D1000',  # Столбец с дискордами
#         majorDimension='ROWS'
#     ).execute()
#     rownum = discordtag.get('values').index([f'{member}'])
#     # Пример записи в файл
#     values = service.spreadsheets().values().batchUpdate(
#         spreadsheetId=spreadsheet_id,
#         body={
#             "valueInputOption": "USER_ENTERED",
#             "data": [
#                 {"range": f"G{rownum+1}",
#                  "majorDimension": "ROWS",
#                  "values": [["FALSE"]]},
#             ]
#         }
#     ).execute()

bot.run('enter bot token here') #Токен бота
