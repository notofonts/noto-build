# -*- coding: utf-8 -*-
# Copyright 2020 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import sys
import urllib.parse
import urllib.request
import requests
import copy
import re
# import fontmake

from pathlib import Path
from defcon import Font
from fontTools import ttLib
from fontTools.subset import Subsetter
from fontTools.subset import Options
from fontTools import merge
from argparse import ArgumentParser
from third_party.scalefonts import scale_font


class Download:
    def __init__(self, repo_names, scriptsFolder, hinted):
        self.repoNames = repo_names
        self.scriptsFolder = scriptsFolder
        self.hinted = hinted
        print("dl begin")
        self.dwnldSources()

    def dwnldSources(self):
        for i in self.repoNames:
            if self.hinted is False:
                url = (
                    "https://api.github.com/repos/notofonts/"
                    + i
                    + "/tree/master/fonts/ttf/unhinted/instance_ttf"
                    )
            else:
                url = (
                    "https://api.github.com/repos/notofonts/"
                    + i
                    + "/tree/master/fonts/ttf/hinted/instance_ttf"
                    )
            api_url, dl_folder = self.createUrl(url)
            dest = self.getFilepathFromUrl(url, self.scriptsFolder)
            dest = os.path.join(os.path.dirname(dest), i, "instance_ttf")
            if not os.path.exists(dest):
                os.makedirs(dest)
            total_files = 0
            print(api_url)
            response = urllib.request.urlretrieve(api_url)
            with open(response[0], "r") as f:
                data_brutes = f.read()
                data = json.loads(data_brutes)
                total_files += len(data)
                for index, file in enumerate(data):
                    file_url = file["download_url"]
                    file_name = file["name"]
                    temp_path = os.path.join(dest, file_url.split("/")[-1]).replace(
                        "%20", " "
                    )
                    if file_url is not None:
                        with requests.get(file_url) as response:
                            binary = response.content
                            self.writeBin(temp_path, binary)

    def writeBin(self, path, binary):
        with open(path, "wb") as f:
            f.write(binary)

    def createUrl(self, url):
        branch = re.findall(r"/tree/(.*?)/", url)
        print(branch)
        api_url = url.replace("https://github.com", "https://api.github.com/repos")
        if len(branch) == 0:
            branch = re.findall(r"/blob/(.*?)/", url)[0]
            download_dirs = re.findall(r"/blob/" + branch + r"/(.*)", url)[0]
            api_url = re.sub(r"/blob/.*?/", "/contents/", api_url)
        else:
            branch = branch[0]
            download_dirs = re.findall(r"/tree/" + branch + r"/(.*)", url)[0]
            api_url = re.sub(r"/tree/.*?/", "/contents/", api_url)

        api_url = api_url + "?ref=" + branch
        return api_url, download_dirs

    def getFilepathFromUrl(self, url, dirpath):
        url_path_list = urllib.parse.urlsplit(url)
        abs_filepath = url_path_list.path
        basepath = os.path.split(abs_filepath)[-1].split("-")[0]

        return os.path.join(dirpath, basepath)


class GlyphsToRemove:

    def add(self, unicodez:list, scriptname):
        for x in unicodez:
            setattr(self, str(x), scriptname)

    def getListFor(self, scriptname):
        return [x for x in vars(self) if getattr(self, x) == scriptname]

    def getScript(self):
        return set([getattr(self, x) for x in vars(self)])

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)

class Prompt:
    def __init__(self):
        self.GlyphsToRemove = GlyphsToRemove()

    def askfor(self, unicodez:list, script1:str, script2:str):
        request = input(">>> ")
        if request == "1":
            self.GlyphsToRemove.add(unicodez, script2)
        else:
            self.GlyphsToRemove.add(unicodez, script1)

    def addGlyphToRemove(self, unicodez, scriptname):
        self.GlyphsToRemove.add(unicodez, scriptname)

    def getGlyphsToRemove(self, scriptname):
        return self.GlyphsToRemove.getListFor(scriptname)

    def getScriptsToSubset(self):
        return self.GlyphsToRemove.getScript()


class Notobuilder:

    """ docstring
    """

    def __init__(
            self,
            newName,
            output,
            writingsystems,
            contrast,
            styles,
            subsets,
            swapedstyles,
            weight,
            width,
            hinted,
            ui
        ):
        self.scriptsFolder = os.path.split(sys.argv[0])[0]
        self.writingSystems = writingsystems
        self.newName = " ".join(newName)
        self.output = ["ttf"]  # OTF and VF merging not available at this point
        self.subsets = subsets
        self.swapedstyles = swapedstyles
        self.contrast = str(contrast[0])
        self.styles = styles
        self.fonts2subset = list()
        self.weight = weight
        self.width = width
        self.default = []
        self.toKeep = dict()
        self.hinted = hinted
        self.uniGlyphsAlreadySorted = list()
        self.path = "instance_ttf"
        self.ui = ui
        self.duplicatesAreResolved = False
        # self.unhintedfontpath = "fonts/ttf/unhinted/instance_ttf"
        # self.hintedfontpath = "fonts/ttf/hinted/instance_ttf"
        self.lgcfonts = [
            "NotoSans",
            "NotoSerif",
            "NotoSans-Italic",
            "NotoSerif",
            "NotoSansDisplay",
            "NotoSerifDisplay",
            "NotoSansDisplay-Italic",
            "NotoSerifDisplay",
        ]
        self.latn_subset = ["ASCII", "LatinPro", "IPA", "Vietnamese", "Ponctuation"]
        self.cyr__subset = ["Russian", "CyrPro"]
        self.grk__subset = ["Modern", "Polytonic"]

        self.repo_naming_translation = {
            "NotoSansKufi": "NotoKufiArabic",
            "NotoSansMusic": "NotoMusic",
            "NotoSerifMusic": "NotoMusic",
            "NotoSerifNaskh": "NotoNaskhArabic",
            "NotoSerifNaskhUI": "NotoNaskhArabicUI",
            "NotoSerifUrdu": "NotoNastaliqUrdu",
            "NotoSerifHebrew": "NotoRashiHebrew",
            "NotoSerifNushu": "NotoTraditionalNushu",
            "NotoSerifTamil-Italic": "NotoSerifTamil-Slanted",
            "NotoSansTamil-Italic": "NotoSansTamil",  # Does not exists, but Serif "Italic" (slanted) does.
            "NotoSansNaskh": "NotoSansArabic",
        }
        self.fonts_with_ui_version = [
            "NotoSansKannada",
            "NotoSansArabic",
            "NotoSansDevanagari",
            "NotoSansLao",
            "NotoNaskhArabic"
            # "NotoSansBengali",
            # "NotoSansGujarati",
            # "NotoSansGurmukhi",
            # "NotoSansKannada",
            # "NotoSansKhmer",
            # "NotoSansLao",
            # "NotoSansMalayalam",
            # "NotoSansMyanmar",
            # "NotoSansOriya",
            # "NotoSansSinhala",
            # "NotoSansTamil",
            # "NotoSansTelugu",
            # "NotoSansThai",
        ]

        self.buildRepoName()

    @property
    def opticalSize(self):
        self._opticalSize = ""
        if "Display" in self.styles:
            self._opticalSize = "Display"
        return self._opticalSize

    @property
    def italic(self):
        self._slant = ""
        if "Italic" in self.styles:
            self._slant = "-Italic"
        return self._slant

    @property
    def arabicStyle(self):
        self._arabicStyle = "Naskh"
        if "Kufi" in self.styles:
            self._arabicStyle = "Kufi"
        elif "Nastaliq" in self.styles:
            self._arabicStyle = "Nastaliq"
        return self._arabicStyle

    def readJson(self, jsonpath):
        with open(jsonpath, 'r') as subsetDict:
            subset = json.load(subsetDict)
        for i in subset:
            if i in self.writingSystems:
                for g in subset[i]:
                    if g not in self.panEuropeanSub:
                        self.panEuropeanSub.append(g)

    def lgcSub(self):
        self.panEuropeanSub = []
        lgcSub = [s for s in self.writingSystems if s in ["Latin", "Greek", "Cyrillic"]]
        if 0 < len(lgcSub) < 3:
            # add folder
            europeanSubsetFolder = os.path.join(self.scriptsFolder, "EuropeanSubset")
            if not os.path.exists(europeanSubsetFolder):
                os.makedirs(europeanSubsetFolder)
            # make the list of glyphs to keep
            for i in lgcSub:
                self.readJson(os.path.join(
                        self.scriptsFolder,
                        "subsets", i.lower() + "_subset.json"
                        )
                    )
            for ftpath in self.fonts2merge_list:
                if os.path.basename(ftpath).split('-')[0] in self.lgcfonts:
                    font = self.subsetter(ttLib.TTFont(ftpath), self.panEuropeanSub)
                    newpath = os.path.join(europeanSubsetFolder, os.path.basename(ftpath))
                    font.save(newpath)
                    self.fonts2merge_list.remove(ftpath)
                    self.fonts2merge_list.append(newpath)
        else:
            pass


    def buildRepoName(self):
        self.repoNames = []
        for script in self.writingSystems:
            if script in ["Latin", "Greek", "Cyrillic"]:
                name = "Noto" + self.contrast + self.opticalSize + self.italic
            elif script in ["Tamil"]:
                name = "Noto" + self.contrast + script + self.italic
            elif script == "Arabic":
                name = "Noto" + self.contrast + self.arabicStyle
            else:
                name = "Noto" + self.contrast + script
            if name in self.repo_naming_translation:
                name = self.repo_naming_translation[name]
            if self.ui is True and name in self.fonts_with_ui_version:
                name = name+"UI"
            self.repoNames.append(name)
        print(self.repoNames)

        Download(self.repoNames, self.scriptsFolder, self.hinted)

        self.buildWghtWdthstyleName()

    def buildWghtWdthstyleName(self):
        self.wghtwdth_styles = []
        for wdth in self.width:
            for wght in self.weight:
                if wdth == "Normal":
                    self.wghtwdth_styles.append(wght)
                elif wght == "Regular":
                    self.wghtwdth_styles.append(wdth)
                else:
                    self.wghtwdth_styles.append(wdth + wght)

        self.buildFonts2mergeList()

    def buildFonts2mergeList(self):
        for s in self.wghtwdth_styles:
            self.tempStyle = s
            print(self.tempStyle)
            self.fonts2merge_list = []
            print("\n> The followings fonts can be merged:")
            for n in self.repoNames:
                ftname = "-".join([n, s]) + ".ttf"
                ftpath = os.path.join(self.scriptsFolder, n, self.path, ftname)
                # if os.path.isfile(ftpath):
                if Path(ftpath).exists():
                    print("  ✓", os.path.basename(ftpath))
                    self.fonts2merge_list.append(ftpath)
                else:
                    for i in self.width:
                        if i in self.tempStyle:
                            if os.path.isfile(ftpath.replace(i, "")):
                                self.fonts2merge_list.append(ftpath.replace(i, ""))
                                print("  ✓", os.path.basename(ftpath.replace(i, "")), "[FALLBACK]")
                            elif os.path.isfile(ftpath.replace(s, "Regular")):
                                    self.fonts2merge_list.append(ftpath.replace(s, "Regular"))
                                    print("  ✓", os.path.basename(ftpath.replace(s, "Regular")), "[FALLBACK]")
                            else:
                                print("No font matches the requirements. The script", n, "is removed from the list")
            self.lgcSub()
            if self.duplicatesAreResolved is False:
                self.findDuplicate()
            self.prepFontsForMerging()

    def findFallbackStyle(self, width, ftpath):
        print("TEST FALLBACK")
        if width in self.tempStyle:
            if (self.tempStyle == width):
                normalwidthpath = ftpath.replace(width, "Regular")
                # BECAUSE "NONNORMALWIDTH-REGULAR" IS CALLED "NONNORMALWIDTH"
            else:
                normalwidthpath = ftpath.replace(width, "")
            if Path(normalwidthpath).exists():
                print(normalwidthpath)
                return normalwidthpath
            else:
                print("Not possible to find a fallback for ", os.path.basename(ftpath))

    def ft2uni(self):
        ft2unilist = dict()
        for ftpath in self.fonts2merge_list:
            f = ttLib.TTFont(ftpath)
            uni_list = list()
            cmap = f["cmap"].tables
            for table in cmap:
                if table.platformID == 3:
                    for uni, name in table.cmap.items():
                        if uni not in uni_list:
                            uni_list.append(uni)
            ft2unilist[ftpath] = uni_list
        return ft2unilist

    def findDuplicate(self):
        self.prompt = Prompt()
        fonts2test = copy.deepcopy(self.fonts2merge_list)
        ft2unilist = self.ft2uni()

        while len(fonts2test) > 1:
            ft2uni_temp =dict()
            ft2uni_temp[fonts2test[0]] = ft2unilist[fonts2test[0]]
            for i in fonts2test[1:]:
                ft2uni_temp[i] = ft2unilist[i]
                identicAlreadyDone, duplicateTodisplay = self.getIdentic(ft2uni_temp)
                if len(identicAlreadyDone) != 0:
                    self.prompt.addGlyphToRemove(identicAlreadyDone, i)
                if len(duplicateTodisplay) != 0:
                    characters = self.getChrs(duplicateTodisplay)
                    print(
                        "\n>>> The following characters are in both fonts:\n"
                        + characters
                        + "\nWhich font should be the default one?"
                        + "\n  1."
                        + os.path.basename(fonts2test[0]).split("-")[0]
                        + "\n  2."
                        + os.path.basename(fonts2test[1]).split("-")[0]
                        )
                    self.prompt.askfor(duplicateTodisplay,
                        os.path.basename(fonts2test[0]).split("-")[0],
                        os.path.basename(i).split("-")[0])
            del fonts2test[0]
        self.duplicatesAreResolved = True

    def population(self, path):
        populate = list()
        uniToremove = self.prompt.getGlyphsToRemove(os.path.basename(path).split("-")[0])
        uni2glyphname = self.uni2glyphname(path)
        for uni in uni2glyphname:
            if str(uni) not in uniToremove:
                populate.append(uni2glyphname[uni])
        return populate

    def prepFontsForMerging(self):
        self.destination = os.path.join(self.scriptsFolder, "Custom_Fonts")
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        self.actualFonts2merge = list()
        self.subsettedFonts2remove = list()
        # print(self.fonts2merge_list)
        print("\n")
        for path in self.fonts2merge_list:
            if os.path.basename(path).split("-")[0] in self.prompt.getScriptsToSubset():
                print("INFO:", os.path.basename(path).split("-")[0], "subseted")
                keep = self.population(path)
                font = self.subsetter(ttLib.TTFont(path), keep)
                font.save(os.path.join(self.destination, os.path.basename(path)))
                self.actualFonts2merge.append(os.path.join(
                    self.destination, os.path.basename(path))
                    )
                self.subsettedFonts2remove.append(
                    os.path.join(self.destination, os.path.basename(path))
                    )
            else:
                self.actualFonts2merge.append(path)

        self.merging()

    def merging(self):
        print("INFO: starts merging")
        merger = merge.Merger()

        for ftpath in self.actualFonts2merge:
            ft, upm = self.upm(ftpath)
            if upm != 1000:
                scale_font(ft, 1000 / upm)
        self.font = merger.merge(self.actualFonts2merge)
        renamed = self.renamer()
        renamed.save(
            os.path.join(
                self.destination,
                self.newName.replace(" ", "") + "-" + self.tempStyle + ".ttf",
                    )
                )
        for suppr in self.subsettedFonts2remove:
            os.remove(suppr)
        print("INFO: ends merging\n")

    def uni2glyphname(self, ftpath):
        f = ttLib.TTFont(ftpath)
        uni2glyphname = dict()
        cmap = f["cmap"].tables
        for table in cmap:
            if table.platformID == 3:
                for uni, name in table.cmap.items():
                    if uni not in uni2glyphname:
                        uni2glyphname[uni] = name
        return uni2glyphname

    def getIdentic(self, mydict):
        values = list(mydict.values())
        identic = copy.deepcopy(set(values[0]))
        identic2display = []
        identicAlreadyDone = []
        for x in values[1:]:
            identic = identic & set(x)
        for i in identic:
            if i not in self.uniGlyphsAlreadySorted:
                self.uniGlyphsAlreadySorted.append(i)
                identic2display.append(i)
            else:
                identicAlreadyDone.append(i)
        return identicAlreadyDone, identic2display

    def duplicate(self, head, tail):
        self.toKeep = {**self.uni2glyphname(head), **self.toKeep}
        self.toSubset = self.uni2glyphname(tail)
        duplicate = set(self.toKeep.keys()) & set(self.toSubset.keys())
        remove = []
        for i in duplicate:
            remove.append(self.toSubset[i])
        populate = []
        for i in ttLib.TTFont(tail).getGlyphOrder():
            if i not in remove:
                populate.append(i)
        return populate

    def commonStyles(self):
        styles_dict = {}
        for family in self.repoNames:
            style_list = []
            ftfolderpath = os.path.join(self.scriptsFolder, family, self.path)
            for i in os.listdir(ftfolderpath):
                style_list.append(i.split("-")[1].replace(".ttf", ""))
            styles_dict[family] = style_list
        self.common = self.getIdentic(styles_dict)
        self.merger()

    def glyphOrders(self, fontpathlist):
        ftpath2glyphorder = dict()
        for fpath in fontpathlist:
            ftpath2glyphorder[fpath] = ttLib.TTFont(fpath).getGlyphOrder()
        return ftpath2glyphorder

    def getChrs(self, duplicate):
        s = ""
        l = []
        for uni in duplicate:
            s += chr(uni) + " "
            l.append(chr(uni))
        return s

    def upm(self, ftpath):
        ft = ttLib.TTFont(ftpath)
        upm = ft["head"].unitsPerEm
        return ft, upm

    def subsetter(self, font, subset):
        options = Options()
        options.layout_features = ""  # keep all GSUB/GPOS features
        options.glyph_names = False  # keep post glyph names
        options.legacy_cmap = True  # keep non-Unicode cmaps
        options.name_legacy = True  # keep non-Unicode names
        options.name_IDs = ["*"]  # keep all nameIDs
        options.name_languages = ["*"]  # keep all name languages
        options.notdef_outline = False
        options.ignore_missing_glyphs = True
        options.prune_unicode_ranges = True
        subsetter = Subsetter(options=options)
        subsetter.populate(glyphs=subset)
        subsetter.subset(font)

        return font

    def swaper(self):  # BUILD THE FONTS FROM SOURCES FOR THIS SPECIFIC CASE?
        pass

    def fontmaker(self):
        pass

    def renamer(self):
        if self.newName:
            renamedFont = self.font
            for namerecord in renamedFont["name"].names:
                namerecord.string = namerecord.toUnicode()
                if namerecord.nameID == 1:
                    name = namerecord.string
                if namerecord.nameID == 2:
                    WeightName = namerecord.string
                if namerecord.nameID == 16:
                    name = namerecord.string
                if namerecord.nameID == 17:
                    WeightName = namerecord.string
            for namerecord in renamedFont["name"].names:
                namerecord.string = namerecord.toUnicode()
                # Create the naming of the font Family + style if the style is non RBIBI
                if namerecord.nameID == 1:
                    if WeightName in ["Bold", "Regular", "Italic", "Bold Italic"]:
                        namerecord.string = self.newName
                    else:
                        namerecord.string = self.newName + " " + WeightName
                if namerecord.nameID == 3:
                    unicID = namerecord.string.split(";")
                    newUnicID = (
                        unicID[0]
                        + ";"
                        + unicID[1]
                        + ";"
                        + "".join(self.newName.split(" "))
                        + "-"
                        + "".join(WeightName.split(" "))
                    )
                    namerecord.string = newUnicID
                if namerecord.nameID == 4:
                    namerecord.string = self.newName + " " + WeightName
                if namerecord.nameID == 6:
                    namerecord.string = (
                        "".join(self.newName.split(" "))
                        + "-"
                        + "".join(WeightName.split(" "))
                    )
                if namerecord.nameID == 16:
                    namerecord.string = self.newName

            return renamedFont

def main():
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", nargs=1)
    parser.add_argument("-s", "--scripts", nargs="*")
    parser.add_argument("-o", "--output", nargs="*")
    parser.add_argument("--contrast", nargs=1)
    parser.add_argument("--styles", nargs="*")
    parser.add_argument("--swap", nargs="*")
    parser.add_argument("--subset", nargs="*")
    parser.add_argument("--weight", nargs="*")
    parser.add_argument("--width", nargs="*")
    parser.add_argument("--hinted")
    parser.add_argument("--ui")
    # parser.add_argument("--vmetrics", nargs=3) # TODO
    args = parser.parse_args()

    newName = "Personal Noto"
    subsets = list()
    swapedstyles = list()
    output = ["ttf"]
    weight = ["Regular"]
    width = ["Normal"]
    styles = ""
    hinted = False
    ui = False

    if "--output" in sys.argv:
        output = args.output
    if "-styles" in sys.argv:
        styles = args.styles
    if "-n" in sys.argv:
        newName = args.name
    if "--swap" in sys.argv:
        swapedstyles = args.swap
    if "--subset" in sys.argv:
        subsets = args.subset
    if "--weight" in sys.argv:
        weight = args.weight
    if "--width" in sys.argv:
        width = args.width
    if "--hinted" in sys.argv:
        hinted = True
    if "--ui" in sys.argv:
        ui = True

    build = Notobuilder(
        newName,  # optional
        output,  # only ttf for now
        args.scripts,  # list of writing systems
        args.contrast,  # sans or serif
        styles,  # italic, kufi, display, etc…
        subsets,  # TBD
        swapedstyles,  # TODO
        weight,  # list of weight. Set as Regular if not specified
        width,  # list of width. Set as Normal if not specified
        hinted,  # take unhinted fonts as default. Hinted ones will be used if option is called with --hinted
        ui,
    )


if __name__ == "__main__":
    sys.exit(main())