import SearchPantry from "../SearchPantry/SearchPantry";
import React from "react";
import SearchTemplate from "../SearchTemplate/SearchTemplate";

class ResultsContainer extends React.Component {

    state = {
        query: false
    }



    render() {
        return (
            <SearchPantry/>

        )
    }
}