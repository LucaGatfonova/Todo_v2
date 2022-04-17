import React from 'react';
import {Link} from 'react-router-dom';
import { Button } from 'react-bootstrap';


const ProjectItem = ({project, users, deleteProject, updateProject}) => {
    return (
        <tr>
            <td>><Link to={`/project/${project.id}`}>{project.name}</Link></td>
            <td>{project.repositoryUrl}</td>
            <td>{project.users.map((userId) => {return users.find((user) => user.id == userId).first_name+' '})}</td>
            {deleteProject && <td><Button variant="outline-danger" onClick={()=>deleteProject(project.id)}
             type='button'>Удалить</Button></td>}
        </tr>
    )
}


export default ProjectItem;