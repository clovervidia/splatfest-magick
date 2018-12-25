# splatfest-magick

Generates Splatfest result images that look like the results shown in-game with ImageMagick and Python.

Uses Splatoon2.ink's API for Splatfest results.

Here is what the generated result images look like: ![Sample generated Splatfest result image](https://i.imgur.com/iBokji8.png)

## Setup

Make sure you have `requests` installed, as it is used to access Splatoon2.ink's API.

```bash
pip install -r requirements
```

You also need to have ImageMagick installed and in your path.

To check if it's set up correctly, on Windows, enter this at a command prompt:

```cmd
magick --version
```

Or for Linux/OS X:

```bash
identify --version
```

If the command returns a message with ImageMagick's version information, the script should be able to interact with 
ImageMagick.

You will also need to provide the Splatoon 1 and 2 fonts in TTF form. If you have access to SplatNet from your 
computer, you will be able to get them easily.

Once you have them, name them `Splatoon1.ttf` and `Splatoon2.ttf` and place them in the repo folder.

## Usage

Just pass in the region and the Splatfest ID to generate the results image for. Scroll down for a list of Splatfest IDs.

```bash
./magick.py NA 4054
```

When it's done, a message will be printed with the image's filename:

```bash
All done, check out 'Hero vs. Villain.png' for the finished product.
```

## IDs

Here is a list of Splatfest IDs so far:

### NA

|ID|Alpha|Bravo|
|---:|---:|:---|
|2050|Mayo|Ketchup|
|5051|Flight|Invisibility|
|2051|Vampires|Werewolves|
|2052|Sci-Fi|Fantasy|
|2053|Sweater|Sock|
|4051|Action|Comedy|
|2054|Money|Love|
|5052|Chicken|Egg|
|2055|Baseball|Soccer|
|5053|Raph|Leo|
|5054|Mikey|Donnie|
|5056|Raph|Donnie |
|5059|Pulp|No Pulp|
|4052|Squid|Octopus|
|2056|Fork|Spoon|
|5060|Retro|Modern|
|4053|Trick|Treat|
|2057|Salsa|Guac|
|4054|Heroes|Villains|
|4055|Family|Friends|

### JP

|ID|Alpha|Bravo|
|---:|---:|:---|
|1051|Mayo|Ketchup|
|1052|Fries|McNuggets|
|1054|Agility|Endurance|
|1055|With Lemon|Without Lemon|
|1056|Warm Inner Wear|Warm Outer Wear|
|4051|Action|Comedy|
|1057|Champion|Challenger|
|1058|Flower|Dumpling|
|1059|Latest Model|Popular Model|
|1060|Unknown Creature|Advanced Technology|
|1061|Hello Kitty|Cinnamoroll|
|1062|My Melody|Pompompurin |
|1063|Hello Kitty|My Melody|
|4052|Squid|Octopus|
|1065|Mushroom Mountain|Bamboo Shoot Village|
|1066|Tsubuan|Koshian|
|4053|Trick|Treat|
|1067|Pocky Chocolate|Pocky: Gokuboso|
|4054|Heroes|Villains|
|4055|Family|Friends|

### EU

|ID|Alpha|Bravo|
|---:|---:|:---|
|3050|Mayo|Ketchup|
|5051|Flight|Invisibility|
|3051|Front|Back|
|3052|Cold Breakfast|Warm Breakfast|
|3053|Film|Book|
|4051|Action|Comedy|
|3054|Gherk-IN|Gherk-OUT|
|5052|Chicken|Egg|
|3055|Salty|Sweet|
|5053|Raph|Leo|
|5054|Mikey|Donnie|
|5056|Raph|Donnie|
|5059|Pulp|No Pulp|
|4052|Squid|Octopus|
|3056|Adventure|Relax|
|5060|Retro|Modern|
|4053|Trick|Treat|
|3057|Eat It|Save It|
|4054|Heroes|Villains|
|4055|Family|Friends|
