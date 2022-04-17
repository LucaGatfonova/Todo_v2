import React from 'react';
import { Form, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


class LoginForm extends React.Component {
    constructor(props) {
      super(props)
      this.state = {login: '', password: ''}
    }

    handleChange(event)
    {
        this.setState(
                {
                    [event.target.name]: event.target.value
                }
            );
    }

    handleSubmit(event) {
      console.log(this.state.login + ' ' + this.state.password)
      this.props.get_token(this.state.login, this.state.password)
      event.preventDefault()
    }

    render() {
      return (
         <form onSubmit={(event)=> this.handleSubmit(event)}>
         <br/><br/><br/>
            <Form.Label htmlFor="inputLogin5">Login</Form.Label>
            <Form.Control type="text" name="login" placeholder="login" value={this.state.login}
                   onChange={(event)=>this.handleChange(event)} />
             <br/>
            <Form.Label htmlFor="inputPassword5">Password</Form.Label>
            <Form.Control type="password" name="password" placeholder="password" value={this.state.password}
                   onChange={(event)=>this.handleChange(event)} />
            <br/>
            <Button type="submit" value="Login" variant="dark">Login</Button>
        </form>

      );
    }
  }

export default LoginForm;
