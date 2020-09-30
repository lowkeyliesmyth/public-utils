#!/usr/bin/env python3
"""
This script will decompose local or remote concatenated YAML files into separate local files.
Usage:
./main.py --remote https://raw.githubusercontent.com/metallb/metallb/v0.9.3/manifests/metallb.yaml --output ~/Desktop/metallb/base
./main.py --name metallb --file metallb.yaml --output ~/Desktop/metallb/base
"""

import os
import argparse
import re
import urllib.parse
import urllib.request
import yaml
import subprocess


def yaml_url_regex_type(url_arg):
    """
    :param url_arg: string, full url path to remote yaml file
    :return: return original string after verifying it matches regex
    """

    pat = re.compile(r"https?:\/\/.*\.yaml$")
    #subprocess.run()
    if not pat.match(url_arg):
        raise argparse.ArgumentTypeError
    return url_arg


def read_input_file(input_file):
    """
    :param input_file: string, path to valid yaml file
    :return: list of dicts, each dict a valid subset of input yaml file
    """

    print(f"Reading input file: {input_file}")
    with open(os.path.expanduser(input_file), "r") as stream:
        try:
            return [doc for doc in yaml.safe_load_all(stream)]
        except yaml.YAMLError as e:
            print(e)


def read_remote_url_file(remote_url):
    """
    :param remote_url: string, url containing remote yaml file
    :return: list of dicts, each dict a valid subset of remote yaml file
    """

    remote_url_path = urllib.parse.urlparse(remote_url)
    remote_filename = remote_url_path[2].split("/")[-1]
    print(f"Retrieving url: {remote_url}")
    print(f"Reading remote file: {remote_filename}")

    # TODO: verify HTTPResponse is `Content-Type: text/plain;` otherwise err
    resp = urllib.request.urlopen(remote_url)
    decoded_data = resp.read().decode("utf-8")
    try:
        # TODO: maintain block scalar formatting
        return [doc for doc in yaml.safe_load_all(decoded_data)]
    except yaml.YAMLError as e:
        print(e)


def write_yaml(output_dir, yamldoc_list, project_name):
    """
    :param output_dir: string, path to write files to
    :param yamldoc_list: list of dicts containing yaml content
    :param project_name: string, name of k8s app project
    :return: files containing content of yamldoc_list
    """

    project_name = project_name.lower()
    outdir_path = os.path.expanduser(output_dir)
    if not os.path.exists(outdir_path):
        os.makedirs(outdir_path)

    for doc in yamldoc_list:
        # sometimes bundles have blank docs. Skip them
        if doc is None:
            continue
        k8s_object_name = doc["metadata"]["name"].lower()
        k8s_object_kind = doc["kind"].lower()

        # TODO: manage filename collisions by appending `-$INT` to filename
        yaml_filename = (
            f"{outdir_path}/{project_name}{k8s_object_name}-{k8s_object_kind}.yaml"
        )
        print(yaml_filename)
        with open(yaml_filename, "w") as outfile:
            yaml.dump(doc, outfile)


def main():
    parser = argparse.ArgumentParser()
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-r",
        "--remote",
        dest="remote_url",
        help="Remote URL to concatenated YAML manifest",
        type=yaml_url_regex_type,
    )
    input_group.add_argument(
        "-f",
        "--file",
        dest="input_file",
        help="Path to local YAML manifest input",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        help="Directory to output files. Default is pwd",
        type=str,
        default=os.getcwd(),
        required=False,
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="project_name",
        help="Name of this project",
        type=str,
        required=False,
    )
    args = parser.parse_args()
    output_dir = args.output_dir

    if args.project_name is not None:
        project_name = f"{args.project_name}-"
    else:
        project_name = ''

    if args.input_file is not None:
        input_file = args.input_file.name
        yamldoc_list = read_input_file(input_file)
    else:
        remote_url = args.remote_url
        yamldoc_list = read_remote_url_file(remote_url)

    write_yaml(output_dir, yamldoc_list, project_name)


if __name__ == "__main__":
    main()
