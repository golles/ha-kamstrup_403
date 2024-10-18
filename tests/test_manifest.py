"""Test for versions."""

import json

from custom_components.kamstrup_403.const import DOMAIN, NAME, VERSION


async def test_manifest():
    """Verify that the manifest and const.py values are equal"""
    with open(
        file="custom_components/kamstrup_403/manifest.json", mode="r", encoding="UTF-8"
    ) as manifest_file:
        data = manifest_file.read()

    manifest: dict = json.loads(data)

    assert manifest.get("domain") == DOMAIN
    assert manifest.get("name") == NAME
    assert manifest.get("version") == VERSION

    with open(file="requirements.txt", mode="r", encoding="UTF-8") as file:
        lines = [line.rstrip("\n") for line in file]

        for requirement in manifest["requirements"]:
            assert requirement in lines
