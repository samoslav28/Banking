import React, { useState } from 'react';

const Project = () => {
  const [updateFirstValue, setUpdateFirstValue] = useState()
  const [updateSecondValue, setUpdateSecondValue] = useState()
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });



  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      setUpdateFirstValue(data.result)
      setUpdateSecondValue(data.heslo)
      setFormData({username: "", password: ""})
    } catch (error) {
      console.error('Chyba pri odosielaní dát:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };


  return (
    <section>
      <input
        type="text"
        name="username"
        value={formData.username}
        onChange={handleChange}
      />
      <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>Odoslať</button>
      <div>
        <h2>{updateFirstValue}</h2>
        <h2>{updateSecondValue}</h2>

      </div>
    </section>
  )
}

export default Project;
