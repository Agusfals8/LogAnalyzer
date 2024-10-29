import React from 'react';

const Header = () => {
  return (
    <header style={{background: '#eee', padding: '10px 20px'}}>
      <nav>
        <ul style={{listStyle: 'none', display: 'flex', justifyContent: 'space-around'}}>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href={`/contact${process.env.REACT_APP_CONTACT_ROUTE_SUFFIX}`}>Contact</a></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;