import React, { Component } from "react";
import {Link, Route} from 'react-router-dom';
import {Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';

export default class NavbarComp extends Component {
    render() {
        return (
          <Route>
            <div>
                <Navbar bg="dark" expand="lg" variant="dark">
                    <Container>
                       <Navbar.Brand href="#home">ToDo</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav" />
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="me-auto">
                                <li><Nav.Link as={Link} to='/'>Пользователи</Nav.Link></li>
                                <li><Nav.Link as={Link} to='/projects'>Проекты</Nav.Link></li>
                                <li><Nav.Link as={Link} to='/todo'>Заметки</Nav.Link></li>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </div>
          </Route>
        )
    }
}