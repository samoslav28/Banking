import React from 'react'
import { useState } from 'react'
import "./Bank.css"

const Bank = () => {
    const [accountNumber, setAccountNumber] = useState()
    const [select, setSelect] = useState()
    const [balance, setBalance] = useState()
    const [result, setResult] = useState()



    const submitForm = async (submit) => {
        submit.preventDefault()
        try {
            const response = await fetch('/api/bank', {
                method: 'POST',
                headers: {
                    'Content-type' : 'application/json'
                },
                body: JSON.stringify({ accountNumber, select, balance })
            })
            const data = await response.json();
            console.log(data);
            setResult(data.result)
          } catch (error) {
            console.error('Chyba pri odosielaní dát:', error);
        }
    }


    const resetAttempts = async () => {
    try {
        const reset = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await reset.json();
        console.log(data.message);
        setResult("Heslo bolo restarovane")
    } catch (error) {
        console.error('Chyba při resetování pokusů:', error);
    }
}

  return (
    <section>
        <div className='input_form'>
        <div className="button-container">
  <form onSubmit={submitForm} className="form-container">
    <div className='input-container'>
      <input id='cisloUctu' onChange={(e) => setAccountNumber(e.target.value)} placeholder='Zadaj cislo uctu' /><br />
      <input id='select' onChange={(e) => setSelect(e.target.value)} type="select" placeholder='Zadaj volbu' /><br />
      <input id='vklad' onChange={(e) => setBalance(e.target.value)} type="number" placeholder='Kolko chcete vybrat/vlozit' /><br />
    </div>
    <input className='button submit-button' type='submit' value="Odoslat" />
  </form>
  <button className="button reset-button" onClick={resetAttempts}>Reset</button>
</div>




        </div>
        <div className='vypis'>
            <h1>{result}</h1>
        </div>
    </section>
  )
}

export default Bank