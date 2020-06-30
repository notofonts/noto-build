# noto-build
Scripts, data and libraries to work with Noto fonts and sources

## nightlybuild.py
The nightlybuild.py code is used by other noto repositories to automatically build fonts on each push on the master branch.

## notobuilderCLI.py
The Notobuilder class is made for allowing users to build their own custom Noto families. The user had to give to the function the writing system and the contrast (Sans or Serif). One can define the weight(s), width(s) and style (Italic and Display for Latin, Greek and Cyrillic writing systems, the Regular weight and Normal width being the default; Kufi and Nastaliq for Arabic, the Naskh style being the default one. Tamil accepts the Italic option if the constrast is tagged as Serif, and return the NotoSerifTamilSlanted family). Binary fonts are downloaded locally on the user's computer, and then merged. 

So far to use it you need to input : python ~/notobuilderCLI.py in a terminal, followed by some of the following argument
  --name, (to set a custom name, optional)
   --scripts, (the wanted writing systems separated by space and starting with an uppercase. Don't specify the family name, the program resolve it for you)
  --contrast, (Serif or Sans, the script can manage families with no prefix)
  --styles (Italic, Display, Kufi, Nastaliq, optional),
  --subset, (NOT implemented yet)
  --swap, (to put alternate as default (I.alt and J.alt, but also tabular figures, etc. NOT implemented yet)
  --weight, (the weight(s) you want, set as Regular if not specified)
  --width, (the weights you want, set as Normal if not specified)
  --hinted (False by default, if specified, the fonts path is changed to download the hinted fonts)
  ### Requirements:
  You need Python3.4 to make it works, and the following libraries:
  • urllib
  • fonttools
  • argparse
  • requests
  • defcon
