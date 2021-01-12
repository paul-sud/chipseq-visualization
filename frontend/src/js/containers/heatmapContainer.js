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
                "experimentName": "test9",
                "rowNum": 0,
                "colNum": 0,
                "rowLabel": "ENCFF017NXL.bed.gz",
                "colLabel": "ENCFF017NXL.bed.gz",
                "corrValue": 1
            },
            {
                "experimentName": "test9",
                "rowNum": 0,
                "colNum": 1,
                "rowLabel": "ENCFF017NXL.bed.gz",
                "colLabel": "ENCFF071XMA.bed.gz",
                "corrValue": 0.401480573670878
            },
            {
                "experimentName": "test9",
                "rowNum": 0,
                "colNum": 2,
                "rowLabel": "ENCFF017NXL.bed.gz",
                "colLabel": "ENCFF106NXV.bed.gz",
                "corrValue": 0.653801541642514
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
            let correlation = correlations_data[i]["corrValue"];
            let correlationRounded = round(correlation, 3);
            formatted_data.push([correlations_data[i]["rowNum"], correlations_data[i]["colNum"], correlationRounded]);
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
            labels.push(correlations_data[i]["colLabel"]);
        }
        return labels;
    }

    const [experimentName, setExperimentName] = useState("samplerun");

    const handleChangeExp = (event) => {
        console.log("handle change experiment");
        console.log(event.currentTarget.value);
        setExperimentName(event.currentTarget.value);
    }

    const inputSave = () => {
        console.log("start submission");
        const submittedExp = experimentName;
        console.log(submittedExp);
        console.log(dispatch);
        loadMapAction(dispatch, submittedExp);
    }

    return (
        <div>
            <div className={props.dynamicClass}>
                <Form>
                    <Form.Item label="Look Up Heatmap Results By Unique Job ID" name="experimentName">
                        <Input value={experimentName} onChange={handleChangeExp}></Input>
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
