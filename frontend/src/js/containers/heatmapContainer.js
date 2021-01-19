import React, { useEffect, useReducer, useCallback, useState } from 'react';
import heatmapReducer from '../reducers/heatmapReducer';
import MyHeatMap from '../components/heatmap/heatmap';
import { loadMapAction } from '../actions/heatmapAction';
import { Form, Input, Button } from 'antd';
import './heatmapContainer.scss';

export const HeatMapContainer = (props) => {
    let initialState = {
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
            }]
    }

    const [{ correlations_data }, dispatch] = useReducer(heatmapReducer, initialState);

    const mapCB = useCallback(() => {
        console.log('Step 2 - react call back fired');
        loadMapAction(dispatch);
    }, [dispatch])

    useEffect(() => {
        console.log('Step 1 - react use effect executed');
        mapCB();
    }, [mapCB]);

    const round = (value, decimals) => {
        return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
    }

    const getCorrelationsData = () => {
        let formatted_data = [];
        if (!correlations_data) {
            console.log("null correlations data")
            return formatted_data;
        }
        for (var i = 0; i < correlations_data.length; i++) {
            let correlation = correlations_data[i]["corr_value"];
            let correlationRounded = round(correlation, 3);
            formatted_data.push([correlations_data[i]["row_num"], correlations_data[i]["col_num"], correlationRounded]);
        }
        return formatted_data;
    }

    const getLabelsData = () => {
        let labels = [];
        if (!correlations_data) {
            console.log("null correlations data");
            return labels;
        }
        for (var i = 0; i < Math.sqrt(correlations_data.length); i++) {
            console.log(i);
            labels.push(correlations_data[i]["col_label"]);
        }
        return labels;
    }

    const [experiment_name, setexperiment_name] = useState("samplerun");

    const handleChangeExp = (event) => {
        console.log("handle change experiment");
        console.log(event.currentTarget.value);
        setexperiment_name(event.currentTarget.value);
    }

    const inputSave = () => {
        console.log("start submission");
        const submittedExp = experiment_name;
        console.log(submittedExp);
        console.log(dispatch);
        loadMapAction(dispatch, submittedExp);
    }

    return (
        <div>
            <div className={props.dynamicClass}>
                <Form>
                    <Form.Item label="Look Up Heatmap Results By Unique Job ID" name="experiment_name">
                        <Input value={experiment_name} onChange={handleChangeExp}></Input>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" onClick={inputSave}>Submit</Button>
                    </Form.Item>
                </Form>
            </div>
            <MyHeatMap correlations={getCorrelationsData()} labels={getLabelsData()}></MyHeatMap>
        </div>
    )
}
