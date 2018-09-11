d = [
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
        'object': 'scenarioSettingsUseDropdown',
        'param': 'placeholder',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'scenarioSettingsUseDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'callback': 'updateScenarioSettings',
},
{
    'output': {
        'object': 'scenarioSettingsInput',
        'param': 'placeholder',
        'type': 'CInput',
    },
    'input': [
        {
            'object': 'scenarioSettingsInput',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'callback': 'updateNScenarios',
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