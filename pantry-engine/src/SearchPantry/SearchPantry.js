import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from "react-bootstrap/Button";
class SearchPantry extends React.Component {

    handleSubmit = () => {
        const value = document.getElementById('search_main').value;
        alert(value)
    }

    render() {
        return(
            <div className={'searchbar'}>
                <form className={'p-2'}>
                    <input id='search_main' placeholder={'Search for recipes using your ingredients!'} size={'50'} type={'text'}/>
                    <input type={'submit'} value={'Search!'} onClick={this.handleSubmit}/>
                </form>
            </div>
        )
    }
}

export default SearchPantry;