import React from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie';
import logo from './logo.svg';
import './App.css';
import {HashRouter, BrowseRouter, Route, Link, Switch, Redirect} from "react-router-dom"
import { Container, Alert } from 'react-bootstrap';
import { Navbar, Button } from 'react-bootstrap';

import MainMenu from './components/MainMenu.js';
import Footer from './components/Footer.js';
import UserList from './components/User.js';
import UserDetail from './components/UserDetail.js';
import ProjectList from './components/Project.js';
import ProjectDetail from './components/ProjectDetail.js';
import TodoList from './components/Todo.js';
import LoginForm from './components/Auth.js';
import NotFound404 from './components/NotFound404.js';
import ProjectForm from './components/ProjectForm.js';
import TodoForm from './components/TodoForm.js';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'projects': [],
            'todo': [],
            'token': '',
            'username': '',
        }
    }

    createProject (name, repository_url, users) {
        const headers = this.get_headers()
        const data = {name: name, repository_url: repository_url, users: users}
        console.log(data)
        axios.post('http://127.0.0.1:8000/api/v1/projects/', data, {headers})
            .then(response => {
                this.load_data()
            }).catch(error => {console.log(error)})
    }

    deleteProject (id) {
        const headers = this.get_headers()
        console.log('Id deleted project =', id)
        axios.delete(`http://127.0.0.1/api/projects/${id}`, {headers})
            .then(response => {
                this.load_data()
            }).catch(error => {console.log(error)})
    }

    createTodo (project, user, title, text) {
        const headers = this.get_headers()
        const data = {project: project, user: user, title: title, text: text}
        console.log('data = ', data)
        axios.post('http://127.0.0.1:8000/api/v1/todo/', data, {headers})
            .then(response => {
                this.load_data()    // лучше перезапрашивать данные, на случай если кто-то еще правит БД
            }).catch(error => {console.log(error)})
    }

    deleteTodo (id) {
        const headers = this.get_headers()
        console.log('Id deleted todo =', id)
        axios.delete(`http://127.0.0.1:8000/api/v1/todo/${id}`, {headers})
            .then(response => {
                this.load_data()
            }).catch(error => {console.log(error)})
    }


    set_token(token) {
        const cookies = new Cookies()
        cookies.set('token', token)
        this.setState({'token': token}, () => this.load_data())
    }

    get_token_from_storage() {
        const cookies = new Cookies()
        const token = cookies.get('token')
        this.setState({'token': token}, () => this.load_data())
    }

    is_authenticated() {
        return !!this.state.token
    }

    logout() {
        this.set_token('')
        this.setState({'username': ''})
    }

    get_token(username, password) {
        axios.post('http://127.0.0.1:8000/api-token-auth/', {username: username, password: password})
        .then(response => {
            console.log(response.data)
            this.set_token(response.data['token'])
            this.setState({'username': username})
            console.log(this.state.username)
        }).catch(error => alert('Неверный логин или пароль'))
    }

    get_headers() {
        let headers = {
            'Content-Type': 'application/json',
            'Accept':'application/json'
        }
        if (this.is_authenticated()){
                headers['Authorization'] = 'Token ' + this.state.token
            }
        return headers
    }

    componentDidMount() {
        this.get_token_from_storage()
    }

    load_data() {
        const headers = this.get_headers()
        axios.get('http://127.0.0.1:8000/api/v1/users/', {headers})
            .then(response => {
                const users = response.data.results
                this.setState(
                            {
                               'users': users
                            }
                )
            }).catch(error => {
                                this.setState({users:[]})
                                console.log(error)
                                }
                )
        axios.get('http://127.0.0.1:8000/api/v1/projects/', {headers})
            .then(response => {
                const projects = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'projects': projects
                            }
                )
            }).catch(error => {
                                this.setState({projects:[]})
                                console.log(error)
                                }
                )
        axios.get('http://127.0.0.1:8000/api/v1/todo/', {headers})
            .then(response => {
                const todo = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'todo': todo
                            }
                )
            }).catch(error => {
                                this.setState({todo:[]})
                                console.log(error)
                                }
                )
    }

    render () {
        return (
            <div>
                <HashRouter>
                    <MainMenu />
                    <br/><br/>
                    <Container>
                    {this.is_authenticated() ?
                        <Alert.Link variant='primary' onClick={() => this.logout()}>Logout {this.state.username}</Alert.Link> :
                        <button type="button" class="btn btn-info"><Link to='/login'>Login</Link></button>
                    }
                    <Switch>
                        <Route exact path='/' component={() => <UserList users={this.state.users} />} />
                        <Route exact path='/projects' component={() => <ProjectList projects={this.state.projects} users={this.state.users} deleteProject={(id)=>this.deleteProject(id)} />} />
                        <Route exact path='/todo' component={() => <TodoList todo={this.state.todo} users={this.state.users} deleteTodo={(id)=>this.deleteTodo(id)} />} />
                        <Route exact path='/todo/create' component={() => <TodoForm projects={this.state.projects} users={this.state.users} createTodo={(project,user,title,text) => this.createTodo(project,user,title,text)} />} />
                        <Route exact path='/project/:id'>
                            <ProjectDetail projects={this.state.projects} users={this.state.users} todo={this.state.todo} />
                        </Route>
                        <Route exact path='/user/:id'>
                            <UserDetail all_obj={this.state} />
                        </Route>
                        <Route exact path='/projects/create' component={() => <ProjectForm users={this.state.users} createProject={(name,repository_url,users) => this.createProject(name,repository_url,users)} />} />
                        <Route exact path='/login' component={() => <LoginForm get_token={(username, password) => this.get_token(username, password)} />} />
                        <Route component={NotFound404} />
                    </Switch>
                        <br/>
                 </Container>
                </HashRouter>
                <Footer />
            </div>
        )
    }
}

export default App;
