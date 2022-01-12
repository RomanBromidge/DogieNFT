from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # Upload the image to IPFS
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        print(response.json())
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"Image URI: {image_uri}")
        return image_uri


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"There are {number_of_advanced_collectibles} advanced collectibles")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        print(f"Token {token_id} is a {breed}")
        # Make the file name related to the network, id and breed
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template

        # If the file already exists, skip it
        if Path(metadata_file_name).exists():
            print(f"Metadata file {metadata_file_name} already exists")
        else:
            print(f"Creating metadata file {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"{breed} collectible token"

            image_path = f"./img/{breed.lower().replace('_', '-')}.png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)

            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri

            print(f"Metadata: {collectible_metadata}")

            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            if os.getenv("UPLOAD_IPFS") == "true":
                tokenuri = upload_to_ipfs(metadata_file_name)
                print(f"Token URI: {tokenuri}")
