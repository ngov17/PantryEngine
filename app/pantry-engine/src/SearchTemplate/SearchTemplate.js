import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';

import Button from "react-bootstrap/Button";

class SearchTemplate extends React.Component {

    render() {
        return(
                <div className={'searchbar'}>
                    <input type={'text'}
                           className={'search_input'}
                           onChange={this.onTextChanged}
                           onKeyDown={this.handleKeyDown}
                           disabled={true}
                           placeholder={this.props.value}/>
                    <button type={'submit'}
                            className={'search_button'}
                            onClick={this.props.buttonClick}>Search</button>
                </div>
        )
    }
}

export default SearchTemplate;