import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import * as React from "react";
import './component-NavbarPantry.css';

class NavbarPantry extends React.Component {
    render() {
        return(
            <Navbar bg="dark" variant='dark' sticky={'top'}>
                <Navbar.Brand href="#home" id="logo-name">Pantry Engine</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link href="#about">About</Nav.Link>
                    <Nav.Link href="#home">Search</Nav.Link>
                    <Nav.Link href="https://github.com/Sami-BG/recipe-browser">Github</Nav.Link>
                </Nav>
            </Navbar>
        )
    }
}

export default NavbarPantry;