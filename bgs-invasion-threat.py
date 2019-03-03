import requests


# look for a system by name in a list, we expect systems to be unique by name
def get_system(json_systems, name):
    matching_system = [system for system in json_systems if system['name'] == name]

    if matching_system:
        # print('found cached system')
        return matching_system[0]
    else:
        # print('not found')
        return []


def get_faction(json_factions, name):
    # print('get_faction ' + name)
    try:
        matching_faction = [faction for faction in json_factions if faction['name'] == name]
        if matching_faction:
            # print('found cached system_faction')
            return matching_faction[0]
        else:
            # print('not found')
            return []
    except:
        print('Error looking for factions in system ' + name)
        print(json_factions)
        raise Exception("Bad faction")


def add_system_list_to_cache(systems):
    for system in systems:
        # print('Adding to cache: ')
        # print(system)
        systems_cache.append(system)


def add_system_factions_entry_to_cache(system_factions):
    system_factions_cache.append(system_factions)


def add_system_factions_list_to_cache(system_factions):
    for system_faction in system_factions:
        # print('adding faction to cache')
        system_factions_cache.append(system_faction)


# get systems near a given system, add results to cache
def get_local_systems(system_name):
    # cached_system = get_system(systems_cache, system_name)
    # if cached_system:
    #     return cached_system
    # else:
    # using sphere
    r = requests.get(
        'https://www.edsm.net/api-v1/sphere-systems?systemName=' + system_name +
        '&radius=22&showInformation=1&showCoordinates=0&showId=0')

    # using cube
    # r = requests.get(
    #     'https://www.edsm.net/api-v1/cube-systems?systemName=' + system_of_concern +
    #     '&size=21&showInformation=1&showCoordinates=1&showId=1')
    local_systems = r.json()
    add_system_list_to_cache(local_systems)
    return local_systems

def filter_factions_with_influence(faction):
    return faction["influence"] != 0.0

# direct api call, add results to cache
def get_system_factions(system_name):
    # print('get_system_factions: ' + system_name)
    cached_factions = get_faction(system_factions_cache, system_name)
    if cached_factions:
        return cached_factions
    else:
        system_factions_request = requests.get('https://www.edsm.net/api-system-v1/factions?systemName=' + system_name)
        system_factions = system_factions_request.json()

        # # filter factions for ones with non zero influence (old retreated factions may be returned
        system_factions["factions"] = list(filter(filter_factions_with_influence, system_factions["factions"]))
        # print('filtered factions for valid influence...')
        # print(system_factions["factions"])
        # system_factions = filter(filter_factions_with_influence, system_factions)

        add_system_factions_entry_to_cache(system_factions)
        return system_factions


def sort_by_distance(systems):
    # print('sort_by_distance: ' + str(systems["distance"]))
    return systems["distance"]


    # for the current system, go through closest systems until you find a system with less than 7 factions
def system_will_expand_to(faction_name, threat_system, system_of_concern):
    print('checking system_will_expand_to ' + threat_system + ', ' + system_of_concern)
    # local_to_threat_systems = get_local_systems(threat_system)
    local_to_threat_systems = get_local_systems(threat_system)
#     need to sort by distance
    local_to_threat_systems.sort(key=sort_by_distance)
    # print(local_to_threat_systems)

    for local_to_threat_system in local_to_threat_systems:
        print('would expand to ' + local_to_threat_system["name"] + '?')
        # exclude the system we searched by it will always be in the search result at distance 0
        if local_to_threat_system["name"] != threat_system:
            # information is None if not populated
            if local_to_threat_system["information"]:
                factions = get_system_factions(local_to_threat_system["name"])
                if [faction for faction in factions["factions"] if faction['name'] == faction_name]:
                    print('faction already in threat system')
                    pass
                else:
                    if len(factions["factions"]) < 7:

                        #this is the system we expect to expand to
                        print('Detect expansion system is ' + local_to_threat_system["name"])
                        # print(factions)
                        print('Comparing ' + local_to_threat_system["name"] + ' to ' + system_of_concern)

                        return local_to_threat_system["name"].lower() == system_of_concern.lower()
                    else:
                        print('no room, ' + str(len(factions["factions"])) + ' factions')
                        # print(factions["factions"])
            else:
                print('Not populated')
                pass
        else:
            print('same system')
            pass
    return False


system_of_concern = 'negrito'
systems_cache = []
system_factions_cache = []

local_systems = get_local_systems(system_of_concern)
print('Processing ' + str(len(local_systems)) + ' systems')

factions_system_concern = get_system_factions(system_of_concern)["factions"]
print('Factions in System of Concern:')
print(factions_system_concern)
print()

for local_system in local_systems:
    print(local_system["name"] + ': ')
    if local_system['information']:
        factions = get_system_factions(local_system["name"])
        for faction in factions["factions"]:
            if faction["influence"] > 0.60:
                # now check if faction is already present in system of concern, if so, skip it
                if get_faction(factions_system_concern, faction["name"]):
                    print('Ignoring ' + local_system["name"] + ' - ' + faction["name"] + ', already in system of concern')
                    print()
                    continue

                # now check if system of concern is closest to faction with less than 7 factions
                if system_will_expand_to(faction["name"], local_system["name"], system_of_concern):
                    print(local_system["name"])
                    print(faction["name"] + ',  influence: ' + str(faction["influence"]) + ' isPlayer: ' + str(faction["isPlayer"]))
                else:
                    print('Ignoring ' + local_system["name"] + ' - ' + faction["name"] + ', will expand elsewhere')

                print()
        # print("No Faction threat detected")
    else:
        pass
        print('System Not Populated')
    print()

print('Done')
