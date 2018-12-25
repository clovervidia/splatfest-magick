#! /usr/bin/python3
# -*- coding: utf-8 -*-

# clovervidia
import json
import os
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree

import requests

URL_API_BASE = "https://app.splatoon2.nintendo.net{}"
URL_API_SPLATOON2_INK_FEST_DATA = "https://splatoon2.ink/data/festivals.json"

if len(sys.argv) < 3:
    print("Usage: {} <region (NA/EU/JP)> <splatfest ID>".format(sys.argv[0]))
    exit(1)

if sys.argv[1].lower() not in ["na", "eu", "jp"]:
    print("Region must be either NA, EU, or JP.")
    exit(1)

if not (sys.argv[2].isdigit() and len(sys.argv[2]) == 4):
    print("Invalid Splatfest ID.")
    exit(1)

region = sys.argv[1].lower()
fest_id = sys.argv[2]

# On Windows, ImageMagick commands have to be run as arguments to magick.exe due to conflicts with system utility names
if os.name == "nt":
    magick_cmd = "magick "
else:
    magick_cmd = ""

# Make sure ImageMagick is installed and accessible
FNULL = open(os.devnull, "w")
im_test_args = [magick_cmd if magick_cmd else "identify", "--version"]
if subprocess.call(im_test_args, stdout=FNULL, stderr=FNULL) != 0:
    print("ImageMagick can't be started. Please make sure it is installed and in your path variable.")
    exit(1)

# Get the Splatfest data from Splatoon2.ink
festival_data = None
try:
    festival_data = json.loads(requests.get(URL_API_SPLATOON2_INK_FEST_DATA).text)
except requests.exceptions.ConnectionError:
    print("Could not connect to splatoon2.ink.")
    exit(1)

# Find the index for the details for the Splatfest in question
fest_info_index = None
for idx, fest in enumerate(festival_data[region]["festivals"]):
    if str(fest["festival_id"]) == fest_id:
        fest_info_index = idx
        break
else:
    print("Invalid Splatfest ID.")
    exit(1)

# Find the index for the results for the Splatfest in question
fest_results_index = None
for idx, fest in enumerate(festival_data[region]["results"]):
    if str(fest["festival_id"]) == fest_id:
        fest_results_index = idx
        break
else:
    print("Invalid Splatfest ID or that Splatfest's results aren't out yet.")
    exit(1)

# Pre-v4 Splatfests used "solo" and "team" for the result keys, which are now "regular" and "challenge"
if festival_data[region]["results"][fest_results_index]["festival_version"] == 1:
    solo_key = "solo"
    solo_string = "Solo"
    team_key = "team"
    team_string = "Team"
else:
    solo_key = "regular"
    solo_string = "Normal"
    team_key = "challenge"
    team_string = "Pro"

alpha_name = festival_data[region]["festivals"][fest_info_index]["names"]["alpha_short"]
bravo_name = festival_data[region]["festivals"][fest_info_index]["names"]["bravo_short"]
panel_url = URL_API_BASE.format(festival_data[region]["festivals"][fest_info_index]["images"]["panel"])
panel_image = "{} vs. {}.png".format(alpha_name, bravo_name)

alpha_color = festival_data[region]["festivals"][fest_info_index]["colors"]["alpha"]["css_rgb"]
bravo_color = festival_data[region]["festivals"][fest_info_index]["colors"]["bravo"]["css_rgb"]

# The scores are stored as four digit ints even though they have 2 decimal places
alpha_votes = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"]["vote"]["alpha"])
                                / 100)
alpha_solo = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"][solo_key]["alpha"])
                               / 100)
alpha_team = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"][team_key]["alpha"])
                               / 100)
bravo_votes = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"]["vote"]["bravo"])
                                / 100)
bravo_solo = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"][solo_key]["bravo"])
                               / 100)
bravo_team = "{:2.2f}%".format(float(festival_data[region]["results"][fest_results_index]["rates"][team_key]["bravo"])
                               / 100)

# Download the panel image
urllib.request.urlretrieve(panel_url, panel_image)

# Draw the semi-transparent rectangles behind the scores to make them easier to read
subprocess.call('{cmd}convert "{img}" -strokewidth 0 -fill "#0008" -draw "rectangle 0,415,910,534 rectangle '
                '0,323,910,404 rectangle 0,228,910,309 rectangle 0,133,910,214" "{img}"'
                .format(cmd=magick_cmd, img=panel_image), shell=True)


def draw_ink_splats(team, category):
    """
    Sets the color of inksplat.svg to the color of the team that won a category and then draws the ink splat
    behind their score.
    :param team: Either 0/1 or "alpha"/"bravo"
    :param category: Can be "votes", "solo", "regular", "team", or "challenge"
    """
    if team == "alpha":
        team = 0
    elif team == "bravo":
        team = 1

    coords = {
        0: {"vote": "-250-100", "solo": "-250+0", "regular": "-250+0", "team": "-250+100", "challenge": "-250+100"},
        1: {"vote": "+230-100", "solo": "+230+0", "regular": "+230+0", "team": "+230+100", "challenge": "+230+100"}}

    xml.etree.ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    tree = xml.etree.ElementTree.parse("inksplat.svg")
    tree.getroot()[1][0].attrib["style"] = "fill:{}".format(alpha_color if team == 0 else bravo_color)
    tree.write(open("inksplat.svg", "wb"))

    subprocess.call('{cmd}composite -background none -gravity center -geometry 70%x70%{coords} inksplat.svg "{img}" '
                    '"{img}"'.format(cmd=magick_cmd, img=panel_image, coords=coords[team][category]), shell=True)

    tree = xml.etree.ElementTree.parse("inksplat.svg")
    tree.getroot()[1][0].attrib["style"] = "fill:{}".format("0%,0%,0%")
    tree.write(open("inksplat.svg", "wb"))


# Draw the ink splats behind the winning scores
alpha_total = 0
bravo_total = 0
for win in festival_data[region]["results"][fest_results_index]["summary"]:
    if win == "total":
        continue
    if festival_data[region]["results"][fest_results_index]["summary"][win] == 0:
        alpha_total += 1
    else:
        bravo_total += 1
    draw_ink_splats(festival_data[region]["results"][fest_results_index]["summary"][win], win)

# Write the team names on two separate images so they can be centered on their halves of the panel
subprocess.call('{cmd}convert -size 455x450 xc:none -stroke black -strokewidth 8 -gravity north -font Splatoon1.ttf '
                '-pointsize 40 -annotate 0 "{name}" -stroke none -fill white -gravity north -font Splatoon1.ttf '
                '-pointsize 40 -annotate 0 "{name}" miff:- | {cmd}composite -gravity west -geometry +0-20 - "{img}" '
                '"{img}"'.format(cmd=magick_cmd, img=panel_image, name=alpha_name), shell=True)
subprocess.call('{cmd}convert -size 455x450 xc:none -stroke black -strokewidth 8 -gravity north -font Splatoon1.ttf '
                '-pointsize 40 -annotate 0 "{name}" -stroke none -fill white -gravity north -font Splatoon1.ttf '
                '-pointsize 40 -annotate 0 "{name}" miff:- | {cmd}composite -gravity east -geometry +0-20 - "{img}" '
                '"{img}"'.format(cmd=magick_cmd, img=panel_image, name=bravo_name), shell=True)

# Write the score category names
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity north -font Splatoon2.ttf -pointsize 56 '
                '-annotate +0+120 "Votes" -stroke none -fill white -gravity north -font Splatoon2.ttf -pointsize 56 '
                '-annotate +0+120 "Votes" -stroke black -strokewidth 8 -gravity north -font Splatoon2.ttf -pointsize '
                '56 -annotate +0+220 "{solo}" -stroke none -fill white -gravity north -font Splatoon2.ttf -pointsize '
                '56 -annotate +0+220 "{solo}" -stroke black -strokewidth 8 -gravity north -font Splatoon2.ttf '
                '-pointsize 56 -annotate +0+315 "{team}" -stroke none -fill white -gravity north -font Splatoon2.ttf '
                '-pointsize 56 -annotate +0+315 "{team}" -stroke black -strokewidth 8 -gravity north -font '
                'Splatoon1.ttf -pointsize 110 -annotate +0+370 "-" -stroke none -fill white -gravity north -font '
                'Splatoon1.ttf -pointsize 110 -annotate +0+370 "-" "{img}"'.
                format(cmd=magick_cmd, img=panel_image, solo=solo_string, team=team_string), shell=True)

# Write the team scores for each category
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate -250-100 "{a_votes}" -stroke none -fill white -gravity center -font Splatoon2.ttf '
                '-pointsize 40 -annotate -250-100 "{a_votes}" "{img}"'.format(cmd=magick_cmd, img=panel_image,
                                                                              a_votes=alpha_votes), shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate +230-100 "{b_votes}" -stroke none -fill white -gravity center -font Splatoon2.ttf '
                '-pointsize 40 -annotate +230-100 "{b_votes}" "{img}"'.format(cmd=magick_cmd, img=panel_image,
                                                                              b_votes=bravo_votes), shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate -250+0 "{a_solo}" -stroke none -fill white -gravity center -font Splatoon2.ttf -pointsize '
                '40 -annotate -250+0 "{a_solo}" "{img}"'.format(cmd=magick_cmd, img=panel_image, a_solo=alpha_solo),
                shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate +230+0 "{b_solo}" -stroke none -fill white -gravity center -font Splatoon2.ttf -pointsize '
                '40 -annotate +230+0 "{b_solo}" "{img}"'.format(cmd=magick_cmd, img=panel_image, b_solo=bravo_solo),
                shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate -250+100 "{a_team}" -stroke none -fill white -gravity center -font Splatoon2.ttf -pointsize '
                '40 -annotate -250+100 "{a_team}" "{img}"'.format(cmd=magick_cmd, img=panel_image, a_team=alpha_team),
                shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity center -font Splatoon2.ttf -pointsize 40 '
                '-annotate +230+100 "{b_team}" -stroke none -fill white -gravity center -font Splatoon2.ttf -pointsize '
                '40 -annotate +230+100 "{b_team}" "{img}"'.format(cmd=magick_cmd, img=panel_image, b_team=bravo_team),
                shell=True)

# Write the total scores
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity north -font Splatoon1.ttf -pointsize 110 '
                '-annotate -80+370 "{a_total}" -stroke none -fill white -gravity north -font Splatoon1.ttf -pointsize '
                '110 -annotate -80+370 "{a_total}" "{img}"'.format(cmd=magick_cmd, img=panel_image,
                                                                   a_total=alpha_total), shell=True)
subprocess.call('{cmd}convert "{img}" -stroke black -strokewidth 8 -gravity north -font Splatoon1.ttf -pointsize 110 '
                '-annotate +80+370 "{b_total}" -stroke none -fill white -gravity north -font Splatoon1.ttf -pointsize '
                '110 -annotate +80+370 "{b_total}" "{img}"'.format(cmd=magick_cmd, img=panel_image,
                                                                   b_total=bravo_total), shell=True)

# The image is done!
print("All done, check out '{}' for the finished product.".format(panel_image))
