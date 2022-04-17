import TodoItem from './TodoItem.js'
import {HashRouter, BrowseRouter, Route, Link, Switch, Redirect} from "react-router-dom"
import { Table, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const TodoList = ({todo, users, deleteTodo}) => {
    return (
        <div>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Проект</th>
                        <th>Создатель</th>
                        <th>Название</th>
                        <th>Заметка</th>
                        <th>Активность</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {todo.map((todo)=> <TodoItem todo={todo} users={users} deleteTodo={deleteTodo} />)}
                </tbody>
            </Table>
           <button type="button" class="btn btn-info"><Link to='/todo/create'>Создать заметку</Link></button>
       </div>
    )
}

export default TodoList;