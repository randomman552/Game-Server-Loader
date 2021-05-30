#!/usr/bin/env python3
import sys
import subprocess
import argparse
import os
import json

# Settings file path
settings_path = "settings.json"
default_settings = {
    "default": "+maxplayers 32 -console -norestart -usercon",
    "unspecified": "+gamemode sandbox +host_workshop_collection 2036327578 +map gm_genesis",
    "update": "./update.sh",
    "start": "./srcds_run",
    "mode": "sandbox",
    "mode map": {
        "sandbox": "+host_workshop_collection 2035084436 +gamemode sandbox +map gm_genesis",
        "prophunt": "+host_workshop_collection 2036450649 +gamemode prop_hunt +map ph_hotel"
    }
}


def write_settings(settings: dict):
    """
    Function to write settings to file.
    """

    json.dump(settings, open(settings_path, "w"), indent=4)


def read_settings() -> dict:
    """
    Function to get settings from json file.
    File location is defined by settings_path variable
    """

    # If file doesnt exist, generate default one
    if not os.path.exists(settings_path):
        print("Creating default settings.json file...")
        write_settings(default_settings)
        settings = read_settings()
    else:
        settings = json.load(open(settings_path, "r"))
    return settings


# region Parsing arguments
settings = read_settings()

# region Parse arguments
# region Create argparse.ArgumentParser
parser = argparse.ArgumentParser(
    description="Launch a server with specified arguments. By default will check for a file called server.mode which "
                "will contain the mode to launch for."
)
parser.add_argument("mode",
                    default="",
                    help="Desired server mode, changes the mode saved in the settings file executes.",
                    nargs="?"
                    )
parser.add_argument("-e", "--exit",
                    default=False,
                    help="Flag to immediately exit after config changes",
                    action="store_true"
                    )
# endregion
args = parser.parse_args()

# If mode is passed as part of command, save new mode to file
if args.mode:
    settings["mode"] = args.mode
    print(f"Mode changed to {args.mode}...")
    write_settings(settings)
# endregion

# Get required settings
start_cmd = settings.get("start")

# Get optional settings
update_cmd = settings.get("update", "")
default_args = settings.get("default", "")
unspecified = settings.get("unspecified", "")
mode = settings.get("mode", "")
mode_map = settings.get("mode map", dict())

# Exit if start_cmd not provided
if not start_cmd:
    sys.exit(2)

# region Check settings values are valid
if not start_cmd:
    print("Start not specified, please check your settings.")
# endregion

# Join together args to form command
cmd = " ".join([start_cmd, default_args, mode_map.get(mode, unspecified)])
# endregion

# Exit if requested
if args.exit:
    print("Exiting...")
    sys.exit(0)

# region Run update command if specified
if update_cmd:
    print(f"Running update command: {update_cmd}")
    update_process = None
    try:
        update_process = subprocess.run(update_cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stdout, shell=True)
    except subprocess.SubprocessError as e:
        if update_process:
            sys.exit(update_process.returncode)
    except KeyboardInterrupt:
        print("Update cancelled, closing")
        sys.exit(1)
else:
    print("Skipping update...")
# endregion

# region Start server

print(f"Mode: '{mode}'")
print(f"Opening '{cmd}'...")
try:
    process = subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stdout, shell=True)
except subprocess.SubprocessError as e:
    pass
except KeyboardInterrupt:
    print("Server closed...")
else:
    print(f"Server closed with code {process.returncode}")
    print(process.stderr)
    sys.exit(process.returncode)

sys.exit(0)
# endregion
