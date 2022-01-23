import json

with open('data1.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

with open("data.json", "w") as f:
    f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
# print(json.dumps(json_data, indent=4, ensure_ascii=False))