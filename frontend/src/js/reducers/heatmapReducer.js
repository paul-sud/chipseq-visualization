let initStore = {
    loading: false,
    error: false,
    correlations_data: [
        {
            "experiment_name": "test9",
            "row_num": 0,
            "col_num": 0,
            "row_label": "ENCFF017NXL.bed.gz",
            "col_label": "ENCFF017NXL.bed.gz",
            "corr_value": 1
        },
        {
            "experiment_name": "test9",
            "row_num": 0,
            "col_num": 1,
            "row_label": "ENCFF017NXL.bed.gz",
            "col_label": "ENCFF071XMA.bed.gz",
            "corr_value": 0.401480573670878
        },
        {
            "experiment_name": "test9",
            "row_num": 0,
            "col_num": 2,
            "row_label": "ENCFF017NXL.bed.gz",
            "col_label": "ENCFF106NXV.bed.gz",
            "corr_value": 0.653801541642514
        }
    ]
}

export default (state = initStore, action) => {
    switch (action.type) {
        case "correlations_success":
            return {...state, loading: false, correlations_data: action.payload.correlations_data}
        case "correlations_begin":
            return {...state, loading: true}
        case "correlations_error":
            return {...state, error: true}
        default:
            return {...state, loading: true}
    }
}
