import json

# Sorts the keys of a dictionary alphabeticly.
def sort_keys_only(obj):
    if isinstance(obj, dict):
        return {key: sort_keys_only(value) for key, value in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_keys_only(item) for item in obj]
    else:
        return obj

# Applies those sorted keys to an actual json file.
def sort_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    sorted_data = sort_keys_only(data)

    with open(file_path, 'w') as file:
        json.dump(sorted_data, file, indent=2, ensure_ascii=False)