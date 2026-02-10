import json
import zlib
import base64

level = [
["bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd"],
["bd","ts","__","__","ts","__","__","__","__","ts","__","__","ts","bd"],
["bd","__","__","__","__","__","__","__","__","__","__","__","__","bd"],
["bd","__","br","br","__","br","br","br","br","__","br","br","__","bd"],
["bd","__","br","br","__","br","br","br","br","__","br","br","__","bd"],
["bd","__","br","br","__","br","br","br","br","__","br","br","__","bd"],
["bd","__","br","br","__","__","__","__","__","__","br","br","__","bd"],
["bd","__","br","br","__","st","br","br","st","__","br","br","__","bd"],
["bd","__","__","__","__","br","st","st","br","__","__","__","__","bd"],
["bd","br","__","st","__","br","st","st","br","__","st","__","br","bd"],
["bd","__","__","st","__","br","br","br","br","__","st","__","__","bd"],
["bd","__","__","__","__","__","__","__","__","__","__","__","__","bd"],
["bd","__","__","br","br","br","bs","__","br","br","br","__","__","bd"],
["bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd","bd"]
]

def level_to_seed(level):
    text = json.dumps(level, separators=(",", ":"))
    compressed = zlib.compress(text.encode())
    seed = base64.urlsafe_b64encode(compressed).decode()
    return seed

def seed_to_level(seed):
    compressed = base64.urlsafe_b64decode(seed.encode())
    text = zlib.decompress(compressed).decode()
    return json.loads(text)

if __name__ == "__main__":
    seed = level_to_seed(level)
    print("Seed:", seed)
    