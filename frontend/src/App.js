import './App.scss';
// import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";

import UploadImages from "./components/image-upload.component";

function App() {
  return (
    <div className="container">
      <h3>Decolourizer AI</h3>

      <div className="content">
        <UploadImages />
      </div>
    </div>
  );
}

export default App;


// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <p>
//           Hello world, I am John Robert, I am getting started with React. 
//         </p> 
//       </header>
//     </div>
//   );
// }

// export default App;
