import React, { useLayoutEffect } from 'react';
import '../../../App.css';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import * as am5 from "@amcharts/amcharts5";
import * as am5percent from "@amcharts/amcharts5/percent";

const theme = createTheme();

export const PollsResults = () => {

    const myQuestions = [
        {q_id: 0, question: 'How are you?'},
        {q_id: 1, question: 'How old are you?'},
        {q_id: 2, question: 'Where are you from?'},
    ]
    
    const zero_answer = [
        {
            Answer: "answer 1",
            Votes: 100
        },
        {
            Answer: "answer 2",
            Votes: 200
        },
        {
            Answer: "answer 3",
            Votes: 300
        }
    ]

    const one_answer = [
        {
            Answer: "answer 4",
            Votes: 400
        },
        {
            Answer: "answer 5",
            Votes: 500
        },
        {
            Answer: "answer 6",
            Votes: 600
        }
    ]

    const two_answer = [
        {
            Answer: "answer 7",
            Votes: 700
        },
        {
            Answer: "answer 8",
            Votes: 800
        },
        {
            Answer: "answer 9",
            Votes: 900
        }
    ]

    const [results, setResults] = React.useState(zero_answer);
    const [questionID, setQuestionID] = React.useState(0);

    useLayoutEffect(() => {
        // Pie Chart - instantiating 
        let root = am5.Root.new("chartdiv");
        let chart = root.container.children.push(
        am5percent.PieChart.new(root, {})
        );

        // Pie Chart - add series 
        let series = chart.series.push(
            am5percent.PieSeries.new(root, {
            name: "Series",
            categoryField: "Answer",
            valueField: "Votes"
            })
        );
        
        // Add legend
        let legend = chart.children.push(am5.Legend.new(root, {
            centerX: am5.percent(50),
            x: am5.percent(50),
            layout: root.horizontalLayout
        }));

        // Pie Chart - setting data
        series.data.setAll(results)
        legend.data.setAll(series.dataItems);
        
        series.appear();
        chart.appear();
    
        return () => {
          root.dispose();
        };
    }, [results]);

    const handleChange = (event:any) => {
        setQuestionID(event.target.value);

        if (event.target.value === 0){
            setResults(zero_answer);
        }
        if (event.target.value === 1){
            setResults(one_answer);
        }
        if (event.target.value === 2){
            setResults(two_answer);
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <h1> Polls Results </h1>
            <Typography component="h1" variant="h6">
                Select a poll for view its results
            </Typography>
            <br></br>
            <Container component="main" maxWidth="md">
                <Box sx={{ minWidth: 120 }}>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Question</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={questionID}
                            label="Question"
                            onChange={handleChange}
                            >
                            {myQuestions.map(question => {
                                    return (
                                        <MenuItem key={question.q_id} value={question.q_id}>
                                            {question.question}
                                        </MenuItem>
                                    )
                                })
                            }
                        </Select>
                    </FormControl>
                </Box>
                <br></br>
                <br></br>
                <div id="chartdiv" style={{ width: "100%", height: "500px" }}></div>
            </Container>
        </ThemeProvider>
    );
}
