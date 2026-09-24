import React from 'react'

export default function Login() {
  return (
    <div className="login">
      <h2>Login</h2>
      <form>
        <label>Username:</label>
        <input type="text" />
        <label>Password:</label>
        <input type="password" />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
