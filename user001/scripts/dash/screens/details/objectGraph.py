d = [
{
    'output': {
        'object': 'calcParametersTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'state': [
        {
            'object': 'hiddenText',
            'param': 'children',
            'type': 'CText',
        }
    ],
    'callback': 'updateCalcParametersTable',
},
{
    'output': {
        'object': 'resultGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'summaryTurbines',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryPumps',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryReservoirs',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryLosses',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryRevenues',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryPrices',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'summaryInflows',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'hiddenButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'state': [
        {
            'object': 'hiddenText',
            'param': 'children',
            'type': 'CText',
        }
    ],
    'callback': 'updateResultGraph',
},
{
    'output': {
        'object': 'summaryTurbines',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'turbinesButton',
},
{
    'output': {
        'object': 'summaryRevenues',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'revenuesButton',
},
{
    'output': {
        'object': 'summaryPumps',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'pumpsButton',
},
{
    'output': {
        'object': 'summaryPrices',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'pricesButton',
},
{
    'output': {
        'object': 'summaryLosses',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'lossesButton',
},
{
    'output': {
        'object': 'summaryInflows',
        'param': 'style',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'inflowsButton',
},
{
    'output': {
        'object': 'myGraphModal',
        'param': 'style',
        'type': 'CModal',
    },
    'input': [
        {
            'object': 'resultOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'modalCloser',
            'param': 'n_clicks',
            'type': 'CText',
        },
    ],
    'state': [
        {
            'object': 'myGraphModal',
            'param': 'style',
            'type': 'CModal',
        },
    ],
    'callback': 'loadModal',
},
{
    'output': {
        'object': 'myTableModal',
        'param': 'style',
        'type': 'CModal',
    },
    'input': [
        {
            'object': 'resultTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'modalCloser1',
            'param': 'n_clicks',
            'type': 'CText',
        },
    ],
    'state': [
        {
            'object': 'myTableModal',
            'param': 'style',
            'type': 'CModal',
        },
    ],
    'callback': 'loadModal1',
},
{
    'output': {
        'object': 'modalGraph',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'resultOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'state': [
        {
            'object': 'resultGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'callback': 'buildModalGraph',
},
{
    'output': {
        'object': 'text1',
        'param': 'style',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'resultGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'state': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'drawText1',
},
{
    'output': {
        'object': 'text1',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'resultGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'state': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'hiddenText',
            'param': 'children',
            'type': 'CText',
        },
    ],
    'callback': 'buildText1',
},
{
    'output': {
        'object': 'text2',
        'param': 'style',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'resultGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'state': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'drawText2',
},
{
    'output': {
        'object': 'text2',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'resultGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'state': [
        {
            'object': 'resultsSelectionDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'hiddenText',
            'param': 'children',
            'type': 'CText',
        },
    ],
    'callback': 'buildText2',
},
{
    'output': {
        'object': 'saveButton',
        'param': 'href',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'modalTable',
            'param': 'rows',
            'type': 'CDataTable',
        },

    ],
    'callback': 'buildLink',
},
{
    'output': {
        'object': 'modalTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'resultTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'buildModalTable',
},
]