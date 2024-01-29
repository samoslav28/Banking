import {useState, useEffect} from 'react'

const Members = () => {
    const [data, setData] = useState([{}])

    

    useEffect ( () => {
        fetch("/members").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data);
            }
        )
    },[])



  return (
    <div>
        {(typeof data.members === "undefined") ? (
            <p>Loading...</p> ) : (
                data.members.map((oneData, i) => (
                    <p key={i}>{oneData}</p>
                )
            )
        ) }
    </div>
  )
}

export default Members