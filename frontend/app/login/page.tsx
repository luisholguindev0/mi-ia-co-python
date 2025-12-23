'use client'
import { useFormStatus } from 'react-dom'
import { login } from '../actions'

function SubmitButton() {
    const { pending } = useFormStatus()
    return (
        <button
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50 transition-colors"
            type="submit"
            disabled={pending}
        >
            {pending ? 'Entrando...' : 'Entrar'}
        </button>
    )
}

export default function LoginPage() {
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm border border-gray-200">
                <div className="text-center mb-6">
                    <h1 className="text-2xl font-bold text-gray-900">Mi IA Dashboard</h1>
                    <p className="text-sm text-gray-500">Acceso Administrativo</p>
                </div>

                <form action={login} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña Maestra</label>
                        <input
                            name="password"
                            type="password"
                            required
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-gray-900 placeholder-gray-400"
                            placeholder="••••••••"
                        />
                    </div>
                    <SubmitButton />
                </form>
            </div>
        </div>
    )
}
