import useSWR from 'swr'
import axios from 'axios';
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {Fragment} from "react";
import {times, weekdays, ENDPOINT} from "./consts.js";


// eslint-disable-next-line react/prop-types
const ScheduleTable = ({schedule: scheduleId}) => {
    const {data, isLoading} = useSWR(
        scheduleId ? `${ENDPOINT}api/schedules/${scheduleId}/` : null, axios
    )

    if (isLoading || !data?.data?.content) return 'Загрузка...'

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
                    {weekdays.map(({name, value, index}) => {
                        const weekday = schedule.weekdays[value]

                        return (
                            <Fragment key={index}>
                                <TableRow>
                                    <TableCell>
                                        {name}
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
                                        {times.map((time, i) => (
                                                <TableRow key={i} colSpan={2}>
                                                    <TableCell>
                                                        {time}
                                                    </TableCell>
                                                </TableRow>
                                            )
                                        )}
                                    </TableCell>
                                    {weekday.map(group => (
                                        <TableCell key={group.group_name} colSpan={3}>
                                            {Array.from({length: 7}).map((_, i) => {
                                                    const lesson = group.lessons.find(lesson => lesson.lesson_index - 1 === i) || {}
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
};

export default ScheduleTable;