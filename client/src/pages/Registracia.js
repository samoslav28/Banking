import React, { useState } from 'react';
import "./Registracia.css";

const Registracia = () => {
  const [message, setMessage] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [amount, setAmount] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('/api/create-account', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: firstName, lastName, amount
      }),
    });
    const data = await response.json();
    console.log(data.message["abc"]);
    setMessage(data.message);
    setIsSubmitted(true);
  };

  return (
    <div>
      {!isSubmitted ? (
        <form onSubmit={handleSubmit}>
          <div className="input-row">
            <div>
              <label>
                <h4 id='title'>Prvé meno:</h4>
                <input id='input-first'
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </label>
            </div>
            <div>
              <label>
                <h4 id='title'>Priezvisko:</h4>
                <input id='input-last'
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </label>
            </div>
          </div>
          <div>
            <label>
              <h4 id='title'>Suma:</h4>
              <input id='input-number'
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </label>
          </div>
          <button type="submit">Odoslať</button>
        </form>
      ) : null}
      {isSubmitted && (
        <div id='message-register'>
        <h5>{message["abc"]}</h5>
        <br />
        <h6>Vase cislo uctu je: {message["bca"]}</h6>
      </div>
      )}
    </div>
  );
};

export default Registracia;
