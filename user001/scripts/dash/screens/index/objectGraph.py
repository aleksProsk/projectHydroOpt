d = [
{
    'output': {
        'object': 'myGraphModal',
        'param': 'style',
        'type': 'CModal',
    },
    'input': [
        {
            'object': 'revenueAndRiskOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentPowerOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'powerPlanningOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentReservoirLevelOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'marginPriceOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'reservoirCycleOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'energyPlanningPeakOpen',
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
            'object': 'revenueAndRiskTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentPowerTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'powerPlanningTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentReservoirLevelTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'marginPriceTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'reservoirCycleTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'energyPlanningPeakTable',
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
            'object': 'revenueAndRiskOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentPowerOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'powerPlanningOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentReservoirLevelOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'marginPriceOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'reservoirCycleOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'energyPlanningPeakOpen',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'state': [
        {
            'object': 'revenueAndRiskGraphFigure',
            'param': 'figure',
            'type': 'CHist',
        },
        {
            'object': 'currentPowerGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
        {
            'object': 'powerPlanningGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
        {
            'object': 'currentReservoirLevelGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
        {
            'object': 'marginPriceGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
        {
            'object': 'reservoirCycleGraphFigure',
            'param': 'figure',
            'type': 'CChart',
        },
        {
            'object': 'energyPlanningPeakGraphFigure',
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
            'object': 'revenueAndRiskTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentPowerTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'powerPlanningTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'currentReservoirLevelTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'marginPriceTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'reservoirCycleTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'energyPlanningPeakTable',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'buildModalTable',
},
{
    'output': {
        'object': 'revenueAndRiskGraphFigure',
        'param': 'figure',
        'type': 'CHist',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderRevenueAndRiskGraphFigure',
},
{
    'output': {
        'object': 'startDate',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderStartDate',
},
{
    'output': {
        'object': 'endDate',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderEndDate',
},
{
    'output': {
        'object': 'averageRevenue',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderAverageRevenue',
},
{
    'output': {
        'object': 'minimumRevenue',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderMinimumRevenue',
},
{
    'output': {
        'object': 'displayDropdown',
        'param': 'style',
        'type': 'CDropdown',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },
    ],
    'state': [
        {
            'object': 'displayDropdown',
            'param': 'style',
            'type': 'CDropdown',
        }
    ],
    'callback': 'updateChecked',
},
{
    'output': {
        'object': 'marginPriceGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderMarginPriceGraphFigure',
},
{
    'output': {
        'object': 'currentPowerGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderCurrentPowerGraphFigure',
},
{
    'output': {
        'object': 'currentReservoirLevelGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderCurrentReservoirLevelGraphFigure',
},
{
    'output': {
        'object': 'energyPlanningPeakGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderEnergyPlanningPeakGraphFigure',
},
{
    'output': {
        'object': 'powerPlanningGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderPowerPlanningGraphFigure',
},
{
    'output': {
        'object': 'reservoirCycleGraphFigure',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'displayDropdown',
            'param': 'value',
            'type': 'CDropdown',
        },

    ],
    'callback': 'renderReservoirCycleGraphFigure',
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
}]