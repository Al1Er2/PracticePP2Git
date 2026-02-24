import json

# Открываем JSON файл
with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':60} {'Description':15} {'Speed':10} {'MTU'}")
print("-" * 80)

# Проходим по элементам JSON
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    
    print(f"{dn:60} {descr:15} {speed:10} {mtu}")
