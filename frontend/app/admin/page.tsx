import { supabase } from '@/lib/supabase'

// Force dynamic rendering since we are fetching data
export const dynamic = 'force-dynamic'

async function getLeads() {
    const { data: leads, error } = await supabase
        .from('leads')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(50)

    if (error) {
        console.error('Error fetching leads:', error)
        return []
    }
    return leads
}

export default async function AdminDashboard() {
    const leads = await getLeads()

    return (
        <div className="px-4 py-4 sm:px-0">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Leads Recientes</h1>
                <span className="bg-blue-100 text-blue-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded">
                    {leads.length} Leads
                </span>
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-lg border border-gray-200">
                <ul role="list" className="divide-y divide-gray-200">
                    {leads.length === 0 ? (
                        <li className="px-4 py-12 text-center text-gray-500">
                            <p className="text-lg">No hay leads registrados aún.</p>
                            <p className="text-sm mt-2">Envía un mensaje al bot para empezar.</p>
                        </li>
                    ) : (
                        leads.map((lead) => (
                            <li key={lead.id} className="hover:bg-gray-50 transition cursor-pointer">
                                <div className="px-4 py-4 sm:px-6">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-medium text-blue-600 truncate">{lead.nombre || 'Sin nombre'}</p>
                                        <div className="ml-2 flex-shrink-0 flex">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${lead.fsm_state === 'AGENDADO' ? 'bg-green-100 text-green-800' :
                                                    lead.fsm_state === 'DESCARTADO' ? 'bg-red-100 text-red-800' :
                                                        lead.fsm_state === 'CIERRE' ? 'bg-indigo-100 text-indigo-800' :
                                                            'bg-yellow-100 text-yellow-800'
                                                }`}>
                                                {lead.fsm_state}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="mt-2 sm:flex sm:justify-between">
                                        <div className="sm:flex">
                                            <p className="flex items-center text-sm text-gray-500">
                                                <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3l-2.583 2.583a.25.25 0 01-.417 0L8 15.5h-2a2 2 0 01-2-2V4zm2 2a1 1 0 100 2 1 1 0 000-2z" clipRule="evenodd" />
                                                </svg>
                                                {lead.empresa || 'Empresa N/A'}
                                            </p>
                                            <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                                                <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                                                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                                                </svg>
                                                {lead.phone_number}
                                            </p>
                                        </div>
                                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                            <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 00-1-1H6zm1 2h6v1H7V4zm0 3h6a1 1 0 110 2H7a1 1 0 110-2z" clipRule="evenodd" />
                                            </svg>
                                            <p>
                                                Score: <span className="font-bold text-gray-900">{lead.bant_score}</span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        ))
                    )}
                </ul>
            </div>
        </div>
    )
}
