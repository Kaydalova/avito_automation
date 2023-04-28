import yaml

with open("token.yml") as file:
    token = yaml.safe_load(file)["token"]
