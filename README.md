# noto-build

Scripts, data and libraries to work with Noto fonts and sources.

Requires Python 3.4 and the following packages:

    pip3 install urllib fonttools argparse requests defcon


#### nightlybuild.py

Used in other Noto repositories to automatically build fonts on each commit pushed to their master branch via GitHub Actions.

#### notobuilderCLI.py

The Notobuilder class is made for users to build their own custom Noto families.

The user has to give to the function the writing system and the contrast (Sans or Serif).
One can define the weight(s), width(s) and style:
Italic and Display for LGC (Latin, Greek and Cyrillic) writing systems, 
the Regular weight and Normal width being the default;
Kufi and Nastaliq for Arabic, the Naskh style being the default one.
Tamil accepts the Italic option if the contrast is tagged as Serif, and returns the NotoSerifTamilSlanted family).

Binary fonts are downloaded locally on the user's computer, and then merged. 

Run it in a Terminal, using some of the following arguments:

* --name
  * To set a custom name
  * Optional
* --scripts
  * The wanted writing systems, separated by space and starting with an uppercase
  * Don't specify the family name, the program will resolve it for you
* --contrast
  * Serif or Sans, the script can manage families with no prefix
* --styles
  * Italic, Display, Kufi, Nastaliq
  * Optional
* --weight
  * The weight(s) you want
  * Defaults to Regular if not specified
* --width
  * The widths you want
  * Defaults to Normal if not specified
* --hinted
  * Downloads hinted fonts
  * Defaults to False

Examples:

```
python ~/notobuilderCLI.py \
  --contrast Sans \
  --script Thai
```
