import { logout } from '../actions'
import Link from 'next/link'

export const metadata = {
    title: 'Mi IA Dashboard',
    description: 'Admin Portal',
}

export default function AdminLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-gray-50 text-gray-900">
            <nav className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center gap-8">
                            <span className="font-bold text-xl text-blue-600">Mi IA Admin</span>
                            <div className="hidden md:flex space-x-4">
                                <Link href="/admin" className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                                    Leads
                                </Link>
                                <Link href="/admin/calendar" className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                                    Calendario
                                </Link>
                            </div>
                        </div>
                        <div className="flex items-center">
                            <form action={logout}>
                                <button className="text-sm text-gray-500 hover:text-red-600 font-medium transition-colors">
                                    Cerrar Sesión
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </nav>
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                {children}
            </main>
        </div>
    )
}
