import requests

#api_key = [API]
#steam_id = [ID]

#API'en skal vare i 14 dager, men hvis den ikke fungerer så send melding.

# Denne her API'en henter generell info om brukeren, og dette bruker jeg til å få tak i Display navnet på steam brukeren. 
varUrl_player = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=[API]&steamids=[ID]' #Dette her er api lenken som inneholder basic info om brukeren. 
varResponse_player = requests.get(varUrl_player) #Sender en GET request fra request modulen jeg importerte. Så lagrer det infoen fra APIen i response_player variablen.
varData_player = varResponse_player.json() #Denne gjør at json filen man fikk ifra apien blir gjort om til et python objekt, også kaller den den for data_player.
varSteam_name = varData_player.get('response', {}).get('players', [{}])[0].get('personaname') #Denne koden henter "personame" informasjonen som ligger inne i APIen.
varSteam_pfp = varData_player.get('response', {}).get('players', [{}])[0].get('avatarfull') #Denne koden gjør det samme som den over, men den henter avatar linken.
varSteam_status = varData_player.get('response', {}).get('players', [{}])[0].get('personastate') #Henter ut spiller status (online/ offline).
varSteam_url = varData_player.get('response', {}).get('players', [{}])[0].get('profileurl') #Henter lenken til steam brukeren.
#Kodene nedover har ganske lik kode, men de er justert sånn at den får anderledes informasjon. Det var flere Steam APIer som inneholdt forskjellig informasjon, 
#så jeg måtte ha flere url'er basert på hva jeg ville ha. Derfor så måtte jeg ha flere koder som henter forskjellige informasjoner som navn, antall spill, og steam level.

#Siden kodene er bygd opp likt og bare har andre variabler + navn så kommer jeg ikke til å forklare for hver av de. 

# Dette er API'en som gir levelet til brukeren.
varUrl_level = f'http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=[API]&steamid=[ID]'
varResponse_level = requests.get(varUrl_level)
varData_level = varResponse_level.json()
varSteam_level = varData_level.get('response', {}).get('player_level', 0)

#API'en her henter info om spillene til brukeren, også bruker jeg include_appinfo for å få navn på spillene. 
varUrl_game = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=[API]&steamid=[ID]&include_appinfo=1&format=json'
varResponse_game = requests.get(varUrl_game)
varData_game = varResponse_game.json()
varNum_games = varData_game.get('response', {}).get('game_count', 0)

# Dette her er app idene til de forskjellige spillene, app id'en ligger inne på spillene når man åpner de på steam sin nettside. 
varApp_ids = ['1144200', '108600', '107410', '393380']
varGame_hours = {}

# Denne her koden tar spill dataen ifra API'en og finner hvor lenge spillet er spillt med 'playtime_forever'.
for game in varData_game.get('response', {}).get('games', []):
    if str(game['appid']) in varApp_ids:
        varGame_hours[game['name']] = round(game['playtime_forever'] / 60, 2)  # Denne koden her runder opp koden til 2 desimaler og gjør det til timer. 

# Denne koden her gjør sånn spillene blir sortert ifra hvem som har høyest antall timer spillt. Ikke nøvendig men gjør at det ser finere ut. 
varSorted_game_hours = dict(sorted(varGame_hours.items(), key=lambda item: item[1], reverse=True))


# Enkelt fortkart så lager denne koden en katalog som gjør at de forskjellige statusene blir endret fra tall til ord sånn at det er lettere og lese. 
# Det vil si at 0=Offline, så da står det når man printer ut Offline istedet for 0.
varStatus_dict = {
    0: 'Offline',
    1: 'Online',
    2: 'Busy',
    3: 'Away',
    4: 'Snooze',
    5: 'Looking to trade',
    6: 'Looking to play'
}

#Det denne koden her gjør er at den omdefinerer varSteam_Status sånn at katologen blir med i variabelen. 
varSteam_status = varStatus_dict.get(varSteam_status, 'Ukjent')


# Denne koden her printer ut navn, level, antall spill.
print('Viser informasjon om Anders Opøiens Steam bruker:\n')
print(f'Brukernavn: {varSteam_name}')
print(f'Antall spill: {varNum_games}')
print(f'Steam level: {varSteam_level}') 

print(f'Status: {varSteam_status}\n') #Bruker newline for å få seperasjon mellom informasjonen, da er det litt enklere å lese. 

print(f'Profil URL: {varSteam_url}')
print(f'Profil bilde: {varSteam_pfp}\n')

print('Antall timer spillt:')
for game_name, hours in varSorted_game_hours.items():
    print(f'{game_name}: {hours} timer') #Printer ut antall timer på spillene. 