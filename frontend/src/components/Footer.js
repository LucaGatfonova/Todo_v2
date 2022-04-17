import React from "react";
import "./Footer.css";
import {Link, Route} from 'react-router-dom';

const Footer = () => {
  return (
  <div className="main-footer">
       <div>
               <li>Пользователи</li>
                <li>Проекты</li>
                <li>Заметки</li>
       </div>

        <hr />
        <div className="row">
          <p className="col-sm">
            &copy;{new Date().getFullYear()} ToDo | All rights reserved
          </p>
        </div>
      </div>

  );
}

export default Footer;