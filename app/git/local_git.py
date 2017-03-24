# -*- coding: utf-8 -*-

import subprocess
import json

def get_json_config():

    f = open('/opt/transformer_deployer/config/build_config.json', 'r')

    json_config = json.loads(str(f.read()))

    f.close()

    return json_config


def get_dir_path():

    f = open('/opt/transformer_deployer/config/build_config.json', 'r')

    dir_path = json.loads(str(f.read()))['path']

    f.close()

    return dir_path


def get_last_version(environment):

    try:

        return get_all_versions(environment)[environment][-1]

    except IndexError:

        return "v0.0.0"


def get_all_versions(environment):
    output = subprocess.check_output(
        'cd ' + get_dir_path() + ' && git tag',
        shell=True
    )

    versions = output.decode("utf-8").split('\n')

    prod_versions = []
    staging_versions = []
    beta_versions = []

    for v in versions:
        if len(v) > 0:
            temp = v.split('-')
            if len(temp) < 2:
                prod_versions.append(v)
            elif temp[-1].split('_')[0] == 'staging':
                staging_versions.append(v)
            elif temp[-1].split('_')[0] == 'beta':
                beta_versions.append(v)

    if environment == "all":
        return {
            "prod": prod_versions,
            "staging": staging_versions,
            "beta": beta_versions
        }
    elif environment == "prod":
        return {
            "prod": prod_versions
        }
    elif environment == "staging":
        return {
            "staging": staging_versions
        }
    elif environment == "beta":
        return {
            "beta": beta_versions
        }
    else:
        return {}


def get_current_version():

    try:

        output = subprocess.check_output(
            'cd ' + get_dir_path() + ' && git describe --tags',
            shell=True
        )

        return output.decode("utf-8").split('\n')[0]

    except subprocess.CalledProcessError:

        return "v0.0.0"


def set_version(tag):

    try:

        subprocess.check_output(
            'cd ' + get_dir_path() + ' && git reset --hard ' + tag,
            shell=True
        )

        return True

    except subprocess.CalledProcessError:

        return False


def update_branch(environment):
    branch = get_json_config()['branch_version'][environment]['branch']

    try:

        subprocess.check_output(
            'cd ' + get_dir_path() + ' && git reset HEAD --hard && git checkout ' + branch + ' && git pull origin ' + branch + ' --tag',
            shell=True
        )

        return True

    except subprocess.CalledProcessError:

        return False


def main():
    print(get_all_versions("all"))


if __name__ == '__main__':
    main()
