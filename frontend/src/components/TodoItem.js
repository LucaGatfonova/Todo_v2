import React from 'react';
import { Button } from 'react-bootstrap';

const TodoItem = ({todo, users, deleteTodo}) => {
    let user = users.filter((item) => item.id === todo.user)[0]
    return (
        <tr>
            <td>{todo.project}</td>
            <td>{user.username}</td>
            <td>{todo.title}</td>
            <td>{todo.text}</td>
            <td>{todo.is_active ? '✅' : '❌'}</td>
            <td><Button variant="outline-danger" onClick={() => deleteTodo(todo.id)}
             type='button'>Delete</Button></td>
        </tr>
    )
}

export default TodoItem;