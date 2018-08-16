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
            'type': 'CChart',
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
}]