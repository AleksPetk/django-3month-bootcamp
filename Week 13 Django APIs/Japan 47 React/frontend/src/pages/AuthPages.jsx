import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import FormField from '../components/FormField'

function AuthShell({ mode }) {
  const registering = mode === 'register'; const { user, login, register } = useAuth(); const location = useLocation(); const navigate = useNavigate()
  const [values, setValues] = useState({ username: '', email: '', password: '', password2: '' }); const [errors, setErrors] = useState({}); const [busy, setBusy] = useState(false)
  if (user) return <Navigate to="/" replace />
  const change = (e) => setValues((v) => ({ ...v, [e.target.name]: e.target.value }))
  const submit = async (e) => { e.preventDefault(); setBusy(true); setErrors({}); try { registering ? await register(values) : await login(values.username, values.password); navigate(location.state?.from || '/', { replace: true }) } catch (err) { setErrors(err.fields || { general: err.message }) } finally { setBusy(false) } }
  return <section className="auth-page"><div className="auth-card"><header><span aria-hidden="true">{registering ? '桜' : '旅'}</span><p className="eyebrow">{registering ? 'Begin your journey' : 'Welcome back'}</p><h1>{registering ? 'Create an account' : 'Login'}</h1></header><form onSubmit={submit}>{errors.general && <p className="form-error">{errors.general}</p>}<FormField label="Username" name="username" errors={errors} required><input id="username" name="username" autoComplete="username" value={values.username} onChange={change} required /></FormField>{registering && <FormField label="Email" name="email" errors={errors} required><input id="email" name="email" type="email" autoComplete="email" value={values.email} onChange={change} required /></FormField>}<FormField label="Password" name="password" errors={errors} required><input id="password" name="password" type="password" autoComplete={registering ? 'new-password' : 'current-password'} value={values.password} onChange={change} required /></FormField>{registering && <FormField label="Confirm password" name="password2" errors={errors} required><input id="password2" name="password2" type="password" autoComplete="new-password" value={values.password2} onChange={change} required /></FormField>}<button className="button button--primary button--full" disabled={busy}>{busy ? 'Please wait…' : registering ? 'Register' : 'Login'}</button></form><p>{registering ? 'Already have an account?' : 'New to Japan 47?'} <Link to={registering ? '/login' : '/register'}>{registering ? 'Login' : 'Create an account'}</Link></p></div></section>
}

export const LoginPage = () => <AuthShell mode="login" />
export const RegisterPage = () => <AuthShell mode="register" />
