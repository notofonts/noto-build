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

    ############
    # PROPERTY #
    ############
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

    ######################
    # PREPROCESS SOURCES #
    ######################
    def parseGlyphsFile(self):
        self.ufos = glyphsLib.load_to_ufos(open(self.glyphsFilePath))
        font = glyphsLib.parser.load(open(self.glyphsFilePath))
        print("Start working on", self.ufos[0].info.familyName)
        self.designSpaceDocument = glyphsLib.builder.to_designspace(font)

    def add_mti_features_to_master(self):
        ufoWithMtiData = []
        mti_paths = readPlist(self.mti_file)
        for master in self.masters:
            key = master.info.familyName.replace(
                " ", "")+"-"+master.info.styleName.replace(" ", "")
            for table, path in mti_paths[key].items():
                with open(os.path.join(self.srcFolder, path), "rb") as mti_:
                    ufo_path = (
                        "com.github.googlei18n.ufo2ft.mtiFeatures/%s.mti"
                        % table.strip()
                    )
                    master.data[ufo_path] = mti_.read()
                # If we have MTI sources, any Adobe feature files derived from
                # the Glyphs file should be ignored. We clear it here because
                # it only contains junk information anyway.
                master.features.text = ""
                ufoWithMtiData.append(master)
                # Don't save the ufo, to keep them clean from mti data
        print("    ufos updated with MTI data")
        return ufoWithMtiData

    ######################
    # GENERATE FUNCTIONS #
    ######################
    def ufo2font(self, ufoSource):
        ufo = Font(ufoSource)
        ttf = compileTTF(
            ufo, removeOverlaps=True,
            useProductionNames=False,
            featureWriters=[
                KernFeatureWriter(mode="append"),
                MarkFeatureWriter
                ]
            )
        ttf.save(os.path.join(
            self.folder_ttf,
            os.path.basename(ufoSource)[:-4] + ".ttf"))
        otf = compileOTF(
            ufo, removeOverlaps=True,
            useProductionNames=False,
            featureWriters=[
                KernFeatureWriter(mode="append"),
                MarkFeatureWriter
                ]
            )
        otf.save(os.path.join(
            self.folder_otf,
            os.path.basename(ufoSource)[:-4] + ".otf"))
        print("    " + self.familyName + " has been generated.\n")

    def designSpace2Var(self):
        ds = self.designSpace
        print("\n>>> Load the {} designspace".format(self.familyName))
        print("    Load " + self.familyName + " files")
        ds.loadSourceFonts(Font)
        print("    Start to build Variable Tables")
        feature_Writers = [KernFeatureWriter(mode="append"), MarkFeatureWriter]
        font, _, _ = varLib.build(
            compileInterpolatableTTFsFromDS(
                ds, featureWriters=feature_Writers), optimize=False)
        scale_font(font, 2000 / font["head"].unitsPerEm)
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        font.save(os.path.join(
            self.folder_var, self.familyName + "-VF.ttf"))
        print("    " + self.familyName + " Variable Font generated\n")

    def glyphs2Var(self):
        self.parseGlyphsFile()
        ds = self.designSpaceDocument
        # family = os.path.basename(self.familyPath)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0]
        print("\n>>> Load the {} designspace".format(fontName))
        print("    Load "+fontName+" files")
        ds.loadSourceFonts(Font)
        print("    Start to build Variable Tables")
        feature_Writers = [KernFeatureWriter(mode="append"), MarkFeatureWriter]
        font, _, _ = varLib.build(
            compileInterpolatableTTFsFromDS(
                ds, featureWriters=feature_Writers), optimize=False)
        scale_font(font, 2000 / font["head"].unitsPerEm)
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        font.save(os.path.join(self.folder_var, fontName + "-VF.ttf"))
        print("    " + fontName + " Variable Font at 2000 UPM generated\n")

    def glyphs2VarWithMti(self):
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0]
        savepath = os.path.join(self.folder_var, fontName + "-VF.ttf")
        var = subprocess.run(["fontmake", "-g", self.glyphsFilePath,
            "--mti-source", mti_path, "-o", "variable", "--output-path", savepath])
        print("    " + fontName + " Variable Font generated\n")
        font = ttLib.TTFont(savepath)
        scale_font(font, 2000 / font["head"].unitsPerEm)
        print("    " + fontName + " Variable Font at 2000 UPM generated\n")

    def glyphsWithMti2instances(self):
        for i in os.listdir(self.srcFolder):
            if i.endswith(".plist") and "UI" not in i:
                mti_path = os.path.join(self.srcFolder, i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        ttf = subprocess.run(["fontmake", "-g", self.glyphsFilePath, "-o", "ttf",
            "--mti-source", mti_path, "--output-dir", self.folder_ttf, "--verbose", "ERROR"])

    def glyphs2instances(self):
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        if not os.path.exists(self.folder_otf):
            os.makedirs(self.folder_otf)
        self.parseGlyphsFile()
        for u in self.ufos:
            # 1. MAKE TTF
            ttf = compileTTF(
                u, removeOverlaps=True,
                useProductionNames=False,
                featureWriters=[
                    KernFeatureWriter(mode="append"),
                    MarkFeatureWriter
                    ]
                )
            ttf.save(os.path.join(
                self.folder_ttf,
                u.info.familyName.replace(" ", "")\
                +"-"+u.info.styleName.replace(" ", "")+ ".ttf"))
            # 2. MAKE OTF
            otf = compileOTF(
                u, removeOverlaps=True,
                useProductionNames=False,
                featureWriters=[
                    KernFeatureWriter(mode="append"),
                    MarkFeatureWriter
                    ]
                )
            otf.save(os.path.join(
                self.folder_otf,
                u.info.familyName.replace(" ", "")\
                +"-"+u.info.styleName.replace(" ", "")+ ".ttf"))

    def designspace2instances(self):
        fp = FontProject()
        fonts = fp.run_from_designspace(
            expand_features_to_instances=True,
            use_mutatormath=False,
            designspace_path=self.designspace_path,
            interpolate=True,
            output=("otf"),
            output_dir=os.path.join(self.srcFolder, "instance_ufos")
            )
        instances_ufos = list()
        for i in os.listdir(os.path.join(self.srcFolder, "instance_ufos")):
            if i.endswith(".ufo"):
                instances_ufos.append(i)
        if not os.path.exists(self.folder_ttf):
            os.makedirs(self.folder_ttf)
        for ufo in instances_ufos:
            self.ufo2font(os.path.join(self.srcFolder, "instance_ufos", ufo))

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

    # DEAL WITH UFO SOURCES
    def multipleMastersVSsingleMasterUfo(self):
        self.familyName = self.ufoList[0].split("-")[0]
        self.familyPath = self.srcFolder
        self.n = os.path.split(self.familyPath)[1].strip()
        self.designspace_path = self.filePath
        #####################################
        # CASE 1 => MULTIPLE MASTERS FAMILY #
        if len(self.ufoList) > 1:
            #1. make variable
            self.designSpace2Var()
            #2. make static ttf fonts
            self.designspace2instances()
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

    # DEAL WITH GLYPHS SOURCES FAMILIES
    def glyphsWithOrWithoutMti(self):
        if self.checkMti is False:
            self.glyphs2instances()
            self.glyphs2Var()
        else:
            self.glyphs2VarWithMti()
            self.glyphsWithMti2instances()

ft = generate()