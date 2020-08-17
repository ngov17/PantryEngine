import * as React from "react";
import SearchPantry from "../SearchPantry/SearchPantry";

class SearchContainer extends React.Component {
    state = {
        result: []
    }
    render() {
        return (
            <div className={'col-md-12 mx-auto'}>
                <SearchPantry callback = {this.handleResult}/>
                {/*TODO: Wrap the below 4 components into one bigger component, that gets re-rendered as list of cards. */}
                {/*<TestCardWrapper query={'Or try some of our template searches:'}/>*/}
                {/*<SearchPantry query={"tomatoes, garlic, chicken, a few slices of toast"} disabled={true}/>*/}
                {/*<SearchPantry query={"sweet potatoes, cucumber, carrots, lemon"} disabled={true}/>*/}
                {/*<SearchPantry query={"kale, onions, pasta, paprika, flour"} disabled={true}/>*/}
            </div>
        )
    }

    handleResult = (queryResult) => {
        this.state.result = queryResult;
        console.log(this.state.result)
    }
}

export default SearchContainer;