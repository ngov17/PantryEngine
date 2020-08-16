import React from 'react';
import './App.css';
import NavbarPantry from "./NavbarPantry/NavbarPantry";
import SearchPantry from "./SearchPantry/SearchPantry";
import Container from "react-bootstrap/cjs/Container";
import Logo from "./Logo/Logo";
import TestCardWrapper from "./TestCardWrapper/TestCardWrapper";
import Subtext from "./Subtext/Subtext";

function App() {
  return (
    <div className="App">
      <Container className='w-50'>
          <NavbarPantry/>
          <div className={'logo-subtext-container'}>
              <Logo className='mb-4'/>
              <Subtext query={'A search engine for food.'}/>
          </div>
      <div className={'col-md-12 mx-auto'}>
          <SearchPantry/>
          {/*TODO: Wrap the below 4 components into one bigger component, that gets re-rendered as list of cards. */}
          <TestCardWrapper query={'Or try some of our template searches:'}/>
          <SearchPantry query={"tomatoes, garlic, chicken, a few slices of toast"} disabled={true}/>
          <SearchPantry query={"sweet potatoes, cucumber, carrots, lemon"} disabled={true}/>
          <SearchPantry query={"kale, onions, pasta, paprika, flour"} disabled={true}/>
      </div>
      </Container>
    </div>
  );
}

export default App;
