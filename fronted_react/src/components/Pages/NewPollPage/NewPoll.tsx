import React, { useState } from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import 'antd/dist/antd.css';
import { Table } from 'antd';
import { styled } from '@mui/styles';

const theme = createTheme();

const MyTextField = styled(TextField)({
    background: 'linear-gradient(45deg, #b3e5fc 10%, white 100%)',
});

export const NewPoll = () => {

    // Question + Answers
    const [answersList, setAnswersList] = useState([{ answer: "" }]);

    const handleAnswersInputChange = (e:any, index:any) => {
        const value = e.target.value;
        const list = [...answersList];
        list[index] = value;
        setAnswersList(list);
    };

    function handleAnswersRemoveClick(index: string) {
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

    const data = [
        {
            key: '0',
            data: 'How are you?',
            children: [
                {
                    key: '0_0',
                    data: 'Good',
                },
                {
                    key: '0_1',
                    data: 'Bad',
                },
                {
                    key: '0_2',
                    data: 'Not bad',
                },
                {
                    key: '0_3',
                    data: 'Perfect',
                },
            ],
        },
        {
            key: 1,
            data: 'How old are you?',
            children: [
                {
                    key: '1_0',
                    data: '0-10',
                },
                {
                    key: '1_1',
                    data: '10-15',
                },
                {
                    key: '1_2',
                    data: '15-20',
                },
                {
                    key: '1_3',
                    data: '20-25',
                },
                {
                    key: '1_4',
                    data: '25-30',
                },
                {
                    key: '1_5',
                    data: '30-40',
                },
            ],
        },
    ];

    const [filterList, setFilterList] = useState([{ key: "", data: "" }]);

    // rowSelection objects indicates the need for row selection
    const rowSelection = {
        onChange: (selectedRowKeys:any, selectedRows:any) => {
            console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
            setFilterList(selectedRowKeys);
        },
        onSelect: (record:any, selected:any, selectedRows:any) => {
            console.log(record, selected, selectedRows);
            setFilterList(selected);
        },
        onSelectAll: (selected:any, selectedRows:any, changeRows:any) => {
            console.log(selected, selectedRows, changeRows);
            setFilterList(selected);
        },
    };

    const checkStrictly = false;

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        // eslint-disable-next-line no-console
        console.log({
            Question: data.get('question'),
            Answers: [data.get('answer1'), ...answersList],
            Filter: filterList
        });
        alert("The poll has been successfully submitted!")
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
                        <MyTextField
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
                        <MyTextField
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
                                <MyTextField
                                    margin="normal"
                                    required
                                    fullWidth
                                    name='answer'
                                    label='Answer'
                                    type="answer"
                                    id="answer"
                                    autoComplete="current-answer"
                                    value={x.answer}
                                    onChange={e => handleAnswersInputChange(e, i)}
                                />
                                <div className="answers-box">
                                    {answersList.length !== 1 && <button className='add-remove-button' onClick={() => handleAnswersRemoveClick(i.toString())}>-</button>}
                                    {answersList.length - 1 === i && <button className='add-remove-button' onClick={handleAnswersAddClick}>+</button>}
                                </div>
                            </div>
                        );
                        })}
                        <Typography component="h5" variant="h6">
                        <br></br>
                            Filter relevant targets according to previous answers
                        </Typography>
                        <br></br>
                        <>
                            <Table 
                                columns={columns}
                                rowSelection={{ ...rowSelection, checkStrictly }}
                                dataSource={data}
                            />
                        </>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 4, mb: 2 }}
                        >
                            Submit
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
    }
