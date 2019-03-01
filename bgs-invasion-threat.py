import requests


# we expect systems to be unique by name
def get_system(json_systems, name):
    matching_system = [system for system in json_systems if system['name'] == name]
    if matching_system:
        return matching_system[0]
    else:
        return []


def get_faction(json_factions, name):
    matching_faction = [faction for faction in json_factions if faction['name'] == name]
    if matching_faction:
        return matching_faction[0]
    else:
        return []


def add_system_list_to_cache(systems):
    for system in systems:
        systems_cache.append(system)


def get_local_systems(system_name):
    cached_system = get_system(systems_cache, system_name)
    if cached_system:
        return cached_system
    else:
        r = requests.get(
            'https://www.edsm.net/api-v1/cube-systems?systemName=' + system_of_concern +
            '&size=30&showInformation=1&showCoordinates=1&showId=1')
        local_systems = r.json()
        add_system_list_to_cache(local_systems)
        return local_systems


system_of_concern = 'Negrito'
systems_cache = []

local_systems = get_local_systems(system_of_concern)
print('Processing ' + str(len(local_systems)) + ' systems')

factions_system_concern_request = requests.get('https://www.edsm.net/api-system-v1/factions?systemName=' + system_of_concern)
factions_system_concern = factions_system_concern_request.json()["factions"]
print('Factions in System of Concern:')
print(factions_system_concern)

for system in local_systems:
    if system['information']:
        # print(system["information"])

        factions_request = requests.get('https://www.edsm.net/api-system-v1/factions?systemName=' + system["name"])
        factions = factions_request.json()
        # print('Factions: ')
        for faction in factions["factions"]:
            # print(faction["name"])
            if faction["influence"] > 0.60:
                # now check if faction is already present is system of concern, if so, skip it
                if get_faction(factions_system_concern, faction["name"]):
                    print('Ignoring ' + system["name"] + ' - ' + faction["name"] + ', already in system of concern')
                    print()
                    continue


                # now check if system of concern is closest to faction with less than 7 factions
                print(system["name"])
                print(faction["name"] + ',  influence: ' + str(faction["influence"]) + ' isPlayer: ' + str(faction["isPlayer"]))
                print()
        # print(factions)
        # print()

    else:
        pass
        # print('No System Information')

print('Done')
