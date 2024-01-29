import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import Prihlasenie from "../pages/Prihlasenie"
import Members from "../pages/Members"
import Project from "../pages/Project"
import Bank from "../pages/Bank"
import Testing from "../pages/Testing"
import Registracia from '../pages/Registracia';
import "./Nav.css"



const Nav = () => {
    return (
        <div className='menu'>
          <Router>
            <nav>
              <ul>
                  <NavLink to="/prihlasenie">Prihlasenie</NavLink>
                  <NavLink to="/members">Members</NavLink>
                  <NavLink to="/project">Project</NavLink>
                  <NavLink to="/bank">Banka</NavLink>
                  <NavLink to="/testing">Testing</NavLink>
                  <NavLink to="/register">Register</NavLink>
              </ul>
            </nav>
            <Routes>
              <Route path="/prihlasenie" element={<Prihlasenie />} />
              <Route path="/members" element={<Members />} />
              <Route path="/project" element={<Project />} />
              <Route path="/bank" element={<Bank />} />
              <Route path="/testing" element={<Testing />} />
              <Route path="/register" element={<Registracia />} />
            </Routes>
          </Router>
        </div>
      );
}

export default Nav