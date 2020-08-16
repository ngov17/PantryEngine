import * as React from "react";

class TestCardWrapper extends React.Component {
    render() {
        return (
            <h1 className={'big_text'}>{this.props.query}</h1>
        )
    }
}

export default TestCardWrapper;