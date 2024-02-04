import React, { useState } from 'react';
import "./Testing.css"
import MainInput from '../components/MainInput';

const Testing = () => {
  const [message, setMessage] = useState();
  const [updateDataAccount, setUpdateDataAccount] = useState('')
  const [updateDataEntry, setUpdateDataEntry] = useState()
  const [updateDataAmount, setUpdateDataAmount] = useState('')
  const [isValid, setIsValid] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

// console.log(updateData);


  const handleSubmit = async (e) => {
    e.preventDefault();
    let endpoint = '';
  
    if (updateDataEntry === '' || updateDataEntry === undefined || updateDataEntry === null) {
      setUpdateDataEntry("vklad")
      console.log("sadfasdfasdfasdf",updateDataEntry);

    }

    if (currentStep === 1) {
      // Odeslání kódu na server pro ověření
      endpoint = '/api/verify-code';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: updateDataAccount
        }),
      });
      setUpdateDataAccount('')
      const data = await response.json();

      if (endpoint === '/api/verify-code') {
        if (data.isValid === true) {
          setCurrentStep(2);
          setMessage(null)
        } else {
          console.log(data.isValid);
          setMessage(data.isValid)
          setIsValid(false);
          document.querySelector('button').classList.add('invalid');
          setCurrentStep(1);
          return;
        }
      }
    } else if (currentStep === 2) {
      // Odeslání výběru na server
      endpoint = '/api/process-input';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: updateDataEntry
        }),
      });
      const data = await response.json();
      setUpdateDataEntry('')

    } else if (currentStep === 3) {
      // Odeslání výběru na server
      endpoint = '/api/entry-amount';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: updateDataAmount
        }),
      });
      const data = await response.json();
      setMessage(data.message)
      setUpdateDataAmount('')
    } else {
      return; // Pro jistotu, kdyby se náhodou dostal do neplatného kroku
    }
  

  
  

  
    // Pokračování v další logice podle potřeby
  
    // Resetovat stav pro další zadání kódu
    setIsValid(false);
  
    // Nastavit další krok
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      setCurrentStep(1);
    }
  };
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        {currentStep === 1 && (
          <label>
            <h4 id='title'>Zadajte číslo účtu:</h4>
            <input id='number-of-account'
              type="text"
              value={updateDataAccount}
              onChange={(f) => setUpdateDataAccount(f.target.value)}
            />
          </label>
        )}
{currentStep === 2 && (
  <label>
    <h4 id='title'>Prajete si?</h4>
    <select id='select'
      value={updateDataEntry}
      onChange={(e) => {
        setUpdateDataEntry(e.target.value);
      }}
    >
      <option value="vklad">Vklad</option>
      <option value="vyber">Výber</option>
    </select>
  </label>
)}

        {currentStep === 3 && (
          <label>
            <h4 id='title'>{updateDataEntry === 'vklad' ? 'Akú sumu chcete vložiť?' : 'Akú sumu chcete vybrať?'}</h4>
            <input id='amount'
              type="number"
              value={updateDataAmount}
              onChange={(e) => setUpdateDataAmount(e.target.value)}
            />
          </label>
        )}
        <button type="submit">Potvrdiť</button>
      </form>
      <div id='message'>
        <h3>{message}</h3>
        </div>
    </div>
  );
};

export default Testing;
