d = [
{
    'output': {
        'object': 'priceChart',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'forwardCurveInput',
            'param': 'value',
            'type': 'CInput',
        },
        {
            'object': 'displayDatePicker',
            'param': 'start_date',
            'type': 'CDatePickerRange',
        },
        {
            'object': 'displayDatePicker',
            'param': 'end_date',
            'type': 'CDatePickerRange',
        },
    ],
    'callback': 'renderPriceChart',
},
{
    'output': {
        'object': 'numberDropdown',
        'param': 'options',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'newButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'updateNumberDropdownButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'copyButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'removeButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'state': [
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        },
        {
            'object': 'shortNameInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'callback': 'addNewAsset',
},
{
    'output': {
        'object': 'numberDropdown',
        'param': 'value',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        },
        {
            'object': 'updateNumberDropdownButton',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'changeDropdownValue',
},
{
    'output': {
        'object': 'nameInput',
        'param': 'value',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'changeName',
},
{
    'output': {
        'object': 'shortNameInput',
        'param': 'value',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'changeShortName',
},
{
    'output': {
        'object': 'assetTypeDropdown',
        'param': 'value',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'changeAssetType',
},
{
    'output': {
        'object': 'nameInput',
        'param': 'placeholder',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'nameInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'state': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateName',
},
{
    'output': {
        'object': 'shortNameInput',
        'param': 'placeholder',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'shortNameInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'state': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateShortName',
},
{
    'output': {
        'object': 'assetTypeDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'assetTypeDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'state': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateAssetType',
},
{
    'output': {
        'object': 'myGraphModal',
        'param': 'style',
        'type': 'CModal',
    },
    'input': [
        {
            'object': 'chartOpen',
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
            'object': 'chartTable',
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
            'object': 'chartOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'state': [
        {
            'object': 'priceChart',
            'param': 'figure',
            'type': 'CChart',
        },
    ],
    'callback': 'buildModalGraph',
},
{
    'output': {
        'object': 'modalTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'chartTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'buildModalTable',
},
{
    'output': {
        'object': 'mainMap',
        'param': 'children',
        'type': 'CYMap',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'options',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateMap',
},
{
    'output': {
        'object': 'defineButton',
        'param': 'href',
        'type': 'CButton',
    },
    'input': [
        {
            'object': 'numberDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateTopologyLink',
},
]