import React from 'react';
const List = (props) => {
    const { repos } = props;
    if (repos.length === 0) return <p>No Results Match Your Search</p>;
    return (
        <ul>
            <h2 className='list-head'>Search Results</h2>
            {repos.map((repo) => {
                return (
                    <li className='list'>
                        <span className='repo-text'>{repo} </span>
                    </li>
                    
                );
            })}
        </ul>
    );
};
export default List;