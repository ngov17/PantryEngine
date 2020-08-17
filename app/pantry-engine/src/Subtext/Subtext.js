import * as React from "react";
import './Subtext.css';

class Subtext extends React.Component {

    render() {
        return (
            <div className={'subtext'}>
                {this.props.query}
            </div>
        )
    }

}

export default Subtext;