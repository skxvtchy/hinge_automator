# hinge_automator

prompt I used
```
Write one super casual, chill, non-cringey one-liner you could say to someone you just matched with. Keep it short, simple, friendly, and don’t use big words. Don’t mention “vibes.” or weird words dont ever use em dash don't use interjections
```
## Get started

make sure to install the requirements.txt

run this command in one terminal
```
appium --allow-insecure=adb_shell:uiautomator2
```
open a another one and run this
```
python3 hinge.py
```

## How it works
Screenshots then uses the screens shots and takes out the text
input that text into a prompt using gpt and types the text into the field
hinge doesn't allow directly putting text so it puts it onto a clipboard because I guess they don't want people doing this
Name and the lame pickup line saved to csv file

