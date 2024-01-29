import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import Testing from "../pages/Testing"
import Registracia from "../pages/Registracia"
import "./Nav.css"



const MainInput = () => {
    return (
        <div className='menu'>
          <Router>
            <nav>
              <ul>
                  <NavLink to="/testing">Testing</NavLink>
                  <NavLink to="/register">Registracia</NavLink>

              </ul>
            </nav>
            <Routes>
              <Route path="/testing" element={<Testing />} />
              <Route path="/register" element={<Registracia />} />
            </Routes>
          </Router>
        </div>
      );
}

export default MainInput