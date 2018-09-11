d = [
{
    'output': {
        'object': 'aggregatedDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'aggregatedDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateAggregated',
},
{
    'output': {
        'object': 'moduleSelectorDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'moduleSelectorDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateModuleSelector',
},
{
    'output': {
        'object': 'fileFormatDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'fileFormatDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateFileFormat',
},
{
    'output': {
        'object': 'resolutionMeanResultsDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'resolutionMeanResultsDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateResolutionMeanResults',
},
{
    'output': {
        'object': 'timeSeriesDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'timeSeriesDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateTimeSeries',
},
{
    'output': {
        'object': 'resultsPerScenarioDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'resultsPerScenarioDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateResultsPerScenario',
},
{
    'output': {
        'object': 'unitDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'unitDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateUnit',
},
{
    'output': {
        'object': 'formatDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'formatDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'updateFormat',
},
{
    'output': {
        'object': 'datePicker',
        'param': 'is_RTL',
        'type': 'CDatePickerRange',
    },
    'input': [
        {
            'object': 'datePicker',
            'param': 'start_date',
            'type': 'CDatePickerRange',
        },
        {
            'object': 'datePicker',
            'param': 'end_date',
            'type': 'CDatePickerRange',
        },
    ],
    'callback': 'updateDatePicker',
},
{
    'output': {
        'object': 'timeSeriesDropdown',
        'param': 'options',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'aggregatedDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'fileFormatDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateTimeSeriesOptions',
},
{
    'output': {
        'object': 'timeSeriesDropdown',
        'param': 'value',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'timeSeriesDropdown',
            'param': 'options',
            'type': 'CDropdown',
        },
    ],
    'state': [
        {
            'object': 'timeSeriesDropdown',
            'param': 'value',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateDropdownValue',
},
{
    'output': {
        'object': 'resultsPerScenarioDropdown',
        'param': 'options',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'aggregatedDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'fileFormatDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateResultsPerScenarioOptions',
},
{
    'output': {
        'object': 'resultsPerScenarioDropdown',
        'param': 'value',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'resultsPerScenarioDropdown',
            'param': 'options',
            'type': 'CDropdown',
        },
    ],
    'state': [
        {
            'object': 'resultsPerScenarioDropdown',
            'param': 'value',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateDropdownValue',
},
{
    'output': {
        'object': 'assetsChecklist',
        'param': 'className',
        'type': 'CChecklist',
    },
    'input': [
        {
            'object': 'assetsChecklist',
            'param': 'values',
            'type': 'CChecklist',
        },
    ],
    'callback': 'updateExportCheck',
},
{
    'output': {
        'object': 'exportButton',
        'param': 'className',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'exportButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'export',
},
{
    'output': {
        'object': 'folderInput',
        'param': 'placeholder',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'folderInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'callback': 'updateFolderName',
},
{
    'output': {
        'object': 'fileInput',
        'param': 'editable',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'fileInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'callback': 'updateFileName',
},
]