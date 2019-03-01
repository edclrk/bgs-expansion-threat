import requests


# we expect systems to be unique by name
def get_system(json_systems, name):
    matching_system = [system for system in json_systems if system['name'] == name]
    if matching_system:
        return matching_system[0]
    else:
        return []
    # return matching_system[0]
    # return [system for system in json_systems if system['name'] == name][0]


# r = requests.get('https://api.github.com/events')
r = requests.get(
    'https://www.edsm.net/api-v1/cube-systems?systemName=Negrito&size=30&showInformation=1&showCoordinates=1&showId=1')
print(r.status_code)
# print(r.json())

systems = r.json()

# exioce = get_system(systems, 'Exioce')
# if exioce:
#     print(exioce)
#
# negrito = get_system(systems, 'Negrito')
# if negrito:
#     print(negrito)


for system in systems:
    # print(system)
    # print(system["name"])

    if system['information']:
        # print(system["information"])

        factions_request = requests.get('https://www.edsm.net/api-system-v1/factions?systemName=' + system["name"])
        factions = factions_request.json()
        # print('Factions: ')
        for faction in factions["factions"]:
            # print(faction["name"])
            if faction["influence"] > 0.60:
                # now check if faction is already present is system of concern, if so, skip it

                # now check if system of concern is closest faction with less than 7 factions
                print(system["name"])
                print(faction["name"] + ',  influence: ' + str(faction["influence"]) + ' isPlayer: ' + str(faction["isPlayer"]))
                print()
        # print(factions)
        # print()

    else:
        pass
        # print('No System Information')

print('Done')
