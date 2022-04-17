import UserItem from './UserItem.js'
import { Table, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


const UserList = ({users}) => {
    return (
        <Table striped bordered hovere>
            <thead>
                <tr>
                    <th>Логин</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>Почта</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user)=> <UserItem user={user}/>)}
            </tbody>
        </Table>
    )
}

export default UserList;