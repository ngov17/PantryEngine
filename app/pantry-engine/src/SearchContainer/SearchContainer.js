import * as React from "react";


class SearchContainer extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        console.log(this.props.result)
        return (
          <div>
                  {this.props.result.map((result, index) => (
                      <div key={index}>
                          <h3>{result.title}</h3>
                      </div>
                  ))}

          </div>


        )
    }
}

export default SearchContainer;