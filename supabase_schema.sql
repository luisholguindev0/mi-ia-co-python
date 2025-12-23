-- =============================================
-- SCHEMA PARA SUPABASE - Sistema SDR WhatsApp
-- Mi IA Colombia
-- =============================================

-- Tabla principal de leads
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    empresa VARCHAR(200),
    cargo VARCHAR(100),
    ciudad VARCHAR(100),
    email VARCHAR(200),
    puntos_dolor JSONB DEFAULT '[]',
    presupuesto_min BIGINT,
    presupuesto_max BIGINT,
    urgencia VARCHAR(20),
    bant_score INTEGER DEFAULT 0,
    fsm_state VARCHAR(50) DEFAULT 'INICIO',
    extracted_facts JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ,
    message_count INTEGER DEFAULT 0,
    source VARCHAR(50) DEFAULT 'whatsapp'
);

-- Tabla de mensajes
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    direction VARCHAR(10) NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    whatsapp_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Tabla de citas
CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    calendar_event_id VARCHAR(200),
    meeting_link VARCHAR(500),
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 15,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reminder_sent BOOLEAN DEFAULT FALSE
);

-- Tabla de transiciones FSM (para auditoría)
CREATE TABLE IF NOT EXISTS fsm_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    from_state VARCHAR(50),
    to_state VARCHAR(50) NOT NULL,
    trigger_event VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- ÍNDICES
-- =============================================

CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone_number);
CREATE INDEX IF NOT EXISTS idx_leads_state ON leads(fsm_state);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_lead ON messages(lead_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_appointments_scheduled ON appointments(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_appointments_lead ON appointments(lead_id);

-- =============================================
-- FUNCIONES
-- =============================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para leads
DROP TRIGGER IF EXISTS update_leads_updated_at ON leads;
CREATE TRIGGER update_leads_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- ROW LEVEL SECURITY (opcional)
-- =============================================

-- Habilitar RLS si es necesario
-- ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- =============================================
-- VISTAS ÚTILES
-- =============================================

-- Vista de leads con métricas
CREATE OR REPLACE VIEW leads_summary AS
SELECT 
    l.id,
    l.phone_number,
    l.nombre,
    l.empresa,
    l.fsm_state,
    l.bant_score,
    l.message_count,
    l.created_at,
    l.last_message_at,
    COUNT(DISTINCT a.id) as appointments_count,
    MAX(a.scheduled_at) as next_appointment
FROM leads l
LEFT JOIN appointments a ON l.id = a.lead_id AND a.status = 'scheduled'
GROUP BY l.id;

-- Vista de conversaciones activas (últimas 24h)
CREATE OR REPLACE VIEW active_conversations AS
SELECT 
    l.*,
    (SELECT content FROM messages WHERE lead_id = l.id ORDER BY created_at DESC LIMIT 1) as last_message
FROM leads l
WHERE l.last_message_at > NOW() - INTERVAL '24 hours'
    AND l.fsm_state NOT IN ('COMPLETADO', 'DESCARTADO')
ORDER BY l.last_message_at DESC;
