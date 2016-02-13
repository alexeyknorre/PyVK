# PyVK

Script for downloading and parsing public userdata from VK.com.
Make sure you have created your own application ID and access token before usage.
Alexey Knorre, 13.02.2016
V.2
## Features

- cooldown for API access, profiles are queried in chunks
- dicts inside lists are unzipped in flat mode
## External dependencies
vkontakte (installing in cmd: "pip install vkontakte". Make sure
you are using Anaconda Python distribution, otherwise pip may not be working.)

## TODO
- replace aliases in fields (f.e., 1 for Moscow or 2 for SPb in field "city")
by collecting such aliases and then quering VK API for their meaning (see 
VK API docs for exact query)
- test cases (not sure if there are gaps in results due to complicated dicts unzipping)
