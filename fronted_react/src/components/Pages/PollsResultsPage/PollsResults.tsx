import React, { Key, ReactNode, useLayoutEffect } from 'react';
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
import { serverPath, wrap64ForSend } from '../../../app-constants';
import useToken from '../../../useToken';

const theme = createTheme();
async function getAnswersHistogram(credentials: any) {
    //Simple POST request with a JSON body using fetch
    let recived: any = "Server Error";
    let connection: boolean = true;
    let was_error: boolean = false;
    const requestOptions1 = {
        method: 'POST',
        body: JSON.stringify(credentials)
    };
    try {
        var response = await fetch(`${serverPath}/get_poll_answers`, requestOptions1);
        var response_json = await response.json();
        console.log(response_json);
        if (!response_json.hasOwnProperty("message_back")) {
            if (!response_json.hasOwnProperty("error")) {
                return { connection, recived };
            }
            recived = response_json['error'];
            was_error = true;
            return { connection, was_error, recived };
        }
        recived = response_json['message_back'];
    } catch (e) {
        console.log(e);
        connection = false;
        console.log('error connection');
        alert('Connection Error - Please check your internet connection');
        //console.error(e);
    }

    return { connection, was_error, recived };
}




export const PollsResults = () => {
    localStorage.setItem('pageAuth', '5');
    const [firstresultsBool, setfirstResultsBoll] = React.useState(false);
    const [fetchingData, setFetchingData] = React.useState(true);
    const [firstSelected, setfirstSelected] = React.useState(false);
    interface Dict {
        question: ReactNode;
        q_id: string;
    }
    const [questionData, setquestionData] = React.useState<Dict[]>();
    const { token, setToken } = useToken();

    // const myQuestions = [
    //     { q_id: 0, question: 'How are you?' },
    //     { q_id: 1, question: 'How old are you?' },
    //     { q_id: 2, question: 'Where are you from?' },
    // ]
    //get data for filter
    React.useEffect(() => {
        let isSubscribed = true;
        const fetchFilter = async (credentials: any) => {

            //Simple POST request with a JSON body using fetch
            var fetchedData;
            let connection: boolean = true;

            const requestOptions1 = {

                method: 'POST',
                body: JSON.stringify(credentials)
            };
            try {
                var response = await fetch(`${serverPath}/get_associated_polls`, requestOptions1);
                var response_json = await response.json();

                if (response_json.hasOwnProperty('result_lst')) {
                    fetchedData = response_json['result_lst'];
                    // setFetching is false here

                }
                else {
                    console.log(response_json['error']);
                }

            } catch (e) {
                connection = false;
                console.error('connection error ');
                alert('Connection Error - Please check your internet connection');
                //console.error(e);
            }
            if (connection === false) {
                return;
            }
            const editDataToViewQuestions = (fetchedData: any) => {
                var fetchedLst = [];
                if (fetchedData) {
                    for (let i = 0; i < fetchedData.length; i++) {
                        var currDict = {
                            q_id: `${fetchedData[i]['id_poll']}`,
                            question: `${fetchedData[i]['poll_content']}    - Was asked at ${fetchedData[i]['date']}`,
                        };
                        fetchedLst.push(currDict)
                        if (i === 0) {
                            setQuestionID(fetchedData[i]['id_poll']);
                        }
                    }
                }
                console.log(fetchedLst);
                setFetchingData(false);
                setquestionData(fetchedLst);
                return fetchedLst;

            };
            editDataToViewQuestions(fetchedData);
        }
        fetchFilter({
            token: wrap64ForSend(token)
        }).catch(console.error);
        setFetchingData(false)
    }, [])
    let FIRSTRESULTS = [
        { Answer: 'NO RESULTS', Votes: 0 },
    ]

    const [results, setResults] = React.useState(FIRSTRESULTS);
    
    const [questionID, setQuestionID] = React.useState(0);

    useLayoutEffect(() => {
        // Pie Chart - instantiating 
        if (firstSelected) {
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
        }
    }, [results]);



    const handleChange = async (event: any) => {
        setQuestionID(event.target.value);
        console.log('id poll num:');
        console.log(event.target.value);
        console.log(questionID);
        if (questionData && !fetchingData) {
            var id_poll = event.target.value;
            //get answers
            const { connection, was_error, recived } = await getAnswersHistogram({
                token: wrap64ForSend(token),
                id_poll: id_poll,
            });
            if (connection === false) {
                return;
            }
            if (was_error === true) {
                return;
            }
            setfirstSelected(true);
            // answers have returned
            setResults(recived);
            setfirstResultsBoll(true);

        }
        // if (event.target.value === 0){
        //     setResults(zero_answer);
        // }
        // if (event.target.value === 1){
        //     setResults(one_answer);
        // }
        // if (event.target.value === 2){
        //     setResults(two_answer);
        // }
    };

    return (
        <ThemeProvider theme={theme}>
            <h1> Polls Results </h1>
            <Typography component="h1" variant="h6">
                Select a poll for view its results
            </Typography>
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

                            {questionData && !fetchingData ?
                                questionData.map(question => {
                                    console.log(question);
                                    return (
                                        <MenuItem key={question.q_id} value={question.q_id}>
                                            {question.question}
                                        </MenuItem>
                                    )
                                })
                                :
                                <Typography component="h1" variant="h6">
                                    Loading...
                                </Typography>

                            }
                        </Select>
                    </FormControl>
                </Box>
                <br></br>
                {firstresultsBool ?
                    <div className='poll_in_numbers'>
                        <h1>Polls Results in Numbers</h1>
                        <div className="user-list">
                            {results && results.length > 0 ? (
                                results.map((result) => (
                                    <li key={result.Answer} className="user">
                                        <span className="user-name">{result.Answer} : </span>
                                        <span className="user-name">{result.Votes} users voted this answer</span>
                                    </li>
                                ))
                            ) : (
                                <h1>No results found!</h1>
                            )}
                        </div>
                    </div>
                    :
                    <br></br>
                }
                <br></br>
                <div id="chartdiv" style={{ width: "100%", height: "500px" }}></div>

            </Container>
        </ThemeProvider>
    );
}
