# Game Server Loader
A python script used to start video game servers with multiple preconfigured states.\
The run arguments for these configured states are stored in the settings.json file.

## Generating settings.json
The settings.json file can be created using the following command (this will not overwrite an existing file)
```shell
python3 srv.py -e
```

## Editing Settings
The default contents of the settings file is as follows:
```json
{
    "default": "+maxplayers 32 -console -norestart -usercon",
    "unspecified": "+gamemode sandbox +host_workshop_collection 2036327578 +map gm_genesis",
    "exe": "./srcds_run",
    "mode": "sandbox",
    "mode map": {
        "sandbox": "+host_workshop_collection 2035084436 +gamemode sandbox +map gm_genesis",
        "prophunt": "+host_workshop_collection 2036450649 +gamemode prop_hunt +map ph_hotel"
    }
}
```

### Explanations
* `default` - Arguments that are provided regardless of which mode is selected.
* `unspecified` - Arguments that are provided if no match is found in the `mode map`.
* `exe` - The executable to run.
* `mode` - The mode to run of none is provided.
* `mode map` - A map between modes and the arguments to provide when that mode is specified as the mode of the server.
    * If a match for `mode` is not found in this, the program will be run with the unspecified args

## Running
The server can be run with the mode stored in the settings.json file with the following command:
```shell
python srv.py
```

A server can be launched in a specified mode via the following:
```shell
python srv.py sandbox
```

### Examples
The default config generated is one I use for a [Garry's Mod](https://store.steampowered.com/app/4000/garrys_mod) server.\
Using this default config, and running the following command:
```shell
./srv.py sandbox
```
* The mode value in settings.json would be changed to sandbox.
* The server would be launched by the script with the following arguments:
```shell
./srcds_run +maxplayers 32 -console -norestart -usercon +host_workshop_collection 2035084436 +gamemode sandbox +map gm_genesis
```
