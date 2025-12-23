import { supabase } from '@/lib/supabase'

export const dynamic = 'force-dynamic'

async function getAppointments() {
    const { data, error } = await supabase
        .from('appointments')
        .select(`
            *,
            leads (
                nombre,
                phone_number
            )
        `)
        .order('scheduled_at', { ascending: true })

    if (error) {
        console.error('Error fetching appointments:', error)
        return []
    }
    return data
}

export default async function CalendarPage() {
    const appointments = await getAppointments()

    return (
        <div className="px-4 py-4 sm:px-0">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Calendario de Citas</h1>
                <span className="bg-green-100 text-green-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded">
                    {appointments.length} Citas
                </span>
            </div>

            {appointments.length === 0 ? (
                <div className="bg-white shadow rounded-lg p-12 text-center text-gray-500 border border-gray-200">
                    <p>No hay citas agendadas aún.</p>
                </div>
            ) : (
                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {appointments.map((apt: any) => (
                        <div key={apt.id} className="bg-white overflow-hidden shadow rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="flex items-center mb-4">
                                    <div className="flex-shrink-0 bg-blue-100 rounded-md p-2">
                                        <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                    </div>
                                    <div className="ml-4">
                                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                                            {new Date(apt.scheduled_at).toLocaleDateString()}
                                        </h3>
                                        <p className="text-sm text-gray-500">
                                            {new Date(apt.scheduled_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </p>
                                    </div>
                                </div>
                                <dl>
                                    <div className="mb-4">
                                        <dt className="text-sm font-medium text-gray-500">Cliente</dt>
                                        <dd className="mt-1 text-sm text-gray-900 font-semibold">{apt.leads?.nombre || 'Desconocido'}</dd>
                                        <dd className="text-sm text-gray-500">{apt.leads?.phone_number}</dd>
                                    </div>
                                    {apt.meeting_link && (
                                        <div>
                                            <a href={apt.meeting_link} target="_blank" rel="noopener noreferrer" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 w-full justify-center">
                                                Unirse a Reunión
                                            </a>
                                        </div>
                                    )}
                                </dl>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
