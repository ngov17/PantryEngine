
import * as React from "react";
import { ReactComponent as ReactLogo } from "./images/React-icon.svg";
import { ReactComponent as ElasticLogo } from "./images/Elasticsearch_logo.svg";
import { ReactComponent as NodeLogo } from "./images/Node.js_logo.svg";
import "./about.css";

class AboutPage extends React.Component {
    render() {
        return (
            <div className={'about-page-container'}>
                <div className={'about-text'}>
                    Built using:
                </div>
                <div className={'about-logo-row'}>
                    <ReactLogo className={'about-logo'}/>
                </div>
                <div className={'about-logo-row'}>
                    <ElasticLogo className={'about-logo'}/>
                    <NodeLogo className={'about-logo'}/>
                </div>
            </div>

        )
    }

}

export default AboutPage;