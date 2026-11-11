# CDDA-Mod-easiest-containers
python mod script for cataclysm: dark days ahead, allowing you to remove the weight and length restrictions of containers

you will need to run the script to actually change anything!

1. idk how other people do it but make sure this mod is in the outermost mod folder, not the one inside /data/
2. copy your worlds 'mods.json' into the mod folder
3. run the python script
4. delete the mods.json file in the mod folder
5. success!

few other notes:
1. it doesn't get every item. In my minimal testing I found a few hide bags that weren't changed there's sure to be more. You can look into it if you want, it's probably something to do with me being forced to skip anything with a 'snippet_category'. I made this mod on a whim and don't actually use it so bug fixing it not really a priority, sorry.
2. I was too lazy to be careful with mod order. The order it assimilates items is outer mod folder, inner mod folder, base cdda folder. If multiple mods override the same item it'll only pick the first it comes across and skip the rest.
3. This mod should transcend updates? unless they change how the json is formatted it should just work...
4. even if you're running vanilla you still have to copy over the mods.json when initializing.
5. idk, make sure you have the mod added to the world and have fun!
