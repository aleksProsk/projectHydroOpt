d = [
{
    'output': {
        'object': 'hydroplantTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'reservoirInputTypeDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateSecondColumn',
},
{
    'output': {
        'object': 'performanceSettingsDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'performanceSettingsDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updatePerformanceSettings',
},
{
    'output': {
        'object': 'reservoirInputTypeDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'reservoirInputTypeDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateInputType',
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
        'object': 'hydroplantTable',
        'param': 'editable',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'hydroplantTable',
            'param': 'rows',
            'type': 'CDataTable',
        },
    ],
    'callback': 'updateReservoirParameters',
},
]