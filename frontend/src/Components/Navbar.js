import React from 'react'

export default function Navbar() {
  return (
    <div>
        <Link to="/">Home</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/mapview">Map View</Link>
        <Link to="/predictions">Predictions</Link>
        <Link to="/reports">Reports</Link>

    </div>
  )
}
