import json

json_file = open('p.json')
json_data = json.load(json_file)
json_file.close()

info_file = open(".info", "w")
for key in json_data:
   info_file.write("%s=%s\n" % (key, json_data[key]))

info_file.close()
print(json_data["VERSION_NUMBER"])