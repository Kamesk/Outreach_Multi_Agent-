import yaml

def load(path):
    with open(path) as f: data=yaml.safe_load(f)
    return data["generate_post"]["system"],data["generate_post"]["user"],data["generate_image"]["prompt"]
