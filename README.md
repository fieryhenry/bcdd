# Battle Cats Dat Decryptor
The Battle Cats Dat Decryptor (BCDD) is a tool made for decrypting, encrypting and hashing battle cats event data that is stored in the /files directory of the game data. I made this project in less than 2 hours so atm there is limited functionality but in the future I plan to be able to modify the data directly in the tool.

## How To Use
#### Prerequisites
-   [Python](https://www.python.org/downloads/) for running and installing the tool
Run the following commands in command prompt or another terminal to install the tool - If you are not using windows you will need to use `python` or `python3` instead of `py`
#### Installation
```bash
py -m pip install -U bcdd
```
If you get an error saying `No module named pip` then run
```bash
py -m ensurepip --upgrade
```
#### Run
```bash
py -m bcdd
```

### Locating the .dat files
You will need a rooted android device to access the data stored in /data/data.
Then you will need to download and install a root explorer such as [root explorer](https://rootexplorer.co/download/RootExplorer.apk).
Then in root explorer in the `root` tab navigate to `/data/data/jp.co.ponos.battlecats{gv}/files` depending on what game version you are using:
- en: `jp.co.ponos.battlecatsen`
- kr: `jp.co.ponos.battlecatskr`
- tw: `jp.co.ponos.battlecatstw`
- jp: `jp.co.ponos.battlecats`

You need to have run the game and entered the cat base at least once to have the event data available.
The .dat file names are long and correspond to the following data:
- Sale data: `002a4b18244f32d7833fd81bc833b97f.dat` : `event_0`
- Gatya data: `09b1058188348630d98a08e0f731f6bd.dat` : `event_1`
- Daily reward data: `408f66def075926baea9466e70504a3b.dat` : `event_2`
- Ad control data: `523af537946b79c4f8369ed39ba78605.dat` : `ad`

If you're interested the file name is the md5 hash of `event_0`, `ad`, `event_2`, etc

Once you have located the files you need to get access to them on your pc, so copy them to a place that you can access without root (e.g Documents) and connect your device to your pc, or just send them to your self.

### Decrypting Data
Now that you have the files you then need to run the tool (see above in the `Run` section).
Then select what game version you are using.
Then select the option to `Decrypt a .dat file`.
It will then ask you to select a .dat file to decrypt and then it will ask you where you want to save the decrypted file.

### Encrypting Data
Once you have finished editing the decrypted .dat data you then need to select the option to `Encrypt a .dat file`.
It will then ask you to select a .dat file to decrypt and then it will ask you you where you want to save the encrypted file.

After encrypting you then need to get the file back onto your device and then replace the original .dat file in the game folder with the new modified one. Then you can open the game.

### Interpreting event data
In the future I might add support for this directly in the tool but for now you'll need to use a text editor such as notepad++, or notepad if you want. You can then open the decrypted data in the text editor and modify what you want. You can read [this guide](https://www.reddit.com/r/battlecats/wiki/event_data/decoding_guide/) to help you figure out what sutff means.

## Install From Source
If you want the latest features and don't want to wait for a release then you can install the tool from the github directly.
1.  Download [Git](https://git-scm.com/downloads)
2.  Run the following commands: (You may have to replace `py` with `python` or `python3`)

```bash
git clone https://github.com/fieryhenry/bcdd.git
py -m pip install -e bcdd/
py -m bcdd
```

If you want to use the tool again all you need to do is run the `py -m bcdd command

Then if you want the latest changes you only need to run `git pull` in the downloaded `bcdd` folder. (use `cd` to change the folder)