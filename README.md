# ZyXEL Keenetic Lite IP address founder

Simple script that helps to find router address, operaitng in Repeater/Extender mode without access to the main router. Searching in 192.168.1.X range.
Theoretically work with any router with HTTP digest authentication.

## Dependencies
* Python 3.7+
* requests
`pip3 install requests`

## Description
`python3 keenetic-ip-finder.py [OPTIONS]`

If login/password entered, script searching for router with matching authentication data. Shows all addresses requiring authentication if not.

## Options
```
-h, --help          Print help text and exit
-a, --address       Use this prefix to change default 192.168.1.X searching address
-l, --login         Router admin login
-p, --password      Router admin password
--fast, -f          Stops the script after first matching address was found
```

## Example
```
python3 keenetic-ip-finder.py -a 192.168.3.1 -l admin -p admin --fast
```