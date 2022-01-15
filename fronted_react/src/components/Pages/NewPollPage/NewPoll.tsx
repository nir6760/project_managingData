import React, { useLayoutEffect, useState } from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import 'antd/dist/antd.css';
import { Table } from 'antd';
import { serverPath, wrap64ForSend } from '../../../app-constants';
import useToken from '../../../useToken';
import { useEffect } from 'react';
import ListBody from 'antd/lib/transfer/ListBody';
import ReactDOM from 'react-dom';
import _ from 'lodash';

import {  FormControl, FormControlLabel, FormLabel, Radio, RadioGroup } from '@mui/material';

async function sendPoll(credentials: any) {
    //Simple POST request with a JSON body using fetch
    let recived: string = "Server Error";
    let connection: boolean = true;

    const requestOptions1 = {
        method: 'POST',
        body: JSON.stringify(credentials)
    };
    try {
        var response = await fetch(`${serverPath}/register_and_send_poll`, requestOptions1);
        var response_json = await response.json();
        console.log(response_json);
        if (!response_json.hasOwnProperty("message_back")) {
            if (!response_json.hasOwnProperty("error")) {
                return { connection, recived };
            }
            recived = response_json['error'];
            return { connection, recived };
        }
        recived = response_json['message_back'];
    } catch (e) {
        console.log(e);
        connection = false;
        console.log('error connection');
        alert('Connection Error - Please check your internet connection');
        //console.error(e);
    }

    return { connection, recived };
}
const theme = createTheme();



export interface TableElementProps {
    columns: any;
    rowSelection: any;
    checkStrictly: any;
    data: any;
}

export const TableElement: React.FC<TableElementProps> = ({
    columns,
    rowSelection,
    checkStrictly,
    data,
}) => {
    return <Table
        columns={columns}
        rowSelection={{ ...rowSelection, checkStrictly }}
        dataSource={data} />;
}

export const NewPoll = () => {
    localStorage.setItem('pageAuth', '4');
    const [fetchingData, setFetchingData] = React.useState(true);
    interface Dict {
    }
    const [filterData, setfilterData] = React.useState<Dict[]>();
    const { token, setToken } = useToken();
    const [checkUnion, setcheckUnion] = React.useState(true);

    // Question + Answers
    const [answersList, setAnswersList] = useState([{ answer: "" }]);

    const handleAnswersInputChange = (e: any, index: any) => {
        const value = e.target.value;
        const list = [...answersList];
        list[index] = value;
        setAnswersList(list);
    };

    function handleAnswersRemoveClick(index: string) {
        console.log('index is' + index);
        const list = [...answersList];
        list.splice(+index, 1);
        setAnswersList(list);
    }

    const handleAnswersAddClick = () => {
        setAnswersList([...answersList, { answer: "" }]);
    };
    // Filters
    const columns = [
        {
            title: "Questions and Answers",
            dataIndex: "data",
            key: "data"
        },
    ];

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
            const editDataToViewFilter = (fetchedData: any) => {
                var fetchedLst = [];
                if (fetchedData) {


                    for (let i = 0; i < fetchedData.length; i++) {
                        var currChildrenLst = [];
                        for (let j = 0; j < fetchedData[i]['numbers_answers_lst'].length; j++) {
                            currChildrenLst.push({
                                key: `${fetchedData[i]['id_poll']}_${j}`,
                                data: fetchedData[i]['numbers_answers_lst'][j],
                            });
                        }

                        fetchedLst.push({
                            key: `${fetchedData[i]['id_poll']}`,
                            data: fetchedData[i]['poll_content'],
                            children: currChildrenLst
                        })
                    }
                }
                console.log(fetchedLst);
                setFetchingData(false);
                setfilterData(fetchedLst);
                return fetchedLst;

            };
            console.log('fetchedData');
            console.log(fetchedData);
            editDataToViewFilter(fetchedData);
            console.log('old vs new');
            // if (isSubscribed) {
            //     //data = editDataToViewFilter(fetchedData);

            //     //console.log(data);
            //     //ReactDOM.render(<TableElement columns={columns} rowSelection={rowSelection} checkStrictly={checkStrictly} data={data} />, document.getElementById('filter_table_div'));

            // }

        }
        fetchFilter({
            token: wrap64ForSend(token)
        }).catch(console.error);
        setFetchingData(false)
    }, [])



    const [filterList, setFilterList] = useState([{ key: "", data: "" }]);

    // rowSelection objects indicates the need for row selection
    const rowSelection = {
        onChange: (selectedRowKeys: any, selectedRows: any) => {
            console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
            setFilterList(selectedRowKeys);
        },
        onSelect: (record: any, selected: any, selectedRows: any) => {
            console.log(record, selected, selectedRows);
            setFilterList(selected);
        },
        onSelectAll: (selected: any, selectedRows: any, changeRows: any) => {
            console.log(selected, selectedRows, changeRows);
            setFilterList(selected);
        },
    };

    const checkStrictly = false;

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        // eslint-disable-next-line no-console
        let question: FormDataEntryValue | null = data.get('question');
        let answer1: any = data.get('answer1');
        let answers: any = [data.get('answer1'), ...answersList];
        let filter: any = filterList;
        console.log({
            Question: question,
            Answers: answers,
            Filter: filter
        });
        if (question === "" || answers.length < 2) {
            alert('All poll detailes must not be empty');
            return;
        }
        let choicesHist: any = {}
        for (let j = 0; j < answers.length; j++) {
            const currCheck = answers[j];
            if (!_.isString(currCheck) || currCheck === "") {
                alert('All poll answers can\'t be empty and must be unique, with least 2 possible choices');
                return;
            }
            if (choicesHist.hasOwnProperty(`${currCheck}`)) {
                alert('All poll answers can\'t be empty, with least 2 unique choices');
                return;
            } else {
                choicesHist[currCheck] = (choicesHist[currCheck] || 0) + 1;

            }

        }

        //login user
        const { connection, recived } = await sendPoll({
            token: wrap64ForSend(token),
            poll_content: data.get('question'),
            numbers_choices_lst: [data.get('answer1'), ...answersList],
            idPoll_answer_lst: filterList,
            should_union: checkUnion
        });
        if (connection === false) {
            return;
        }
        else {
            alert(recived);
        }

    };
    const handleOnChangeRadio = (e: any) => {
        if (e.target.value === 'union') {
            setcheckUnion(true);
        }
        else {
            setcheckUnion(false);
        }

    };
    return (
        <ThemeProvider theme={theme}>
            <h1> New Poll </h1>
            <Container component="main" maxWidth="md">
                <Box
                    sx={{
                        marginTop: 1,
                        marginBottom: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <Typography component="h5" variant="h6">
                            Add a question
                        </Typography>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="question"
                            label="Question"
                            name="question"
                            autoComplete="question"
                            autoFocus
                        />
                        <Typography component="h5" variant="h6">
                            <br></br>
                            Add possible answers
                        </Typography>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name='answer1'
                            label="Answer"
                            type="answer"
                            id="answer"
                            autoComplete="current-answer"
                        />
                        {answersList.map((x, i) => {
                            return (
                                <div className="answers-box">
                                    <TextField
                                        margin="normal"
                                        required
                                        fullWidth
                                        name='answer'
                                        label=''
                                        type="answer"
                                        id="answer"
                                        autoComplete="current-answer"
                                        value={x.answer}
                                        onChange={e => handleAnswersInputChange(e, i)}
                                    />
                                    <div className="answers-box">
                                        {answersList.length !== 1 && <Button  className='add-remove-button' onClick={() => handleAnswersRemoveClick(i.toString())}>Remove</Button>}
                                        {answersList.length - 1 === i && <Button className='add-remove-button' onClick={handleAnswersAddClick}>Add</Button>}
                                    </div>
                                </div>
                            );
                        })}
                        <Typography component="h5" variant="h6">
                            <br></br>
                            Filter relevant targets according to previous answers
                        </Typography>
                        <br></br>
                        <div id='filter_table_div'>
                            <>
                                {filterData && !fetchingData ?
                                    <Table
                                        columns={columns}
                                        rowSelection={{ ...rowSelection, checkStrictly }}
                                        dataSource={filterData} />
                                    :
                                    <Typography component="h1" variant="h6">
                                        Loading...
                                    </Typography>
                                }
                                {/* <TableElement columns={columns} rowSelection={rowSelection} checkStrictly={checkStrictly} data={data} /> */}
                            </>
                        </div>
                        {/* <FormGroup>
                            <FormControlLabel control={<Checkbox defaultChecked onChange={handleOnChangeRadio} />}
                                label="Check for union (OR Condition)" />
                        </FormGroup> */}
                        <FormControl component="fieldset">
                            <FormLabel component="legend">Union (OR Condition)
                                \
                                Intersection query (AND Condition)</FormLabel>
                            <RadioGroup
                                aria-label="Union / Intersection query"
                                name="controlled-radio-buttons-group"
                                defaultValue={"union"}

                            >
                                <FormControlLabel value="union" control={<Radio />} label="Union" onChange={handleOnChangeRadio} />
                                <FormControlLabel value="intersect" control={<Radio />} label="Intersection" onChange={handleOnChangeRadio} />
                            </RadioGroup>
                        </FormControl>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 4, mb: 2 }}
                        >
                            Send To Mailing List
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}
