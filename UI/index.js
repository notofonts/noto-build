var app = new Vue({
    el: '#app',
    data: function() {
        return {
            ready: false,
            choices: {
                output: [
                    // {
                    //     name:'OTF',
                    //     value:'otf'
                    // },
                    {
                        name:'TTF',
                        value:'ttf'
                    },
                    // {
                    //     name:'VAR',
                    //     value:'var'
                    // },
                    {
                        name:'WOFF2',
                        value:'woff2'
                    }
                ],
                scripts: [
                    {
                        name:'Adlam',
                        value:'Adlam'
                    },
                    {
                        name:'Arabic',
                        value:'Arabic',
                        featured: true
                    },
                    {
                        name:'Armenian',
                        value:'Armenian',
                        featured: true
                    },
                    {
                        name:'Avestan',
                        value:'Avestan'
                    },
                    {
                        name:'Balinese',
                        value:'Balinese'
                    },
                    {
                        name:'Bamum',
                        value:'Bamum'
                    },
                    {
                        name:'Batak',
                        value:'Batak'
                    },
                    {
                        name:'Bengali',
                        value:'Bengali',
                        featured: true
                    },
                    {
                        name:'Brahmi',
                        value:'Brahmi'
                    },
                    {
                        name:'Buginese',
                        value:'Buginese'
                    },
                    {
                        name:'Buhid',
                        value:'Buhid'
                    },
                    {
                        name:'Burmese',
                        value:'Burmese',
                        featured: true
                    },
                    {
                        name:'Canadian Aboriginal',
                        value:'CanadianAboriginal',
                        featured: true
                    },
                    {
                        name:'Carian',
                        value:'Carian'
                    },
                    {
                        name:'Chakma',
                        value:'Chakma'
                    },
                    {
                        name:'Cham',
                        value:'Cham'
                    },
                    {
                        name:'Cherokee',
                        value:'Cherokee',
                        featured: true
                    },
                    {
                        name:'Coptic',
                        value:'Coptic'
                    },
                    {
                        name:'Cuneiform',
                        value:'Cuneiform'
                    },
                    {
                        name:'Cypriot',
                        value:'Cypriot'
                    },
                    {
                        name:'Cyrillic',
                        value:'Cyrillic',
                        featured: true
                    },
                    {
                        name:'Deseret',
                        value:'Deseret'
                    },
                    {
                        name:'Devanagari',
                        value:'Devanagari',
                        featured: true
                    },
                    {
                        name:'Ethiopic',
                        value:'Ethiopic',
                        featured: true
                    },
                    {
                        name:'Georgian',
                        value:'Georgian',
                        featured: true
                    },
                    {
                        name:'Glagolitic',
                        value:'Glagolitic'
                    },
                    {
                        name:'Gothic',
                        value:'Gothic'
                    },
                    {
                        name:'Greek',
                        value:'Greek',
                        featured: true
                    },
                    {
                        name:'Gujarati',
                        value:'Gujarati',
                        featured: true
                    },
                    {
                        name:'Gurmukhi',
                        value:'Gurmukhi',
                        featured: true
                    },
                    {
                        name:'Hanunoo',
                        value:'Hanunoo'
                    },
                    {
                        name:'Hebrew',
                        value:'Hebrew',
                        featured: true
                    },
                    {
                        name:'Imperial Aramaic',
                        value:'ImperialAramaic'
                    },
                    {
                        name:'Inscriptional Pahlavi',
                        value:'InscriptionalPahlavi'
                    },
                    {
                        name:'Inscriptional Parthian',
                        value:'InscriptionalParthian'
                    },
                    {
                        name:'Javanese',
                        value:'Javanese',
                        featured: true
                    },
                    {
                        name:'Kaithi',
                        value:'Kaithi'
                    },
                    {
                        name:'Kannada',
                        value:'Kannada',
                        featured: true
                    },
                    {
                        name:'KayahLi',
                        value:'KayahLi'
                    },
                    {
                        name:'Khmer',
                        value:'Khmer',
                        featured: true
                    },
                    {
                        name:'Lao',
                        value:'Lao',
                        featured: true
                    },
                    {
                        name:'Latin',
                        value:'Latin',
                        featured: true
                    },
                    {
                        name:'Lepcha',
                        value:'Lepcha'
                    },
                    {
                        name:'Limbu',
                        value:'Limbu'
                    },
                    {
                        name:'Linear B',
                        value:'LinearB'
                    },
                    {
                        name:'Lisu',
                        value:'Lisu'
                    },
                    {
                        name:'Lycian',
                        value:'Lycian'
                    },
                    {
                        name:'Lydian',
                        value:'Lydian'
                    },
                    {
                        name:'Malayalam',
                        value:'Malayalam',
                        featured: true
                    },
                    {
                        name:'Mandaic',
                        value:'Mandaic'
                    },
                    {
                        name:'Meetei Mayek',
                        value:'MeeteiMayek'
                    },
                    {
                        name:'Mongolian',
                        value:'Mongolian',
                        featured: true
                    },
                    {
                        name:'Myanmar',
                        value:'Myanmar'
                    },
                    {
                        name:'New Tai Lue',
                        value:'NewTaiLue'
                    },
                    {
                        name:'NKo',
                        value:'NKo'
                    },
                    {
                        name:'Nushu',
                        value:'Nushu'
                    },
                    {
                        name:'Odia',
                        value:'Odia',
                        featured: true
                    },
                    {
                        name:'Ogham',
                        value:'Ogham'
                    },
                    {
                        name:'Ol Chiki',
                        value:'OlChiki'
                    },
                    {
                        name:'Old Italic',
                        value:'OldItalic'
                    },
                    {
                        name:'Old Persian',
                        value:'OldPersian'
                    },
                    {
                        name:'Old South Arabian',
                        value:'OldSouthArabian'
                    },
                    {
                        name:'Old Turkic',
                        value:'OldTurkic'
                    },
                    {
                        name:'Oriya',
                        value:'Oriya'
                    },
                    {
                        name:'Osage',
                        value:'Osage'
                    },
                    {
                        name:'Osmanya',
                        value:'Osmanya'
                    },
                    {
                        name:'Phags Pa',
                        value:'PhagsPa'
                    },
                    {
                        name:'Phoenician',
                        value:'Phoenician'
                    },
                    {
                        name:'Rejang',
                        value:'Rejang'
                    },
                    {
                        name:'Runic',
                        value:'Runic'
                    },
                    {
                        name:'Samaritan',
                        value:'Samaritan'
                    },
                    {
                        name:'Saurashtra',
                        value:'Saurashtra'
                    },
                    {
                        name:'Shavian',
                        value:'Shavian'
                    },
                    {
                        name:'Sinhala',
                        value:'Sinhala',
                        featured: true
                    },
                    {
                        name:'Sundanese',
                        value:'Sundanese',
                        featured: true
                    },
                    {
                        name:'Syloti Nagri',
                        value:'SylotiNagri'
                    },
                    {
                        name:'Syriac Eastern',
                        value:'SyriacEastern'
                    },
                    {
                        name:'Syriac Estrangela',
                        value:'SyriacEstrangela'
                    },
                    {
                        name:'Syriac Western',
                        value:'SyriacWestern'
                    },
                    {
                        name:'Tagalog',
                        value:'Tagalog'
                    },
                    {
                        name:'Tagbanwa',
                        value:'Tagbanwa'
                    },
                    {
                        name:'Tai Le',
                        value:'TaiLe'
                    },
                    {
                        name:'Tai Tham',
                        value:'TaiTham'
                    },
                    {
                        name:'Tai Viet',
                        value:'TaiViet'
                    },
                    {
                        name:'Tamil',
                        value:'Tamil',
                        featured: true
                    },
                    {
                        name:'Telugu',
                        value:'Telugu',
                        featured: true
                    },
                    {
                        name:'Thaana',
                        value:'Thaana',
                        featured: true
                    },
                    {
                        name:'Thai',
                        value:'Thai',
                        featured: true
                    },
                    {
                        name:'Tibetan',
                        value:'Tibetan',
                        featured: true
                    },
                    {
                        name:'Tifinagh',
                        value:'Tifinagh'
                    },
                    {
                        name:'Ugaritic',
                        value:'Ugaritic'
                    },
                    {
                        name:'Vai',
                        value:'Vai'
                    },
                    {
                        name:'Yi',
                        value:'Yi'
                    }
                ],
                contrast: [
                    {
                        name:'Sans',
                        value:'Sans'
                    },
                    {
                        name:'Serif',
                        value:'Serif'
                    }
                ],
                styles: [
                    {
                        name:'Italic',
                        value:'Italic',
                        disabled:true
                    },
                    {
                        name:'Mono',
                        value:'Mono',
                        disabled:true
                    },
                    {
                        name:'Display',
                        value:'Display',
                        disabled:true
                    },
                    {
                        name:'Kufi',
                        value:'Kufi',
                        disabled:true
                    },
                    {
                        name:'Nastaliq',
                        value:'Nastaliq',
                        disabled:true
                    }
                ],
                weight: [
                    {
                        name:'Thin',
                        value:'Thin'
                    },
                    {
                        name:'ExtraLight',
                        value:'ExtraLight'
                    },
                    {
                        name:'Light',
                        value:'Light'
                    },
                    {
                        name:'Regular',
                        value:'Regular'
                    },
                    {
                        name:'Medium',
                        value:'Medium'
                    },
                    {
                        name:'SemiBold',
                        value:'SemiBold'
                    },
                    {
                        name:'Bold',
                        value:'Bold'
                    },
                    {
                        name:'ExtraBold',
                        value:'ExtraBold'
                    },
                    {
                        name:'Black',
                        value:'Black'
                    }
                ],
                width: [
                    {
                        name:'ExtraCondensed',
                        value:'ExtraCondensed'
                    },
                    {
                        name:'SemiCondensed',
                        value:'SemiCondensed'
                    },
                    {
                        name:'Condensed',
                        value:'Condensed'
                    },
                    {
                        name:'Normal',
                        value:'Normal'
                    }
                ],
                metrics: {
                    ascender: {
                        name:'Ascender',
                        min: 0,
                        max: 1000
                    },
                    descender: {
                        name:'Descender',
                        min: -1000,
                        max: 0
                    }
                },
                hinted: {
                    name:'Hinted'
                },
                ui: {
                    name:'UI'
                },
                subset: [
                    {
                        name:'Latin',
                        value:'Latin',
                        subsets: [
                            {
                                name:'Basic Latin',
                                value:'BasicLatin',
                                disabled:true,
                                default:true
                            },
                            {
                                name:'Extended Latin',
                                value:'ExtendedLatin',
                                disabled:true,
                                default:false
                            },
                            {
                                name:'Unicode Latin',
                                value:'UnicodeLatin',
                                disabled:true,
                                default:false
                            }
                        ]
                    },
                    {
                        name:'Greek',
                        value:'Greek',
                        subsets: [
                            {
                                name:'Basic Greek',
                                value:'BasicGreek',
                                disabled:true,
                                default:true
                            },
                            {
                                name:'Extended Greek',
                                value:'ExtendedGreek',
                                disabled:true,
                                default:false
                            }
                        ]
                    },
                    {
                        name:'Cyrillic',
                        value:'Cyrillic',
                        subsets: [
                            {
                                name:'Basic Cyrillic',
                                value:'BasicCyrillic',
                                disabled:true,
                                default:true
                            },
                            {
                                name:'Extended Cyrillic',
                                value:'ExtendedCyrillic',
                                disabled:true,
                                default:false
                            }
                        ]
                    },
                    {
                        name:'Arabic',
                        value:'Arabic',
                        subsets: [
                            {
                                name:'Basic Arabic',
                                value:'BasicArabic',
                                disabled:true,
                                default:true
                            },
                            {
                                name:'Extended Arabic',
                                value:'ExtendedArabic',
                                disabled:true,
                                default:false
                            }
                        ]
                    },
                    {
                        name:'Tamil',
                        value:'Tamil',
                        subsets: [
                            {
                                name:'Basic Tamil',
                                value:'BasicTamil',
                                disabled:true,
                                default:true
                            },
                            {
                                name:'Extended Tamil',
                                value:'ExtendedTamil',
                                disabled:true,
                                default:false
                            }
                        ]
                    }
                ]
            },
            choicesIndexed: {
                scriptsByValue: {},
                stylesByName: {},
                subsetByName: {}
            },
            options: {
                name: '',
                version: '',
                output: [],
                contrast: '',
                styles: [],
                scripts: [],
                scripts_all: false,
                scripts_filter: '',
                scripts_show_all: false,
                scripts_dragging: false,
                weight: [],
                weights_all: false,
                width: [],
                widths_all: false,
                metrics: {
                    ascender: 0,
                    descender: 0
                },
                hinted: false,
                ui: false,
                subset: {
                    Latin: '',
                    Greek: '',
                    Cyrillic: '',
                    Tamil: '',
                    Arabic: ''
                },
                subset_chars: '',
                swap_enabled: false,
                swap_altIJ_enabled: false,
                swap_altIJ: false,
                swap_figures: ''
            },
            command: '',
            commandOk: false,
            copyCommandDone: false,
            copyCommandDoneTimeout: 0
        }
    },
    filters: {
        scriptName: function(value) {
            return app.choicesIndexed.scriptsByValue[value]['name'];
        },
        slugify: function (value) {
            return utils.string.slugify(value);
        },
        upper: function (value) {
            return String(value).toUpperCase();
        }
    },
    methods: {
        clearScriptsFilter: function() {
            this.options.scripts_filter = '';
            this.onChangeScriptsFilter();
        },
        isScriptSelected: function(name) {
            return utils.array.contains(
                this.options.scripts, name);
        },
        toggleScriptsShowAll: function(argument) {
            this.options.scripts_show_all = !this.options.scripts_show_all;
        },
        disableAllStyles: function() {
            // disable all style choices
            this.choices.styles.forEach(function(style) {
                style.disabled = true;
            });
        },
        enableScriptStyles: function(scriptName, styleNames) {
            // enable only style choices of selected scripts
            var scope = this;
            if (this.isScriptSelected(scriptName)) {
                styleNames.forEach(function(styleName) {
                    scope.choicesIndexed.stylesByName[styleName].disabled = false;
                });
            }
        },
        updateStyles: function() {
            this.disableAllStyles();
            this.enableScriptStyles('Latin', ['Italic', 'Display', 'Mono']);
            this.enableScriptStyles('Greek', ['Italic', 'Display', 'Mono']);
            this.enableScriptStyles('Cyrillic', ['Italic', 'Display', 'Mono']);
            this.enableScriptStyles('Tamil', ['Italic']);
            this.enableScriptStyles('Arabic', ['Kufi', 'Nastaliq']);
            this.updateStylesOptions();
        },
        updateStylesOptions: function() {
            // remove disabled style choices from options
            var scope = this;
            this.choices.styles.forEach(function(style) {
                if (style.disabled === true) {
                    utils.array.remove(scope.options.styles, style.value);
                }
            });
        },
        updateStylesArabic: function() {
            var stylesSelected = this.options.styles;
            var indexOfKufi = stylesSelected.indexOf('Kufi');
            var indexOfNastaliq = stylesSelected.indexOf('Nastaliq');
            if (indexOfKufi > -1 && indexOfNastaliq > -1) {
                if (indexOfKufi < indexOfNastaliq) {
                    // remove Kufi on check Nastaliq
                    utils.array.remove(stylesSelected, 'Kufi');
                } else if (indexOfNastaliq < indexOfKufi) {
                    // remove Nastaliq on check Kufi
                    utils.array.remove(stylesSelected, 'Nastaliq');
                }
            }
        },
        updateSubset: function() {
            this.updateSubsetForScript('Arabic');
            this.updateSubsetForScript('Cyrillic');
            this.updateSubsetForScript('Greek');
            this.updateSubsetForScript('Latin');
            this.updateSubsetForScript('Tamil');
        },
        updateSubsetForScript: function(scriptName) {
            var scope = this;
            var subsetScriptSelected = this.isScriptSelected(scriptName);
            var subsetDisabled = Boolean(!subsetScriptSelected);
            // disable Arabic subset controls if Nastaliq is checked
            if (scriptName === 'Arabic' && this.options.styles.indexOf('Nastaliq') > -1) {
                subsetDisabled = true;
            }
            if (this.options.subset_chars !== '') {
                subsetDisabled = true;
            }
            this.updateSubsetForScriptOptions(scriptName, subsetDisabled);
        },
        updateSubsetForScriptOptions: function(scriptName, disabled) {
            var scope = this;
            this.choicesIndexed.subsetByName[scriptName].subsets.forEach(function(subset) {
                subset.disabled = disabled;
                if (disabled === true) {
                    scope.options.subset[scriptName] = '';
                } else {
                    // automatically check default subset(s)
                    if (subset.default === true) {
                        scope.options.subset[scriptName] = subset.value;
                    }
                }
            });
        },
        updateSwap: function() {
            if (this.isScriptSelected('Latin') || this.isScriptSelected('Greek') || this.isScriptSelected('Cyrillic')) {
                this.options.swap_enabled = true;
            } else {
                this.options.swap_enabled = false;
                this.options.swap_altIJ = false;
                this.options.swap_figures = '';
            }
            if (this.options.contrast === 'Sans') {
                this.options.swap_altIJ_enabled = true;
            } else {
                this.options.swap_altIJ_enabled = false;
                this.options.swap_altIJ = false;
            }
        },
        updateSelectDeselectAll: function(allKey, valuesKey) {
            if (this.options[allKey]) {
                var valuesList = this.options[valuesKey];
                var listContains = utils.array.contains;
                this.choices[valuesKey].forEach(function(item) {
                    if (!listContains(valuesList, item.value)) {
                        valuesList.push(item.value);
                    }
                });
            } else {
                this.options[valuesKey] = [];
            }
        },
        onChangeContrast: function() {
            this.updateSwap();
        },
        onChangeStyles: function() {
            this.updateStylesArabic();
            this.updateSubset();
        },
        onChangeScriptsFilter: function() {
            var scripts = this.choices.scripts;
            var filter = this.options.scripts_filter;
            if (filter !== '') {
                scripts.forEach(function(el) {
                    if (el.name.toLowerCase().indexOf(filter) === 0) {
                        el.hidden = false;
                    } else {
                        el.hidden = true;
                    }
                });
            } else {
                scripts.forEach(function(el) {
                    el.hidden = false;
                });
            }
        },
        onChangeScriptsAll: function() {
            this.updateSelectDeselectAll('scripts_all', 'scripts');
            this.onChangeScripts();
        },
        onChangeScripts: function() {
            this.updateStyles();
            this.updateSubset();
            this.updateSwap();
        },
        onChangeWeightsAll: function() {
            this.updateSelectDeselectAll('weights_all', 'weight');
        },
        onChangeWidthsAll: function() {
            this.updateSelectDeselectAll('widths_all', 'width');
        },
        onChangeCharacterSubset: function() {
            this.updateSubset();
        },
        buildCommand: function() {
            command_options = []

            var name = this.options.name;
            if (name !== '') {
                name = utils.string.replace(name, ' ', '-');
                command_options.push('--name "' + name + '"');
            }

            var version = this.options.version;
            if (version !== '') {
                // name = utils.string.replace(name, ' ', '-');
                command_options.push('--version ' + version);
            }

            var output = this.options.output;
            if (output.length > 0) {
                command_options.push('--output ' + output.join(' '));
            }

            var scripts = this.options.scripts;
            if (scripts.length > 0) {
                command_options.push('--scripts ' + scripts.join(' '));
            }

            var constrast = this.options.contrast;
            if (constrast !== '') {
                command_options.push('--contrast ' + constrast);
            }

            var styles = this.options.styles;
            if (styles.length > 0) {
                command_options.push('--styles ' + styles.join(' '));
            }

            var weight = this.options.weight;
            if (weight.length > 0) {
                command_options.push('--weight ' + weight.join(' '));
            }

            var width = this.options.width;
            if (width.length > 0) {
                command_options.push('--width ' + width.join(' '));
            }

            var metrics_options = this.options.metrics;
            var metrics_ascender = Number(metrics_options.ascender);
            var metrics_descender = Number(metrics_options.descender);
            var metrics = [metrics_ascender, metrics_descender];
            if (!isNaN(metrics_ascender) && !isNaN(metrics_descender)) {
                if (metrics_ascender || metrics_descender) {
                    command_options.push('--metrics "' + metrics.join(' ') + '"');
                }
            }

            var hinted = this.options.hinted;
            if (hinted === true) {
                command_options.push('--hinted');
            }

            var ui = this.options.ui;
            if (ui === true) {
                command_options.push('--ui');
            }

            var subset = this.options.subset;
            var subsetValues = utils.array.clean(utils.object.values(subset), true);
            if (subsetValues.length > 0) {
                subsetValues.sort();
                command_options.push('--preset ' + subsetValues.join(' '));
            }

            var subset_chars = this.options.subset_chars;
            var subset_chars_list;
            if (subset_chars.length > 0) {
                subset_chars_list = subset_chars.split('');
                subset_chars_list = utils.array.unique(subset_chars_list);
                subset_chars_list = utils.array.remove(subset_chars_list, ' ')
                if (subset_chars_list.length > 0) {
                    subset_chars_list.sort();
                    subset_chars = subset_chars_list.join('');
                    subset_chars = utils.string.replace(subset_chars, '"', '\\"');
                    command_options.push('--subset "' + subset_chars + '"');
                }
            }

            var swapOptions = [];
            var swap_altIJ = this.options.swap_altIJ;
            var swap_figures = this.options.swap_figures;
            if (swap_altIJ === true) {
                swapOptions.push('altIJ');
            }
            if (swap_figures.length > 0) {
                swapOptions.push(swap_figures);
            }
            if (swapOptions.length > 0) {
                command_options.push('--swap ' + swapOptions.join(' '));
            }

            return 'python ~/notobuilderCLI.py ' + command_options.join(' ');
        },
        copyCommand: function() {
            var scope = this;
            var onCopySuccess = function() {
                // alert('Copied! :)');
                clearTimeout(scope.copyCommandDoneTimeout);
                scope.copyCommandDone = true;
                scope.copyCommandDoneTimeout = setTimeout(function() {
                    scope.copyCommandDone = false;
                }, 1500);
            };
            var onCopyError = function() {
                // alert('Copying error... :(');
            };
            Clipboard.copy(this.command, onCopySuccess, onCopyError);
        },
        updateCommand: function() {
            this.command = this.buildCommand();
            this.commandOk = (this.options.contrast !== '' && this.options.scripts.length > 0);
        }
    },
    mounted: function() {
        var indexList = utils.array.index;
        this.choicesIndexed.scriptsByValue = indexList(this.choices.scripts, 'value', true);
        this.choicesIndexed.stylesByName = indexList(this.choices.styles, 'name', true);
        this.choicesIndexed.subsetByName = indexList(this.choices.subset, 'name', true);
        this.ready = true;
    },
    updated: function() {
        this.updateCommand();
    }
});