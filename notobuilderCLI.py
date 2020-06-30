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


class Notobuilder:

    """ 'subsets' is a list of dict {nameOfSubset:[list ofGlypgs2keep]}
        'writingsystems' is a list. From this list and 2 arguments
        ('--contrast, i.e. Sans or Serif
        and '--styles', i.e. Italic, Display, Kufi or Nastaliq),
        one can pick the right source.
        If there is more than 1 writingsystem, the class assumes
        you ask for a merging (with the exception of LGC fonts).
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
    ):
        self.scriptsFolder = os.path.split(sys.argv[0])[0]
        self.sources = writingsystems
        self.newName = " ".join(newName)
        self.output = ["ttf"]  # otf and variable merger not available at this point
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

        self.path = "instance_ttf"
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
            "NotoNaskhArabic",
            "NotoSansArabic",
            "NotoSansBengali",
            "NotoSansDevanagari",
            "NotoSansGujarati",
            "NotoSansGurmukhi",
            "NotoSansKannada",
            "NotoSansKhmer",
            "NotoSansLao",
            "NotoSansMalayalam",
            "NotoSansMyanmar",
            "NotoSansOriya",
            "NotoSansSinhala",
            "NotoSansTamil",
            "NotoSansTelugu",
            "NotoSansThai",
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

    def buildRepoName(self):
        self.repoNames = []
        for script in self.sources:
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
            self.repoNames.append(name)

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
            self.fonts2merge_list = []
            for n in self.repoNames:
                ftname = "-".join([n, s]) + ".ttf"
                ftpath = os.path.join(self.scriptsFolder, n, self.path, ftname)
                # if os.path.isfile(ftpath):
                if Path(ftpath).exists():
                    print(os.path.basename(ftpath), " exists")
                    self.fonts2merge_list.append(ftpath)
                else:
                    if "Normal" not in self.width:
                        for width in [
                            "Condensed",
                            "SemiCondensed",
                            "Compressed",
                            "Extended",
                        ]:
                            self.fonts2merge_list.append(
                                self.findFallbackStyle(width, ftpath)
                            )
                    else:
                        if os.path.isfile(ftpath.replace(s, "Regular")):
                            self.fonts2merge_list.append(ftpath.replace(s, "Regular"))
                        elif os.path.isfile(ftpath.replace(s, "")):
                            self.fonts2merge_list.append(ftpath.replace(s, ""))
                        else:
                            print("No font matches the requirements.")
            self.merging()

    def findFallbackStyle(self, chasse, ftpath):
        if chasse in self.tempStyle:
            if (
                self.tempStyle == chasse
            ):
                normalwidthpath = ftpath.replace(chasse, "Regular")
                # BECAUSE "NONNORMALWIDTH-REGULAR" IS CALLED "NONNORMALWIDTH"
            else:
                normalwidthpath = ftpath.replace(chasse, "")
            if Path(normalwidthpath).exists():
                return normalwidthpath
            else:
                print("Not possible to find a fallback for ", os.path.basename(ftpath))

    def merging(self):
        subsettedFonts2remove = []
        print("starts merging")
        actualFonts2merge = list()
        destination = os.path.join(self.scriptsFolder, "Custom_Fonts")
        if not os.path.exists(destination):
            os.makedirs(destination)
        merger = merge.Merger()
        if len(self.default) != 0:
            pass
        else:
            self.reorganizeListOrder()
        actualFonts2merge.append(self.fonts2merge_list[0])
        for path in self.fonts2merge_list[1:]:
            sub = self.duplicate(
                self.fonts2merge_list[self.fonts2merge_list.index(path) - 1], path
            )
            font = self.subsetter(ttLib.TTFont(path), sub)
            font.save(os.path.join(destination, os.path.basename(path)))
            actualFonts2merge.append(os.path.join(destination, os.path.basename(path)))
            subsettedFonts2remove.append(
                os.path.join(destination, os.path.basename(path))
            )
        print([os.path.basename(i) for i in actualFonts2merge])
        for ftpath in actualFonts2merge:
            ft, upm = self.upm(ftpath)
            if upm != 1000:
                scale_font(ft, 1000 / upm)
        self.font = merger.merge(actualFonts2merge)
        renamed = self.renamer()
        renamed.save(
            os.path.join(
                destination,
                self.newName.replace(" ", "") + "-" + self.tempStyle + ".ttf",
            )
        )
        for suppr in subsettedFonts2remove:
            os.remove(suppr)
        print("ends merging\n")

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
        for x in values[1:]:
            identic = identic & set(x)
        return identic

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
        for uni in duplicate:
            s += chr(uni) + " "
        return s

    def detectConflicts(self):
        self.default = []
        fonts2test = copy.deepcopy(self.fonts2merge_list)
        ft2unilist = dict()
        while len(fonts2test) > 1:
            for ft in fonts2test[0:]:
                f = ttLib.TTFont(ft)
                uni_list = list()
                cmap = f["cmap"].tables
                for table in cmap:
                    if table.platformID == 3:
                        for uni, name in table.cmap.items():
                            if uni not in uni_list:
                                uni_list.append(uni)
                ft2unilist[ft] = uni_list
            # for g in ft2unilist:
            #     print(g, len(ft2unilist[g]))
            duplicate = self.getIdentic(ft2unilist)
            characters = self.getChrs(duplicate)
            if len(duplicate) != 0:
                print(
                    "\nThe following characters are in both fonts:\n"
                    + "    >>> "
                    + characters
                    + "\nWhich font should be the default one?"
                    + "\n1."
                    + os.path.basename(fonts2test[0]).replace(".ttf", "")
                    + "\n2."
                    + os.path.basename(fonts2test[1]).replace(".ttf", "")
                )
                request = input(">>> ")
                self.default.append(fonts2test[int(request) - 1])
            del fonts2test[0]
        if len(self.default) != 0:
            return True
        else:
            return False

    def reorganizeListOrder(self):
        if self.detectConflicts() is True:
            newOrder = list(self.default)
            for i in self.fonts2merge_list:
                if i not in newOrder:
                    newOrder.append(i)
            self.fonts2merge_list = newOrder
        else:
            pass

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

    # def mergerOnlySameWghtWdth(self):
    #     destination = os.path.join(self.scriptsFolder, "Custom_Fonts")
    #     if not os.path.exists(destination):
    #         os.makedirs(destination)
    #     merger = merge.Merger()
    #     for style in self.common:
    #         fonts2merge = list()
    #         for script in self.repoNames:
    #             ft_path = os.path.join(
    #                 self.scriptsFolder, script, self.path, script + "-" + style + ".ttf"
    #             )
    #             fonts2merge.append(ft_path)
    #         ftpath2gorders = self.glyphOrders(fonts2merge)
    #         actualFonts2merge = list()
    #         actualFonts2merge.append(fonts2merge[0])
    #         for path in fonts2merge[1:]:
    #             sub = ftpath2gorders[path]
    #             for glyf in sub:
    #                 if glyf in ftpath2gorders[fonts2merge[fonts2merge.index(path) - 1]]:
    #                     sub.remove(glyf)
    #             font = self.subsetter(ttLib.TTFont(path), sub)
    #             font.save(os.path.join(destination, os.path.basename(path)))
    #             actualFonts2merge.append(
    #                 os.path.join(destination, os.path.basename(path))
    #             )
    #         self.font = merger.merge(actualFonts2merge)
    #         renamed = self.renamer()
    #         renamed.save(
    #             os.path.join(
    #                 destination, self.newName.replace(" ", "") + "-" + style + ".ttf"
    #             )
    #         )


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
    )


if __name__ == "__main__":
    sys.exit(main())
