'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function login(formData: FormData) {
    const password = formData.get('password') as string
    const correctPassword = process.env.ADMIN_PASSWORD

    if (password === correctPassword) {
        (await cookies()).set('admin_session', 'true', {
            httpOnly: true,
            path: '/',
            maxAge: 60 * 60 * 24 // 1 day
        })
        redirect('/admin')
    }

    return { error: 'Contraseña incorrecta' }
}

export async function logout() {
    (await cookies()).delete('admin_session')
    redirect('/login')
}
