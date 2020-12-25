import * as React from "react";
import './NavbarPantry.css';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

class NavbarPantry extends React.Component {
    render() {
        return(
            this.newNavbar()
        )
    }

    newNavbar() {
        return (
            <div className={'navbar'}>
                <div className={'about navbar-item'} onClick={this.handleAboutRedirect}>
                    <a className={'navbar-text'} href={'#about'}><Link style={{color:'#ffffff'}} to={'/about'}>About</Link></a>
                </div>

                <div className={'search navbar-item'} onClick={this.handleHomeRedirect}>
                    <a className={'navbar-text'} href={'#home'}><Link style={{color:'#ffffff'}} to={'/'}>Search</Link></a>
                </div>

                <div className={'github navbar-item'} onClick={this.handleGithubRedirect}>
                    <h3 className={'navbar-text'} href={'https://github.com/Sami-BG/recipe-browser'}><Link style={{color:'#ffffff'}}
                                                                                                           to={''}>Github</Link></h3>
                </div>

            </div>
        )
    }

    handleAboutRedirect = () => {
        window.location.href = '#about';
    }

    handleHomeRedirect = () => {
        window.location.href = '#';
    }

    handleGithubRedirect = () => {
        window.open('https://github.com/Sami-BG/recipe-browser');
    }


}

export default NavbarPantry;