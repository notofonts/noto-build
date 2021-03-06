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
import fontmake
import subprocess
import shutil
import ttfautohint
from fontTools import ttLib
from third_party.scalefonts import scale_font


class Generate:
    def __init__(self):
        self.failing = list()
        self.MMfailing = list()
        self.srcFolder = os.path.join(os.getcwd(), "main", "sources")
        self.folder_otf = os.path.join(
            os.getcwd(), "main", "fonts", "otf", "unhinted", "instance_otf"
        )
        self.folder_ttf = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "unhinted", "instance_ttf"
        )
        self.folder_var = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "unhinted", "variable_ttf"
        )
        self.instances_ufos = os.path.join(self.srcFolder, "instances_ufos")
        self.master_ufos = os.path.join(self.srcFolder, "master_ufos")
        ### HINTED FOLDER
        self.hinted_folder_ttf = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "hinted", "instance_ttf"
        )
        self.hinted_folder_otf = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "hinted", "instance_otf"
        )
        self.hinted_folder_var = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "hinted", "variable_ttf"
        )
        self.natureOfSource()

    @property
    def designSpace(self):
        designspace = DesignSpaceDocument()
        designspace.read(self.designspace_path)
        return designspace

    @property
    def ufoList(self):
        ufoList_ = list()
        for element in os.listdir(self.srcFolder):
            if element.endswith(".ufo"):
                ufoList_.append(element)
        return ufoList_

    @property
    def checkMti(self):
        checkMtiBool = False
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist"):
                checkMtiBool = True
        return checkMtiBool

    @property
    def masters(self):
        return self.designSpaceDocument.loadSourceFonts(Font)

    def scaleFont(self, ftpath):
        pass
        # font = ttLib.TTFont(ftpath)
        # scale_font(font, 2000 / font["head"].unitsPerEm)

    def cleanRepo(self):
        shutil.rmtree(self.master_ufos)
        shutil.rmtree(self.instances_ufos)

    def ufo2font(self, ufoSource):
        ttf = subprocess.run(
            [
                "fontmake",
                "-u",
                ufoSource,
                "-o",
                "ttf",
                "--output-dir",
                self.folder_ttf,
                "--verbose",
                "ERROR",
            ]
        )
        otf = subprocess.run(
            [
                "fontmake",
                "-u",
                ufoSource,
                "-o",
                "otf",
                "--output-dir",
                self.folder_otf,
                "--verbose",
                "ERROR",
            ]
        )
        self.autohint(self.folder_ttf, self.hinted_folder_ttf)

    def designSpace2Var(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".designspace"):
                ds_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(ds_path).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(
            [
                "fontmake",
                "-m",
                ds_path,
                "-o",
                "variable",
                "--output-path",
                savepath,
                "--verbose",
                "ERROR",
            ]
        )
        self.scaleFont(savepath)
        self.autohint(self.folder_var, self.hinted_folder_var)

    def glyphs2Var(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "variable",
                "--output-path",
                savepath,
                "--verbose",
                "ERROR",
            ]
        )
        self.scaleFont(savepath)
        print("    " + fontName + " Variable Font generated\n")
        self.autohint(self.folder_var, self.hinted_folder_var)

    def glyphs2VarWithMti(self):
        print("start")
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist"):
                mti_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "--mti-source",
                mti_path,
                "-o",
                "variable",
                "--output-path",
                savepath,
                "--feature-writer",
                "None",
            ]
        )
        print("    " + fontName + " Variable Font generated\n")
        self.scaleFont(savepath)
        self.autohint(self.folder_var, self.hinted_folder_var)

    def glyphsWithMti2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist"):
                mti_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "ttf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "--mti-source",
                mti_path,
                "--output-dir",
                self.folder_ttf,
                "--verbose",
                "ERROR",
                "--feature-writer",
                "None",
            ]
        )
        # Re-run to use ttf as sources to interpolate the GPOS
        ttf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "ttf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "-i",
                "--interpolate-binary-layout",
                self.folder_ttf,
                "--output-dir",
                self.folder_ttf,
                "--verbose",
                "ERROR",
                "--feature-writer",
                "None",
            ]
        )

        otf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "otf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "--mti-source",
                mti_path,
                "--output-dir",
                self.folder_otf,
                "--verbose",
                "ERROR",
                "--feature-writer",
                "None",
            ]
        )
        otf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "otf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "-i",
                "--interpolate-binary-layout",
                self.folder_otf,
                "--output-dir",
                self.folder_otf,
                "--verbose",
                "ERROR",
                "--feature-writer",
                "None",
            ]
        )
        self.cleanRepo()
        self.autohint(self.folder_ttf, self.hinted_folder_ttf)

    def quadraticGlyphsWithMti2instances(self):
        for i in os.listdir(self.tempSrcFolder):
            if i.endswith(".plist"):
                mti_path = os.path.join(self.tempSrcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(
            [
                "fontmake",
                "-g", self.glyphsFilePath,
                "--overlaps-backend", "pathops",
                "-o", "ttf",
                "--master-dir", self.master_ufos,
                "--instance-dir", self.instances_ufos,
                "--mti-source", mti_path,
                "--output-dir", self.folder_ttf,
                "--verbose", "ERROR",
                "--feature-writer", "None",
            ]
        )

        otf = subprocess.run(
            [
                "fontmake",
                "-g", self.glyphsFilePath,
                "--overlaps-backend", "pathops",
                "-o", "otf",
                "--master-dir", self.master_ufos,
                "--instance-dir", self.instances_ufos,
                "--mti-source", mti_path,
                "--output-dir", self.folder_otf,
                "--verbose", "ERROR",
                "--feature-writer", "None",
            ]
        )
        self.cleanRepo()
        self.autohint(self.folder_ttf, self.hinted_folder_ttf)

    def glyphs2instances(self):
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "ttf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "--output-dir",
                self.folder_ttf,
                "-i",
                "--verbose",
                "ERROR",
            ]
        )
        otf = subprocess.run(
            [
                "fontmake",
                "-g",
                self.glyphsFilePath,
                "-o",
                "otf",
                "--master-dir",
                self.master_ufos,
                "--instance-dir",
                self.instances_ufos,
                "--output-dir",
                self.folder_otf,
                "-i",
                "--verbose",
                "ERROR",
            ]
        )
        self.autohint(self.folder_ttf, self.hinted_folder_ttf)

    def designspace2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".designspace"):
                ds_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(
            [
                "fontmake",
                "-m",
                ds_path,
                "-o",
                "ttf",
                "--output-dir",
                self.folder_ttf,
                "-i",
                "--verbose",
                "ERROR",
                "--expand-features-to-instances",
            ]
        )
        otf = subprocess.run(
            [
                "fontmake",
                "-m",
                ds_path,
                "-o",
                "otf",
                "--output-dir",
                self.folder_otf,
                "-i",
                "--verbose",
                "ERROR",
                "--expand-features-to-instances",
            ]
        )

        self.autohint(self.folder_ttf, self.hinted_folder_ttf)

    def autohint(self, folder, hintedFolder):
        print("START")
        for ft in os.listdir(folder):
            print(folder, ft)
            ftpath = os.path.join(folder, ft)
            hintedFontPath = os.path.join(hintedFolder, ft)
            if not os.path.exists(hintedFolder):
                os.makedirs(hintedFolder)
            try:
                ttfautohint.ttfautohint(in_file=ftpath, out_file=hintedFontPath)
            except:
                print("Not possible to autohint the fonts")

    #####################################################################
    # INITIAL FUNCTIONS THAT FINDS IN WHICH CATEGORY THE FAMILY BELONGS #
    #####################################################################
    def natureOfSource(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".glyphs"):
                print("GLYPHS FILE")
                self.glyphsFilePath = os.path.join(self.srcFolder, i)
                self.glyphsWithOrWithoutMti()
            if i.endswith(".designspace"):
                print("UFOs FILES")
                self.filePath = os.path.join(self.srcFolder, i)
                self.multipleMastersVSsingleMasterUfo()
            elif os.path.isdir((os.path.join(self.srcFolder, i))): # "Arimo", "Tinos" & "Cousine" families
                import pathops
                for f in os.listdir(os.path.join(self.srcFolder, i)):
                    if f.endswith(".glyphs"):
                        print(f)
                        self.glyphsFilePath = os.path.join(self.srcFolder, i, f)
                        self.tempSrcFolder = os.path.join(self.srcFolder, i)
                        self.quadraticGlyphsWithMti2instances()

    def multipleMastersVSsingleMasterUfo(self):
        self.familyName = self.ufoList[0].split("-")[0]
        self.familyPath = self.srcFolder
        self.n = os.path.split(self.familyPath)[1].strip()
        self.designspace_path = self.filePath
        #####################################
        # CASE 1 => MULTIPLE MASTERS FAMILY #
        if len(self.ufoList) > 1:
            try:
                self.designSpace2Var()  # make variable
            except:
                pass
            self.designspace2instances()  # make static ttf fonts
        #############################
        # CASE 2 => ONLY ONE MASTER #
        else:
            print(
                ">>> " + self.n + " family has only one master.\n"
                "    A static ttf will be generated instead."
            )
            if not os.path.exists(self.folder_ttf):
                os.makedirs(self.folder_ttf)
            if not os.path.exists(self.folder_otf):
                os.makedirs(self.folder_otf)
            ufo = self.ufoList[0]
            self.ufo2font(os.path.join(self.srcFolder, ufo))

    def glyphsWithOrWithoutMti(self):
        if self.checkMti is False:
            self.glyphs2instances()  # make static fonts
            try:
                self.glyphs2Var()  # make variable
            except:
                pass
        else:
            try:
                self.glyphs2VarWithMti()  # make variable
            except:
                pass
            self.glyphsWithMti2instances()  # make static fonts




def main():
    ft = Generate()

if __name__ == "__main__":
    import sys
    sys.exit(main())