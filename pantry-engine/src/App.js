import React from 'react';
import './App.css';
import NavbarPantry from "./NavbarPantry/NavbarPantry";
import SearchPantry from "./SearchPantry/SearchPantry";
import Container from "react-bootstrap/cjs/Container";
import SearchTemplate from "./SearchTemplate/SearchTemplate";

function App() {
  return (
    <div className="App">
      <NavbarPantry/>
      <Container>
          <SearchPantry/>
          <SearchTemplate query={"tomatoes, garlic, chicken, a few slices of toast"}/>
          <SearchTemplate query={"sweet potatoes, cucumber, carrots, lemon"}/>
          <SearchTemplate query={"kale, onions, pasta, paprika, flour"}/>
      </Container>
    </div>
  );
}

export default App;
