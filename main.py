import requests
from apikey import API_KEY

def get_contributions(clan_tag="#QUR0LJVY", donation_ratio=0.3, fame_ratio=0.7):
    encoded_tag = clan_tag.replace("#", "%23")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    donation_data = {}
    fame_data = {}

    donation_url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/members"
    try:
        response = requests.get(donation_url, headers=headers)
        response.raise_for_status()
        members = response.json().get("items", [])
        for member in members:
            name = member.get("name")
            donations = member.get("donations", 0)
            donation_data[name] = donations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching donations: {e}")

    # Fetch fame info from the current clan war (river race) endpoint
    war_url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/currentriverrace"
    try:
        response = requests.get(war_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        clan_info = data.get("clan", {})
        participants = clan_info.get("participants", [])
        for participant in participants:
            name = participant.get("name")
            fame = participant.get("fame", 0)
            fame_data[name] = fame
    except requests.exceptions.RequestException as e:
        print(f"Error fetching war info: {e}")

    all_names = set(donation_data.keys()).union(fame_data.keys())
    contributions = []
    for name in all_names:
        donation = donation_data.get(name, 0)
        fame = fame_data.get(name, 0)
        contribution = donation_ratio * donation + fame_ratio * fame
        contributions.append({name: [contribution, donation, fame]})
    contributions.sort(key=lambda d: list(d.values())[0], reverse=True)
    return contributions


if __name__ == "__main__":
    results = get_contributions()
    for r in results:
        for name,C in r.items():
            print(f"{name}: {C[0]} || donation: {C[1]} fame: {C[2]}")
    with open("contribution.txt", "w", encoding="utf-8") as file:
        for r in results:
            for name, C in r.items():
                file.write(f"{name}: {C[0]} || donation: {C[1]} fame: {C[2]}\n")