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
    "exe": "./srcds_run",
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


settings = read_settings()

# Parse script arguments
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
args = parser.parse_args()

# If mode is passed as part of command, save new mode to file
if args.mode:
    settings["mode"] = args.mode
    print(f"Mode changed to {args.mode}...")
    write_settings(settings)

# Exit if requested
if args.exit:
    print("Exiting...")
    sys.exit(0)

# Check executable exists
if not os.path.exists(settings.get("exe")):
    print(f"'{settings.get('exe')} not found. Set it correctly in settings.json...")
    sys.exit(1)

# Join together args to form command
exe = settings.get("exe")
default_args = settings.get("default")
mode = settings.get("mode")
unspecified = settings.get("unspecified")
mode_map = settings.get("mode map")

cmd = " ".join([exe, default_args, mode_map.get(mode, unspecified)])

print(f"Mode: '{mode}'")
print(f"Opening '{cmd}'...")
try:
    # Input and input from the process are redirected to python shell
    process = subprocess.run(cmd, stdin=sys.stdin,
                             stdout=sys.stdout, stderr=sys.stdout, shell=True)
# Customise exception behavior below
except subprocess.TimeoutExpired:
    pass
except subprocess.CalledProcessError:
    pass
except subprocess.SubprocessError:
    pass
except KeyboardInterrupt:
    print("Server closed...")
else:
    print(f"Server closed with code {process.returncode}")
    sys.exit(process.returncode)

sys.exit(0)
