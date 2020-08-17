import * as React from "react";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Form from "react-bootstrap/Form"
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from "react-bootstrap/Button";

class SearchTemplate extends React.Component {

    handleSubmit = () => {
        alert(this.props.query);
    }

    render() {
        return(
            <div className={'searchbar'}>
                <form className={'p-2'}>
                    <input className={'searchTemplate'} placeholder={this.props.query} size={'50'} type={'text'} disabled/>
                    <input type={'submit'} value={'Search!'} onClick={this.handleSubmit}/>
                </form>
            </div>
        )
    }
}

export default SearchTemplate;