import os
import fontmake
import subprocess
from fontTools import ttLib
from tools.scalefonts import scale_font

class generate():

    def __init__(self):
        # INITATE VARIABLE
        self.failing = list()
        self.MMfailing = list()
        self.srcFolder = os.path.join(os.getcwd(), "main", "sources")
        self.folder_otf = os.path.join(
            os.getcwd(), "main", "fonts", "otf", "unhinted", "instance_otf")
        self.folder_ttf = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "unhinted", "instance_ttf")
        self.folder_var = os.path.join(
            os.getcwd(), "main", "fonts", "ttf", "unhinted", "variable_ttf")
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
    def mti_file(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                path = os.path.join(self.srcFolder, i)
        return open(path, "rb")

    @property
    def masters(self):
        return self.designSpaceDocument.loadSourceFonts(Font)

    def ufo2font(self, ufoSource):
        ttf = subprocess.run(["fontmake", "-u", ufoSource, "-o", "ttf",
            "--output-dir", self.folder_ttf, "--verbose", "ERROR"])
        otf = subprocess.run(["fontmake", "-u", ufoSource, "-o", "otf",
            "--output-dir", self.folder_otf, "--verbose", "ERROR"])

    def designSpace2Var(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".designspace"):
                ds_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(ds_path).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(["fontmake", "-m", ds_path, "-o", "variable",
           "--output-path", savepath, "--verbose", "ERROR"])

    def glyphs2Var(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(["fontmake", "-g", self.glyphsFilePath,
            "-o", "variable", "--output-path", savepath, "--verbose", "ERROR"])
        print("    " + fontName + " Variable Font generated\n")

    def glyphs2VarWithMti(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0].split(".")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(["fontmake", "-g", self.glyphsFilePath,
            "--mti-source", mti_path, "-o", "variable", "--output-path", savepath])
        print("    " + fontName + " Variable Font generated\n")
        # font = ttLib.TTFont(savepath)
        # scale_font(font, 2000 / font["head"].unitsPerEm)

    def glyphsWithMti2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        # if not os.path.exists(self.folder_otf):
        #     os.makedirs(self.folder_otf)
        ttf = subprocess.run(["fontmake", "-g", self.glyphsFilePath, "-o", "ttf",
            "--mti-source", mti_path, "--output-dir", self.folder_ttf, "--verbose", "ERROR"])
        ttf = subprocess.run(["fontmake", "-g", self.glyphsFilePath, "-o", "ttf",
            "-i", "--interpolate-binary-layout", self.folder_ttf,
            "--output-dir", self.folder_ttf, "--verbose", "ERROR"])

    def glyphs2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(["fontmake", "-g", self.glyphsFilePath, "-o", "ttf",
            "--output-dir", self.folder_ttf, "-i", "--verbose", "ERROR"])
        otf = subprocess.run(["fontmake", "-g", self.glyphsFilePath, "-o", "otf",
            "--output-dir", self.folder_otf, "-i", "--verbose", "ERROR"])

    def designspace2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".designspace"):
                ds_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(["fontmake", "-m", ds_path, "-o", "ttf",
            "--output-dir", self.folder_ttf, "-i", "--verbose", "ERROR",
            "--expand-features-to-instances"])
        otf = subprocess.run(["fontmake", "-m", ds_path, "-o", "otf",
            "--output-dir", self.folder_otf, "-i", "--verbose", "ERROR",
            "--expand-features-to-instances"])

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
            elif os.path.isdir((os.path.join(self.srcFolder, i))):
                for f in os.listdir(os.path.join(self.srcFolder, i)):
                    if f.endswith(".glyphs"):
                        self.glyphsFilePath = os.path.join(self.srcFolder, i, f)
                        self.srcFolder = os.path.join(self.srcFolder, i)
                        self.glyphsWithOrWithoutMti()

    def multipleMastersVSsingleMasterUfo(self):
        self.familyName = self.ufoList[0].split("-")[0]
        self.familyPath = self.srcFolder
        self.n = os.path.split(self.familyPath)[1].strip()
        self.designspace_path = self.filePath
        #####################################
        # CASE 1 => MULTIPLE MASTERS FAMILY #
        if len(self.ufoList) > 1:
            self.designSpace2Var()          # make variable
            self.designspace2instances()    # make static ttf fonts
        #############################
        # CASE 2 => ONLY ONE MASTER #
        else:
            print(">>> " + self.n + " family has only one master.\n"\
                  "    A static ttf will be generated instead.")
            if not os.path.exists(self.folder_ttf):
                os.makedirs(self.folder_ttf)
            if not os.path.exists(self.folder_otf):
                os.makedirs(self.folder_otf)
            ufo = self.ufoList[0]
            self.ufo2font(os.path.join(self.srcFolder, ufo))

    def glyphsWithOrWithoutMti(self):
        if self.checkMti is False:
            self.glyphs2instances()         # make static ttf fonts
            self.glyphs2Var()               # make variable
        else:
            self.glyphs2VarWithMti()        # make variable
            self.glyphsWithMti2instances()  # make static ttf fonts

ft = generate()