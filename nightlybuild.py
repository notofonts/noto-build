import os
import glyphsLib
from tools.scalefonts          import scaleFont
from fontTools                 import ttLib
from fontTools.misc.plistlib   import load as readPlist

from fontmake.font_project     import FontProject

from defcon                    import Font
from ufo2ft                    import compileOTF, compileTTF
from fontTools                 import varLib
from fontTools.designspaceLib  import DesignSpaceDocument
from ufo2ft                    import compileInterpolatableTTFsFromDS
from ufo2ft.featureCompiler    import (FeatureCompiler, MtiFeatureCompiler)
from ufo2ft.featureWriters     import (KernFeatureWriter,
                                        MarkFeatureWriter,
                                        loadFeatureWriters,
                                        ast
                                        )
class generate():

    def __init__(self, ):
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
    # GENERATE FUNCTIONS #
    ######################
    def ufo2font(self, ufoSource):
        ufo = Font(ufoSource)
        ttf = compileTTF(
                        ufo,
                        removeOverlaps=True,
                        useProductionNames=False,
                        featureWriters=[
                            KernFeatureWriter(mode="append"),
                            MarkFeatureWriter
                            ]
                        )
        ttf.save(os.path.join(
            self.folder_ttf,
            os.path.basename(ufoSource)[:-4] + ".ttf"))
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
        scaleFont(font, 2000)
        if not os.path.exists(self.folder_var):
            os.makedirs(self.folder_var)
        font.save(os.path.join(
            self.folder_var, self.familyName + "-VF.ttf"))
        print("    " + self.familyName + " Variable Font generated\n")

    def parseGlyphsFile(self):
        self.ufos = glyphsLib.load_to_ufos(open(self.glyphsFilePath))
        font = glyphsLib.parser.load(open(self.glyphsFilePath))
        print("Start working on", self.ufos[0].info.familyName)
        self.designSpaceDocument = glyphsLib.builder.to_designspace(font)

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
        scaleFont(font, 2000)
        font.save(os.path.join(self.folder_var, fontName + "-VF.ttf"))
        print("    " + fontName + " Variable Font at 2000 UPM generated\n")

    def add_mti_features_to_master():
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

    def glyphs2VarWithMti(self):
        self.parseGlyphsFile()
        ufoSource = self.add_mti_features_to_master()
        ds = self.designSpaceDocument
        fontName = os.path.basename(self.glyphsFilePath).split("-")[0]
        print("\n>>> Load the {} designspace".format(fontName))
        print("    Load "+fontName+" files")
        ds.loadSourceFonts(Font)
        print("    Start to build Variable Tables")
        feature_Writers = MtiFeatureCompiler
        font, _, _ = varLib.build(
            compileInterpolatableTTFsFromDS(
                ds, featureCompilerClass=MtiFeatureCompiler,
                featureWriters=None),
            optimize=False)
        scaleFont(font, 2000)
        font.save(os.path.join(self.folder_var, fontName + "-VF.ttf"))
        print("    " + fontName + " Variable Font at 2000 UPM generated\n")

    def glyphs2instances(self):
        self.parseGlyphsFile()

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
                self.glyphs2Var()
            if i.endswith(".designspace"):
                print("UFOs FILES")
                self.filePath = os.path.join(self.srcFolder, i)
                self.multipleMastersVSsingleMaster()

    def multipleMastersVSsingleMaster(self):
        self.familyName = self.ufoList[0].split("-")[0]
        self.familyPath = self.srcFolder
        self.n = os.path.split(self.familyPath)[1].strip()
        self.designspace_path = self.filePath
        #####################################
        # CASE 1 => MULTIPLE MASTERS FAMILY #
        if len(self.ufoList) > 1:
            #1 make variable
            self.designSpace2Var()
            #2 make static ttf fonts
            # self.designspace2instances()
        #############################
        # CASE 2 => ONLY ONE MASTER #
        else:
            print(">>> " + self.n + " family has only one master.\n"\
                  "    A static ttf will be generated instead.")
            ufo = self.ufoList[0]
            try:
                self.ufo2font(ufo)
            except:
                self.failing.append(ufo)

    def glyphsWithOrWithoutMti():
        for i in os.listdir(self.srcFolder):
            if self.checkMti is False:
                self.glyphs2Var()
            else:
                self.glyphs2VarWithMti()

ft = generate()