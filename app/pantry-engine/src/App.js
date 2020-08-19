import React from 'react';
import './App.css';
import NavbarPantry from "./NavbarPantry/NavbarPantry";
import SearchPantry from "./SearchPantry/SearchPantry";
import Container from "react-bootstrap/cjs/Container";
import Logo from "./Logo/Logo";
import TestCardWrapper from "./TestCardWrapper/TestCardWrapper";
import Subtext from "./Subtext/Subtext";
import SearchContainer from "./SearchContainer/SearchContainer";
import RecipeCard from "./RecipeCard/RecipeCard";

function App() {
  return (
    <div className="App">
          <NavbarPantry/>
          <div className={'logo-subtext-container'}>
              <Logo className='mb-4'/>
              <Subtext query={'A search engine for food.'}/>
          </div>
        {/*<SearchPantry/>*/}
        <RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}
                    recipe_url={'https://github.com/'}
                    recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}
                    ingredients={['4x eggs', '3 tomatoes', 'peppers', 'onions']}/>
        <RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}
                    recipe_url={'https://github.com/'}
                    recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}
                    ingredients={['4x eggs', '3 tomatoes', 'peppers', 'onions']}/>
        <RecipeCard recipe_title={"Lorem Ipsum with a bunch of other stuff"}
                    recipe_url={'https://github.com/'}
                    recipe_img={'https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg'}
                    ingredients={['4x eggs', '3 tomatoes', 'peppers', 'onions']}/>
    </div>
  );
}

export default App;
