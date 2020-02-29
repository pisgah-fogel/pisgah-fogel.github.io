import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hello world
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
         </header>

    ​<table class="calendar">
      <tr>
        <th>January</th>
        <th>February</th>
        <th>March</th>
        <th>April</th>
        <th>May</th>
        <th>June</th>
        <th>July</th>
        <th>August</th>
        <th>September</th>
        <th>October</th>
        <th>November</th>
        <th>December</th>
      </tr>
      <tr>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
        <td>Week 1</td>
      </tr>
      <tr>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
        <td>Week 2</td>
      </tr>
      <tr>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
        <td>Week 3</td>
      </tr>
      <tr>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
        <td>Week 4</td>
      </tr>
      <tr>
      <td>Week 5</td>
        <td class="blank"></td>
        <td class="blank"></td>
        <td>Week 5</td>
        <td class="blank"></td>
        <td class="blank"></td>
        <td>Week 5</td>
        <td class="blank"></td>
        <td class="blank"></td>
        <td>Week 5</td>
        <td class="blank"></td>
        <td>Week 5</td>
      </tr>
    </table>
    </div>
      );
    }
    
    export default App;
