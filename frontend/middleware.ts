import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
    // Solo proteger rutas /admin
    if (request.nextUrl.pathname.startsWith('/admin')) {
        const session = request.cookies.get('admin_session')

        // Si no hay cookie, redirigir a login
        if (!session || session.value !== 'true') {
            return NextResponse.redirect(new URL('/login', request.url))
        }
    }

    return NextResponse.next()
}

export const config = {
    matcher: '/admin/:path*',
}
