import useSWR from 'swr'
import axios from 'axios';
import './App.css'
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {Fragment} from "react";

function App() {
    const {data, isLoading} = useSWR('http://localhost:8000/api/schedules/2/', axios)

    if (isLoading) return 'Загрузка...'

    const schedule = data.data.content

    return (
        <TableContainer component={Paper}>
            <Table stickyHeader borderAxis="both">
                <TableHead>
                    <TableRow>
                        <TableCell rowSpan={2}>
                            День недели
                        </TableCell>
                        <TableCell rowSpan={2}>
                            Пара
                        </TableCell>
                        <TableCell rowSpan={2}>
                            Время начала
                        </TableCell>
                        {schedule.weekdays.monday.map(group => (
                            <TableCell key={group.group_name} colSpan={3}>
                                {group.group_name}
                            </TableCell>
                        ))}
                    </TableRow>

                    <TableRow>
                        {schedule.weekdays.monday.map(_ => (
                            <>
                                <TableCell>
                                    Пара
                                </TableCell>
                                <TableCell>
                                    Кабинет
                                </TableCell>
                                <TableCell>
                                    Преподаватель
                                </TableCell>
                            </>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {Object.entries(schedule.weekdays).map(([key, weekday], i) => {
                        if (key === 'statistic') return null;

                        return (
                            <Fragment key={i}>
                                <TableRow>
                                    <TableCell>
                                        {key}
                                    </TableCell>
                                    <TableCell>

                                        {Array.from({length: 7}, (_, i) => (
                                                <TableRow key={i} colSpan={2}>
                                                    <TableCell>
                                                        {i + 1}
                                                    </TableCell>
                                                </TableRow>
                                            )
                                        )}
                                    </TableCell>

                                    <TableCell>
                                        {Array.from({length: 7}, (_, i) => (
                                                <TableRow key={i} colSpan={2}>
                                                    <TableCell>
                                                        date
                                                    </TableCell>
                                                </TableRow>
                                            )
                                        )}
                                    </TableCell>
                                    {weekday.map(group => (
                                        <TableCell key={group.group_name} colSpan={3}>
                                            {Array.from({length: 7}).map((_, i) => {
                                                    const lesson = group.lessons.find(lesson => lesson.lesson_index === i) || {}
                                                    return (
                                                        <TableRow key={lesson.lesson_index} colSpan={3}>
                                                            <TableCell>{lesson.lesson_name ?? '---'}</TableCell>
                                                            <TableCell>{lesson.lesson_cabinet ?? '---'}</TableCell>
                                                            <TableCell>{lesson.lesson_teacher ?? '---'}</TableCell>
                                                        </TableRow>
                                                    )

                                                }
                                            )}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </Fragment>)
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

export default App
