import useSWR from 'swr'
import axios from 'axios';
import './App.css'
import {useState} from "react";
import {ENDPOINT} from "./consts.js";
import ScheduleTable from "./ScheduleTable.jsx";


function App() {
    const [activeSchedule, setActiveSchedule] = useState(null)
    const {data, isLoading} = useSWR(`${ENDPOINT}api/schedules/`, axios)

    if (isLoading || !data?.data?.content?.length) return null

    return <div>

        <div>
            <h2>
                Выберите расписание
            </h2>

            <select onChange={(e) => setActiveSchedule(+e.target.value)} id="select-schedule">
                {data.data.content.map((schedule) => <option key={schedule.id} value={schedule.id}>ID {schedule.id}: {schedule.name}</option>)}
            </select>
            <button onClick={(e) => {
                let sch_id = document.getElementById("select-schedule").value
                setActiveSchedule(sch_id)
            }}>Показать</button>
        </div>
        {activeSchedule && <ScheduleTable schedule={activeSchedule}/>}
    </div>
}

export default App
