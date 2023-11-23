#!/usr/bin/env python3
from pyhocon import ConfigFactory, HOCONConverter
from jycm.jycm import YouchamaJsonDiffer
import json
from colorama import Fore
import sys


def parse_configs(config_path):
    config = ConfigFactory.parse_file(config_path)
    json_config = HOCONConverter().to_json(config=config)
    return json_config


def compare(left, right):
    config1 = json.loads(parse_configs(left))
    config2 = json.loads(parse_configs(right))

    ycm = YouchamaJsonDiffer(config1, config2)
    diff_result = ycm.get_diff()

    if 'dict:add' not in diff_result:
        diff_result['dict:add'] = {}
    if 'dict:remove' not in diff_result:
        diff_result['dict:remove'] = {}
    if 'value_changes' not in diff_result:
        diff_result['value_changes'] = {}

    for diff in diff_result["dict:add"]:
        print(Fore.GREEN + left + ": NOT PRESENT")
        print(Fore.RED + right + ": " + diff["right_path"] + "=" + str(diff["right"]))
        print()

    for diff in diff_result["dict:remove"]:
        print(Fore.GREEN + left + ": " + diff["left_path"] + "=" + str(diff["left"]))
        print(Fore.RED + right + ": NOT PRESENT")
        print()

    for diff in diff_result["value_changes"]:
        print(Fore.GREEN + left + ": " + diff["left_path"] + "=" + str(diff["left"]))
        print(Fore.RED + right + ": " + diff["right_path"] + "=" + str(diff["right"]))
        print()


if __name__ == '__main__':
    compare(sys.argv[1], sys.argv[2])
