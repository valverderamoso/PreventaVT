import React, { useState, useEffect, useMemo } from 'react';
import { 
  Calculator, HardHat, Truck, FileText, AlertTriangle, Settings, 
  Calendar, Sparkles, BrainCircuit, Loader2, Database, 
  Plus, Trash2, Save, UserCheck, Tags, LayoutGrid, 
  ChevronDown, ChevronRight, Filter, SortAsc, DollarSign, X,
  Clock, MapPin, Network, GitBranch
} from 'lucide-react';

// ==========================================
// 1. DATA GEOGRÁFICA (MOCK EXTENDIDO)
// ==========================================
const PERU_DATA = {
  "Lima": {
    "Lima": ["Miraflores", "San Isidro", "Santiago de Surco", "La Molina", "San Borja", "Cercado de Lima"],
    "Cañete": ["Asia", "Mala", "Chilca", "San Vicente"],
    "Huaral": ["Huaral", "Chancay"]
  },
  "Arequipa": {
    "Arequipa": ["Cayma", "Yanahuara", "Cerro Colorado"],
    "Islay": ["Mollendo", "Mejia"]
  },
  "Cusco": {
    "Cusco": ["Wanchaq", "San Jerónimo", "San Sebastián"],
    "Urubamba": ["Ollantaytambo", "Machupicchu"]
  },
  "La Libertad": {
    "Trujillo": ["Trujillo", "Victor Larco", "Huanchaco"],
    "Pacasmayo": ["Pacasmayo", "San Pedro de Lloc"]
  },
  "Piura": {
    "Piura": ["Piura", "Castilla"],
    "Talara": ["Pariñas", "Máncora"]
  },
  // ... Se puede extender
};

const DEPARTAMENTOS_LIST = Object.keys(PERU_DATA);

// ==========================================
// 2. CONFIGURACIÓN & DATOS MAESTROS
// ==========================================
const apiKey = ""; 

const INITIAL_DB_PARAMETROS = [
  { id: 'P1', grupo: 'Materiales', parametro: 'FactorReservaCable', valor: 1.1, unidad: 'factor', desc: 'Reserva 10% cables' },
  { id: 'P2', grupo: 'Materiales', parametro: 'FactorReservaDucteria', valor: 1.05, unidad: 'factor', desc: 'Reserva 5% ductos' },
  { id: 'P3', grupo: 'ManoObra', parametro: 'ProdCamarasEstandar', valor: 4, unidad: 'und/dia', desc: 'Instalación cámaras < 4m' },
  { id: 'P7', grupo: 'Gastos Generales', parametro: 'ViaticoDiarioProvincia', valor: 180, unidad: 'S/ dia', desc: 'Hospedaje + Alimentos' },
  { id: 'P8', grupo: 'Gastos Generales', parametro: 'MovilidadLima', valor: 30, unidad: 'S/ dia', desc: 'Pasajes locales' },
];

const INITIAL_DB_ITEMS = [
  // EQUIPOS
  { id: 'E1', modulo: 'Equipo', categoria: 'CCTV', descripcion: 'Cámara Bullet IP 4MP IR50m Hikvision DS-2CD2T43', marca: 'Hikvision', modelo: 'DS-2CD2T43', costo: 450, unidad: 'UND', tags: ['CCTV'] },
  { id: 'E2', modulo: 'Equipo', categoria: 'CCTV', descripcion: 'Cámara Domo IP 4MP IK10 Hikvision DS-2CD2143', marca: 'Hikvision', modelo: 'DS-2CD2143', costo: 480, unidad: 'UND', tags: ['CCTV'] },
  { id: 'E3', modulo: 'Equipo', categoria: 'CCTV', descripcion: 'NVR 32 Canales 4K Hikvision DS-7732NI', marca: 'Hikvision', modelo: 'DS-7732NI', costo: 1200, unidad: 'UND', tags: ['CCTV'] },
  { id: 'E4', modulo: 'Equipo', categoria: 'Networking', descripcion: 'Switch Cisco CBS350-24P-4G 24 Puertos PoE+', marca: 'Cisco', modelo: 'CBS350-24P', costo: 1800, unidad: 'UND', tags: ['SWITCH&WIFI'] },
  { id: 'E5', modulo: 'Equipo', categoria: 'Energia', descripcion: 'UPS APC 3KVA Online SRV3K', marca: 'APC', modelo: 'SRV3K', costo: 2500, unidad: 'UND', tags: ['ENERGIA'] },
  
  // MATERIALES
  { id: 'M1', modulo: 'MATERIAL', categoria: 'Infraestructura', descripcion: 'Tubería EMT 3/4 pulgada x 3m', marca: 'Generico', modelo: '-', costo: 25, unidad: 'TIRA', tags: ['CCTV'] },
  { id: 'M2', modulo: 'MATERIAL', categoria: 'Cableado', descripcion: 'Cable UTP Cat6 LSZH Panduit', marca: 'Panduit', modelo: 'NUC6', costo: 2.50, unidad: 'M', tags: ['CCTV'] },
  { id: 'M3', modulo: 'MATERIAL', categoria: 'Ferreteria', descripcion: 'Caja de paso 100x100x50 PVC', marca: 'Generico', modelo: '-', costo: 8, unidad: 'UND', tags: ['CCTV'] },
  { id: 'M4', modulo: 'MATERIAL', categoria: 'Infraestructura', descripcion: 'Canaleta 40x25 con adhesivo', marca: 'Dexson', modelo: '-', costo: 15, unidad: 'M', tags: ['CCTV'] },
  
  // MANO DE OBRA
  { id: 'MO1', modulo: 'MANO_OBRA', categoria: 'Técnico', descripcion: 'Técnico Nivel 1 (Básico)', marca: '-', modelo: '-', costo: 150, unidad: 'DIA', eficiencia: 0.8 },
  { id: 'MO2', modulo: 'MANO_OBRA', categoria: 'Técnico', descripcion: 'Técnico Nivel 2 (Especialista)', marca: '-', modelo: '-', costo: 250, unidad: 'DIA', eficiencia: 1.0 },
];

const SOLUCION_OPTIONS = ['CCTV', 'ACCESO', 'ALARMA', 'INCENDIO', 'CABLEADO', 'ENERGIA', 'SWITCH&WIFI'];

// ==========================================
// 3. COMPONENTES UI PRINCIPAL
// ==========================================

export default function PreventaApp() {
  // --- STATE MAESTROS ---
  const [dbItems, setDbItems] = useState(INITIAL_DB_ITEMS);
  const [dbParametros, setDbParametros] = useState(INITIAL_DB_PARAMETROS);
  
  // Criterios ahora tienen parentId para estructura de arbol
  // Parents reservador: 'root', 'cat-equipos', 'cat-materiales', 'cat-mo', 'cat-gg'
  const [criteriosAdicionales, setCriteriosAdicionales] = useState([]); 

  // --- STATE INPUTS ---
  const [inputs, setInputs] = useState({
    proyectoNombre: 'Nuevo Proyecto',
    fechaInicio: new Date().toISOString().split('T')[0],
    soluciones: ['CCTV'],
    departamento: 'Lima',
    provincia: 'Lima',
    distrito: 'Miraflores', // Nuevo campo
    margenEquipos: 30,
    margenMateriales: 35,
    margenMO: 40,
    margenGG: 15,
  });

  // --- STATE TABLAS EDITABLES ---
  const [equipos, setEquipos] = useState([]);
  const [materiales, setMateriales] = useState([]);
  const [cuadrillas, setCuadrillas] = useState([
    { id: 1, nombre: 'Cuadrilla Principal', sede: 'Sede Central', inicioDia: 0, recursos: [] }
  ]);
  
  // --- STATE UI & IA ---
  const [activeTab, setActiveTab] = useState('resumen');
  const [aiLoading, setAiLoading] = useState(false);
  const [filterModulo, setFilterModulo] = useState('Todos');
  const [filterText, setFilterText] = useState('');

  // --- HELPERS DB ---
  const getParam = (name) => {
    const p = dbParametros.find(x => x.parametro === name);
    return p ? parseFloat(p.valor) : 0;
  };
  const updateParam = (id, newVal) => {
    setDbParametros(dbParametros.map(p => p.id === id ? {...p, valor: newVal} : p));
  };

  // --- LÓGICA GEO DINÁMICA ---
  const handleDepartamentoChange = (e) => {
    const dpto = e.target.value;
    const firstProv = PERU_DATA[dpto] ? Object.keys(PERU_DATA[dpto])[0] : '';
    const firstDist = (PERU_DATA[dpto] && firstProv) ? PERU_DATA[dpto][firstProv][0] : '';
    
    setInputs(prev => ({
        ...prev, 
        departamento: dpto,
        provincia: firstProv,
        distrito: firstDist
    }));
  };

  const handleProvinciaChange = (e) => {
    const prov = e.target.value;
    const firstDist = PERU_DATA[inputs.departamento][prov][0] || '';
    setInputs(prev => ({ ...prev, provincia: prov, distrito: firstDist }));
  };

  // --- LÓGICA EQUIPOS ---
  const addEquipo = (itemDB = null) => {
    const base = itemDB || { descripcion: '', marca: '', modelo: '', costo: 0, unidad: 'UND' };
    setEquipos([...equipos, {
        id: Date.now() + Math.random(),
        ...base,
        cantidad: 1,
        altura: 'Estandar',
        manual: !itemDB
    }]);
  };
  
  // Actualizar fila equipo: Si cambia descripción desde dropdown, autocompletar
  const updateEquipoRow = (id, field, value) => {
    if (field === 'descripcion') {
        // Buscar si existe coincidencia exacta en BD Equipos
        const match = dbItems.find(i => i.descripcion === value && i.modulo === 'Equipo');
        if (match) {
            setEquipos(prev => prev.map(item => item.id === id ? { 
                ...item, descripcion: value, marca: match.marca, modelo: match.modelo, costo: match.costo, unidad: match.unidad 
            } : item));
            return;
        }
    }
    setEquipos(prev => prev.map(item => item.id === id ? { ...item, [field]: value } : item));
  };

  // --- LÓGICA MATERIALES & IA ---
  const addMaterial = () => {
    setMateriales([...materiales, {
        id: Date.now() + Math.random(),
        descripcion: '',
        asignadoA: [],
        cantidad: 1,
        costo: 0,
        unidad: 'UND'
    }]);
  };

  const handleSuggestMaterialsAI = async () => {
    if (equipos.length === 0) {
        alert("Primero agrega equipos para poder sugerir materiales complementarios.");
        return;
    }
    setAiLoading(true);
    try {
        const prompt = `Actúa como ingeniero de preventa experto. Tengo estos equipos: 
        ${equipos.map(e => `${e.cantidad}x ${e.descripcion}`).join(', ')}.
        Tipo de Solución: ${inputs.soluciones.join(', ')}.
        
        Genera un JSON con una lista de materiales complementarios necesarios (cables, ductos, conectores, ferretería).
        Usa items genéricos si no hay específicos.
        Formato JSON array: [{ "descripcion": "string", "cantidad": number, "costo_referencial": number, "unidad": "string", "razon": "string" }]`;

        const response = await fetch(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseMimeType: "application/json" } })
            }
        );
        const data = await response.json();
        const suggestions = JSON.parse(data.candidates[0].content.parts[0].text);
        
        // Agregar sugerencias al estado
        const newMaterials = suggestions.map(s => ({
            id: Date.now() + Math.random(),
            descripcion: s.descripcion,
            asignadoA: ['Sugerido IA'],
            cantidad: s.cantidad,
            costo: s.costo_referencial,
            unidad: s.unidad,
            manual: true
        }));
        
        setMateriales(prev => [...prev, ...newMaterials]);
    } catch (e) {
        alert("Error IA: " + e.message);
    } finally {
        setAiLoading(false);
    }
  };

  // --- LÓGICA CRITERIOS (ÁRBOL DE COSTOS) ---
  const getImpactFactor = (parentId) => {
    // Suma los impactos de todos los hijos directos de un nodo
    const children = criteriosAdicionales.filter(c => c.parentId === parentId);
    const totalPercent = children.reduce((acc, c) => acc + (c.impactoPorcentual || 0), 0);
    return 1 + (totalPercent / 100);
  };

  // --- CÁLCULOS PRINCIPALES ---
  const resumen = useMemo(() => {
    // 1. Costos Base
    const baseEquipos = equipos.reduce((acc, e) => acc + (e.cantidad * e.costo), 0);
    const baseMateriales = materiales.reduce((acc, m) => acc + (m.cantidad * m.costo), 0);
    
    // MO Base
    let baseMO = 0;
    let totalDiasHombre = 0;
    let maxDiasProyecto = 0;
    cuadrillas.forEach(c => {
        let diasCuadrilla = 0;
        c.recursos.forEach(r => {
            baseMO += r.dias * r.costo;
            totalDiasHombre += r.dias;
            if (r.dias > diasCuadrilla) diasCuadrilla = r.dias;
        });
        const fin = c.inicioDia + diasCuadrilla;
        if (fin > maxDiasProyecto) maxDiasProyecto = fin;
    });
    
    // GG Base
    let baseGG = 0;
    const esLima = inputs.departamento === 'Lima' && inputs.provincia.includes('Lima'); // Lógica simplificada
    if (!esLima) {
        baseGG += totalDiasHombre * getParam('ViaticoDiarioProvincia');
        const numPersonas = cuadrillas.reduce((acc, c) => acc + c.recursos.length, 0);
        baseGG += numPersonas * 200; // Pasaje bus aprox
    } else {
        baseGG += totalDiasHombre * getParam('MovilidadLima');
    }

    // 2. Aplicar Árbol de Criterios
    // Ajuste = Base * (1 + SumaHijosCategoria)
    const costoEquiposAdj = baseEquipos * getImpactFactor('cat-equipos');
    const costoMaterialesAdj = baseMateriales * getImpactFactor('cat-materiales');
    const costoMOAdj = baseMO * getImpactFactor('cat-mo');
    const costoGGAdj = baseGG * getImpactFactor('cat-gg');

    // Suma de ajustados
    const subtotalDirecto = costoEquiposAdj + costoMaterialesAdj + costoMOAdj + costoGGAdj;
    
    // Aplicar criterios Globales (Hijos de root)
    const costoDirectoTotal = subtotalDirecto * getImpactFactor('root');

    // 3. Ventas
    const ventaEquipos = costoEquiposAdj / (1 - (inputs.margenEquipos/100));
    const ventaMateriales = costoMaterialesAdj / (1 - (inputs.margenMateriales/100));
    const ventaMO = costoMOAdj / (1 - (inputs.margenMO/100));
    const ventaGG = costoGGAdj / (1 - (inputs.margenGG/100));
    
    // El sobrecosto por criterios globales se prorratea o suma al final
    const deltaGlobal = costoDirectoTotal - subtotalDirecto;
    const precioVentaTotal = ventaEquipos + ventaMateriales + ventaMO + ventaGG + deltaGlobal;
    const utilidad = precioVentaTotal - costoDirectoTotal;

    // Fechas
    const fechaInicioObj = new Date(inputs.fechaInicio);
    // Ajustar zona horaria chapucero para visualización correcta
    const fechaFinObj = new Date(fechaInicioObj);
    fechaFinObj.setDate(fechaFinObj.getDate() + maxDiasProyecto);

    return { 
        baseEquipos, costoEquiposAdj, ventaEquipos,
        baseMateriales, costoMaterialesAdj, ventaMateriales,
        baseMO, costoMOAdj, ventaMO,
        baseGG, costoGGAdj, ventaGG,
        costoDirectoTotal, precioVentaTotal, utilidad,
        maxDiasProyecto,
        fechaFin: fechaFinObj.toLocaleDateString('es-PE', { day: 'numeric', month: 'short', year: 'numeric' })
    };
  }, [equipos, materiales, cuadrillas, inputs, dbParametros, criteriosAdicionales]);


  // --- COMPONENTES AUXILIARES ---
  const Currency = ({ val, bold, className }) => (
    <span className={`font-mono ${bold ? 'font-bold' : ''} ${className}`}>
        {val?.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' })}
    </span>
  );

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 font-sans text-sm">
      
      {/* HEADER */}
      <header className="bg-white border-b sticky top-0 z-50 px-6 py-3 flex justify-between items-center shadow-sm">
        <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white p-2 rounded-lg shadow-lg">
                <BrainCircuit size={24}/>
            </div>
            <div>
                <h1 className="font-bold text-xl leading-tight text-slate-900">Preventa <span className="text-blue-600">Enterprise</span></h1>
                <div className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Sistema de Ingeniería de Valor</div>
            </div>
        </div>
        <div className="flex items-center gap-8">
            <div className="text-right hidden md:block">
                <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">Total Proyecto (Venta)</div>
                <div className="text-2xl font-black text-slate-800 leading-none tracking-tight">
                    <Currency val={resumen.precioVentaTotal} />
                </div>
                <div className="text-[11px] font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full inline-block mt-1">
                    Utilidad: <Currency val={resumen.utilidad} />
                </div>
            </div>
            <button className="bg-slate-900 text-white px-5 py-2.5 rounded-lg hover:bg-slate-700 flex gap-2 font-medium transition-all shadow-md active:scale-95">
                <Save size={18}/> Guardar
            </button>
        </div>
      </header>

      <main className="max-w-[1800px] mx-auto p-6 grid grid-cols-12 gap-6">
        
        {/* SIDEBAR CONFIGURACIÓN */}
        <aside className="col-span-12 lg:col-span-3 space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-5 border border-slate-200">
                <h3 className="font-bold text-slate-800 flex items-center gap-2 mb-4 border-b pb-3">
                    <Settings size={18} className="text-blue-600"/> Datos Generales
                </h3>
                
                <div className="space-y-4">
                    <div>
                        <label className="block text-xs font-bold text-slate-500 mb-1">Nombre del Proyecto</label>
                        <input className="w-full border border-slate-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all" 
                            value={inputs.proyectoNombre} onChange={e=>setInputs({...inputs, proyectoNombre: e.target.value})} />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="block text-xs font-bold text-slate-500 mb-1">Fecha Inicio</label>
                            <input type="date" className="w-full border border-slate-300 rounded-md p-2 text-xs" 
                                value={inputs.fechaInicio} onChange={e=>setInputs({...inputs, fechaInicio: e.target.value})} />
                        </div>
                        <div>
                            <label className="block text-xs font-bold text-slate-500 mb-1">Soluciones</label>
                            <div className="bg-slate-50 p-2 rounded border text-xs h-[38px] overflow-hidden truncate">
                                {inputs.soluciones.join(', ')}
                            </div>
                        </div>
                    </div>

                    {/* GEO DINÁMICO */}
                    <div className="space-y-3 pt-2 border-t border-slate-100">
                         <div>
                            <label className="block text-xs font-bold text-slate-500 mb-1 flex items-center gap-1"><MapPin size={12}/> Departamento</label>
                            <select className="w-full border border-slate-300 rounded-md p-2 bg-white text-xs" 
                                value={inputs.departamento} onChange={handleDepartamentoChange}>
                                {DEPARTAMENTOS_LIST.map(d => <option key={d} value={d}>{d}</option>)}
                            </select>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-bold text-slate-500 mb-1">Provincia</label>
                                <select className="w-full border border-slate-300 rounded-md p-2 bg-white text-xs" 
                                    value={inputs.provincia} onChange={handleProvinciaChange}>
                                    {inputs.departamento && PERU_DATA[inputs.departamento] && 
                                        Object.keys(PERU_DATA[inputs.departamento]).map(p => <option key={p} value={p}>{p}</option>)
                                    }
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-slate-500 mb-1">Distrito</label>
                                <select className="w-full border border-slate-300 rounded-md p-2 bg-white text-xs" 
                                    value={inputs.distrito} onChange={e => setInputs({...inputs, distrito: e.target.value})}>
                                    {inputs.departamento && inputs.provincia && PERU_DATA[inputs.departamento][inputs.provincia] &&
                                        PERU_DATA[inputs.departamento][inputs.provincia].map(d => <option key={d} value={d}>{d}</option>)
                                    }
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* MARGENES RAPIDOS */}
            <div className="bg-white rounded-xl shadow-sm p-5 border border-slate-200">
                 <h3 className="font-bold text-slate-800 flex items-center gap-2 mb-4 border-b pb-3">
                    <DollarSign size={18} className="text-emerald-600"/> Márgenes Objetivos
                </h3>
                <div className="space-y-3">
                    {[
                        {l: 'Equipos', k: 'margenEquipos'}, 
                        {l: 'Materiales', k: 'margenMateriales'}, 
                        {l: 'Mano de Obra', k: 'margenMO'}, 
                        {l: 'Gastos G.', k: 'margenGG'}
                    ].map((m) => (
                        <div key={m.k} className="flex justify-between items-center">
                            <label className="text-xs text-slate-600">{m.l}</label>
                            <div className="flex items-center gap-1">
                                <input type="number" className="w-12 text-right border rounded p-1 text-xs font-bold text-slate-700 focus:ring-1 focus:ring-blue-500"
                                    value={inputs[m.k]} onChange={e => setInputs({...inputs, [m.k]: parseFloat(e.target.value)||0})} />
                                <span className="text-xs text-slate-400">%</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </aside>

        {/* WORKSPACE PRINCIPAL */}
        <section className="col-span-12 lg:col-span-9 space-y-6">
            
            {/* TABS NAVEGACION */}
            <nav className="bg-white rounded-xl shadow-sm border border-slate-200 px-2 p-1 flex gap-1 overflow-x-auto">
                {[
                    {id: 'resumen', label: 'Dashboard Financiero', icon: FileText},
                    {id: 'equipos', label: 'Equipos', icon: Calculator},
                    {id: 'materiales', label: 'Materiales', icon: HardHat},
                    {id: 'mo', label: 'Cronograma & MO', icon: Calendar},
                    {id: 'db', label: 'Base de Datos', icon: Database},
                    {id: 'criterios', label: 'Árbol de Costos', icon: GitBranch}
                ].map(tab => (
                    <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center gap-2 px-4 py-2.5 text-xs font-bold rounded-lg transition-all min-w-max ${activeTab === tab.id ? 'bg-slate-800 text-white shadow-md' : 'text-slate-500 hover:bg-slate-100'}`}>
                        <tab.icon size={16}/> {tab.label}
                    </button>
                ))}
            </nav>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 min-h-[600px] p-1 relative overflow-hidden">
                
                {/* ---------- 1. RESUMEN ---------- */}
                {activeTab === 'resumen' && (
                    <div className="p-8 animate-in fade-in duration-300">
                        <div className="flex justify-between items-end mb-6">
                            <h2 className="text-2xl font-bold text-slate-800">Análisis de Rentabilidad</h2>
                            <div className="text-right">
                                <div className="text-sm text-slate-500">Beneficio Neto Estimado</div>
                                <div className="text-3xl font-black text-emerald-600"><Currency val={resumen.utilidad}/></div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                            {/* Tabla Detallada */}
                            <div className="xl:col-span-2 overflow-hidden rounded-xl border border-slate-200">
                                <table className="w-full text-sm">
                                    <thead className="bg-slate-50 text-slate-500 border-b border-slate-200">
                                        <tr>
                                            <th className="p-4 text-left font-semibold">Concepto</th>
                                            <th className="p-4 text-right font-semibold">Costo Base</th>
                                            <th className="p-4 text-right font-semibold text-purple-600">Ajustado (Criterios)</th>
                                            <th className="p-4 text-right font-semibold text-blue-600">Precio Venta</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100">
                                        <tr className="hover:bg-slate-50/50 transition-colors">
                                            <td className="p-4 font-medium text-slate-700 flex items-center gap-2"><Calculator size={16} className="text-slate-400"/> Equipos</td>
                                            <td className="p-4 text-right text-slate-500"><Currency val={resumen.baseEquipos}/></td>
                                            <td className="p-4 text-right font-medium text-purple-700"><Currency val={resumen.costoEquiposAdj}/></td>
                                            <td className="p-4 text-right font-bold text-blue-700"><Currency val={resumen.ventaEquipos}/></td>
                                        </tr>
                                        <tr className="hover:bg-slate-50/50 transition-colors">
                                            <td className="p-4 font-medium text-slate-700 flex items-center gap-2"><HardHat size={16} className="text-slate-400"/> Materiales</td>
                                            <td className="p-4 text-right text-slate-500"><Currency val={resumen.baseMateriales}/></td>
                                            <td className="p-4 text-right font-medium text-purple-700"><Currency val={resumen.costoMaterialesAdj}/></td>
                                            <td className="p-4 text-right font-bold text-blue-700"><Currency val={resumen.ventaMateriales}/></td>
                                        </tr>
                                        <tr className="hover:bg-slate-50/50 transition-colors">
                                            <td className="p-4 font-medium text-slate-700 flex items-center gap-2"><UserCheck size={16} className="text-slate-400"/> Mano de Obra</td>
                                            <td className="p-4 text-right text-slate-500"><Currency val={resumen.baseMO}/></td>
                                            <td className="p-4 text-right font-medium text-purple-700"><Currency val={resumen.costoMOAdj}/></td>
                                            <td className="p-4 text-right font-bold text-blue-700"><Currency val={resumen.ventaMO}/></td>
                                        </tr>
                                        <tr className="hover:bg-slate-50/50 transition-colors">
                                            <td className="p-4 font-medium text-slate-700 flex items-center gap-2"><Truck size={16} className="text-slate-400"/> Gastos Generales</td>
                                            <td className="p-4 text-right text-slate-500"><Currency val={resumen.baseGG}/></td>
                                            <td className="p-4 text-right font-medium text-purple-700"><Currency val={resumen.costoGGAdj}/></td>
                                            <td className="p-4 text-right font-bold text-blue-700"><Currency val={resumen.ventaGG}/></td>
                                        </tr>
                                        <tr className="bg-slate-50 font-bold border-t-2 border-slate-200">
                                            <td className="p-4">TOTAL</td>
                                            <td className="p-4 text-right text-slate-400">-</td>
                                            <td className="p-4 text-right text-purple-900"><Currency val={resumen.costoDirectoTotal}/></td>
                                            <td className="p-4 text-right text-xl text-blue-900"><Currency val={resumen.precioVentaTotal}/></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            {/* Cards KPI */}
                            <div className="space-y-4">
                                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 text-white shadow-lg">
                                    <div className="text-slate-400 text-xs font-bold uppercase mb-2">Costo Directo Ajustado</div>
                                    <div className="text-3xl font-bold mb-1"><Currency val={resumen.costoDirectoTotal}/></div>
                                    <div className="text-xs text-slate-400">Incluye impacto de criterios de riesgo</div>
                                </div>
                                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
                                    <div className="text-slate-400 text-xs font-bold uppercase mb-2">Margen Bruto Promedio</div>
                                    <div className="text-3xl font-bold text-slate-700 mb-1">
                                        {((resumen.utilidad / resumen.precioVentaTotal)*100 || 0).toFixed(1)}%
                                    </div>
                                    <div className="w-full bg-slate-100 rounded-full h-1.5 mt-2">
                                        <div className="bg-blue-600 h-1.5 rounded-full" style={{width: `${(resumen.utilidad / resumen.precioVentaTotal)*100}%`}}></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* ---------- 2. EQUIPOS (LISTA DESPLEGABLE DINAMICA) ---------- */}
                {activeTab === 'equipos' && (
                    <div className="flex flex-col h-full animate-in fade-in">
                        <div className="p-4 border-b flex justify-between items-center bg-slate-50">
                             <div className="text-xs text-slate-500 font-medium">
                                Los cambios se guardan automáticamente. La descripción busca en BD.
                             </div>
                             <button onClick={() => addEquipo()} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-blue-700 transition-colors flex items-center gap-2 shadow-sm">
                                <Plus size={16}/> Agregar Fila
                             </button>
                        </div>
                        <div className="overflow-auto flex-1 p-4">
                            <table className="w-full text-xs border-separate border-spacing-y-1">
                                <thead className="text-slate-400 uppercase font-semibold">
                                    <tr>
                                        <th className="pb-2 pl-2 text-left">Descripción (Seleccionar de BD)</th>
                                        <th className="pb-2 w-24 text-left">Marca</th>
                                        <th className="pb-2 w-24 text-left">Modelo</th>
                                        <th className="pb-2 w-16 text-center">Cant.</th>
                                        <th className="pb-2 w-24 text-right">Unitario</th>
                                        <th className="pb-2 w-24 text-right">Total</th>
                                        <th className="pb-2 w-10"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {equipos.map((item) => (
                                        <tr key={item.id} className="group hover:bg-slate-50 transition-colors">
                                            <td className="border border-slate-200 rounded-l-lg bg-white p-0 relative">
                                                {/* INPUT CON LISTA DESPLEGABLE FILTRADA */}
                                                <input 
                                                    list={`dl-equipos-${item.id}`}
                                                    className="w-full h-full p-3 outline-none rounded-l-lg font-medium text-slate-700 placeholder-slate-300 bg-transparent"
                                                    value={item.descripcion}
                                                    onChange={e => updateEquipoRow(item.id, 'descripcion', e.target.value)} 
                                                    placeholder="Escribe o selecciona..." 
                                                />
                                                <datalist id={`dl-equipos-${item.id}`}>
                                                    {dbItems.filter(i => i.modulo === 'Equipo').map(e => (
                                                        <option key={e.id} value={e.descripcion}>{e.marca} - {e.modelo}</option>
                                                    ))}
                                                </datalist>
                                            </td>
                                            <td className="border-y border-slate-200 bg-white p-2">
                                                <input className="w-full outline-none text-slate-500" value={item.marca} readOnly tabIndex={-1}/>
                                            </td>
                                            <td className="border-y border-slate-200 bg-white p-2">
                                                <input className="w-full outline-none text-slate-500" value={item.modelo} readOnly tabIndex={-1}/>
                                            </td>
                                            <td className="border-y border-slate-200 bg-white p-2">
                                                <input type="number" className="w-full text-center outline-none font-bold text-blue-600 bg-blue-50 rounded" 
                                                    value={item.cantidad} onChange={e => updateEquipoRow(item.id, 'cantidad', parseFloat(e.target.value)||0)} />
                                            </td>
                                            <td className="border-y border-slate-200 bg-white p-2">
                                                <input type="number" className="w-full text-right outline-none" 
                                                    value={item.costo} onChange={e => updateEquipoRow(item.id, 'costo', parseFloat(e.target.value)||0)} />
                                            </td>
                                            <td className="border-y border-slate-200 bg-white p-2 text-right font-mono font-medium text-slate-700">
                                                <Currency val={item.cantidad*item.costo}/>
                                            </td>
                                            <td className="border border-slate-200 rounded-r-lg bg-white p-0 text-center">
                                                <button onClick={() => setEquipos(prev => prev.filter(x => x.id !== item.id))} className="text-slate-300 hover:text-red-500 p-2 w-full h-full"><Trash2 size={16}/></button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* ---------- 3. MATERIALES (IA ASSISTANT) ---------- */}
                {activeTab === 'materiales' && (
                    <div className="flex flex-col h-full p-4 animate-in fade-in">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-bold text-slate-700">Lista de Materiales</h3>
                            <div className="flex gap-2">
                                <button onClick={handleSuggestMaterialsAI} disabled={aiLoading} 
                                    className="bg-purple-600 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-purple-700 transition-colors flex items-center gap-2 shadow-sm disabled:opacity-50">
                                    {aiLoading ? <Loader2 size={16} className="animate-spin"/> : <Sparkles size={16}/>} 
                                    {aiLoading ? 'Analizando...' : 'Sugerir con IA'}
                                </button>
                                <button onClick={addMaterial} className="bg-slate-800 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-slate-900 flex items-center gap-2">
                                    <Plus size={16}/> Agregar
                                </button>
                            </div>
                        </div>
                        <div className="overflow-auto border rounded-lg">
                             <table className="w-full text-xs text-left">
                                <thead className="bg-slate-50 text-slate-500">
                                    <tr>
                                        <th className="p-3 w-1/2">Descripción</th>
                                        <th className="p-3 text-center">Cant.</th>
                                        <th className="p-3 text-right">Unitario</th>
                                        <th className="p-3 text-right">Total</th>
                                        <th className="p-3 w-10"></th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {materiales.map((item) => (
                                        <tr key={item.id} className="hover:bg-slate-50">
                                            <td className="p-2">
                                                <input 
                                                    className="w-full border p-2 rounded bg-white outline-none font-medium text-slate-700 focus:border-blue-500" 
                                                    value={item.descripcion} 
                                                    onChange={e => setMateriales(prev => prev.map(m => m.id === item.id ? { ...m, descripcion: e.target.value } : m))} 
                                                />
                                            </td>
                                            <td className="p-2"><input type="number" className="w-full text-center border rounded p-2" value={item.cantidad} onChange={e=>setMateriales(prev => prev.map(m => m.id === item.id ? { ...m, cantidad: parseFloat(e.target.value)||0 } : m))}/></td>
                                            <td className="p-2"><input type="number" className="w-full text-right border rounded p-2" value={item.costo} onChange={e=>setMateriales(prev => prev.map(m => m.id === item.id ? { ...m, costo: parseFloat(e.target.value)||0 } : m))}/></td>
                                            <td className="p-2 text-right font-bold text-slate-700"><Currency val={item.cantidad * item.costo}/></td>
                                            <td className="p-2 text-center"><button onClick={() => setMateriales(prev => prev.filter(x => x.id !== item.id))} className="text-red-400"><Trash2 size={14}/></button></td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* ---------- 4. MO & GANTT ---------- */}
                {activeTab === 'mo' && (
                    <div className="flex flex-col h-full p-6 animate-in fade-in space-y-8">
                        
                        {/* HEADER GANTT */}
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap gap-6 items-center">
                            <div className="flex items-center gap-3">
                                <div className="bg-blue-100 p-2 rounded-lg text-blue-700"><Calendar size={20}/></div>
                                <div>
                                    <div className="text-xs text-slate-400 uppercase font-bold">Inicio Proyecto</div>
                                    <div className="font-bold text-slate-800">{inputs.fechaInicio}</div>
                                </div>
                            </div>
                            <div className="w-px h-8 bg-slate-100"></div>
                            <div className="flex items-center gap-3">
                                <div className="bg-emerald-100 p-2 rounded-lg text-emerald-700"><Clock size={20}/></div>
                                <div>
                                    <div className="text-xs text-slate-400 uppercase font-bold">Duración Est.</div>
                                    <div className="font-bold text-emerald-700">{resumen.maxDiasProyecto} días hábiles</div>
                                </div>
                            </div>
                            <div className="w-px h-8 bg-slate-100"></div>
                            <div className="flex items-center gap-3">
                                <div className="bg-rose-100 p-2 rounded-lg text-rose-700"><MapPin size={20}/></div>
                                <div>
                                    <div className="text-xs text-slate-400 uppercase font-bold">Fin Estimado</div>
                                    <div className="font-bold text-rose-700">{resumen.fechaFin}</div>
                                </div>
                            </div>
                        </div>

                        {/* CUADRILLAS */}
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <h3 className="font-bold text-slate-800">Planificación de Recursos</h3>
                                <button onClick={() => setCuadrillas([...cuadrillas, {id: Date.now(), nombre: 'Nueva Tarea', sede: 'Sede X', inicioDia: 0, recursos: []}])} 
                                    className="bg-slate-800 text-white px-4 py-2 rounded-lg text-xs hover:bg-slate-900 flex gap-2 items-center">
                                    <Plus size={16}/> Agregar Tarea
                                </button>
                            </div>
                            {/* ... (Logica de cuadrillas igual que antes, simplificado para display) ... */}
                            {cuadrillas.map((c) => (
                                <div key={c.id} className="border border-slate-200 rounded-lg p-4 bg-slate-50 relative hover:shadow-md transition-shadow">
                                    <div className="flex gap-4 mb-3 border-b border-slate-200 pb-3">
                                        <input className="font-bold bg-transparent border-b border-transparent focus:border-blue-500 outline-none" value={c.nombre} onChange={e => setCuadrillas(prev => prev.map(x => x.id === c.id ? {...x, nombre: e.target.value}: x))} />
                                        <input className="text-xs bg-white border rounded px-2" value={c.sede} onChange={e => setCuadrillas(prev => prev.map(x => x.id === c.id ? {...x, sede: e.target.value}: x))} />
                                        <div className="flex items-center gap-2 text-xs ml-auto">
                                            <span>Inicia día:</span>
                                            <input type="number" className="w-12 border rounded p-1 text-center font-mono" value={c.inicioDia} onChange={e => setCuadrillas(prev => prev.map(x => x.id === c.id ? {...x, inicioDia: parseInt(e.target.value)||0}: x))} />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        {c.recursos.map(r => (
                                            <div key={r.idInstance} className="flex justify-between items-center bg-white p-2 rounded border border-slate-200 text-xs">
                                                <span>{r.descripcion}</span>
                                                <div className="flex gap-2 items-center">
                                                    <input type="number" className="w-12 border rounded p-1 text-center" value={r.dias} onChange={e => setCuadrillas(prev => prev.map(cur => cur.id === c.id ? {...cur, recursos: cur.recursos.map(res => res.idInstance === r.idInstance ? {...res, dias: parseFloat(e.target.value)}: res)} : cur))} />
                                                    <span className="text-slate-400">días</span>
                                                </div>
                                            </div>
                                        ))}
                                        <button className="text-xs text-blue-600 font-medium hover:underline mt-2" 
                                            onClick={() => {
                                                const mo = dbItems.find(i => i.modulo === 'MANO_OBRA'); // Mock add simple
                                                if(mo) setCuadrillas(prev => prev.map(cur => cur.id === c.id ? {...cur, recursos: [...cur.recursos, {...mo, idInstance: Date.now(), dias: 5}]} : cur));
                                            }}>
                                            + Añadir Recurso Estándar
                                        </button>
                                    </div>
                                    <button onClick={() => setCuadrillas(prev => prev.filter(x => x.id !== c.id))} className="absolute top-4 right-4 text-slate-300 hover:text-red-500"><Trash2 size={16}/></button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* ---------- 6. CRITERIOS (ÁRBOL RELACIONAL) ---------- */}
                {activeTab === 'criterios' && (
                    <div className="p-8 animate-in fade-in h-full overflow-auto bg-slate-50 relative">
                         <div className="flex justify-between items-start mb-8">
                            <div>
                                <h2 className="font-bold text-xl text-slate-800">Árbol de Costos y Riesgos</h2>
                                <p className="text-sm text-slate-500">Define criterios que impactan en categorías específicas o en el total global.</p>
                            </div>
                            <button onClick={() => setCriteriosAdicionales([...criteriosAdicionales, {id: Date.now(), nombre: 'Nuevo Factor', impactoPorcentual: 5, parentId: 'root'}])} 
                                className="bg-slate-800 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-slate-900 flex gap-2 items-center">
                                <GitBranch size={16}/> Agregar Nodo
                            </button>
                        </div>

                        {/* VISUALIZACIÓN DE ÁRBOL */}
                        <div className="flex flex-col items-center gap-12 min-w-[900px]">
                            
                            {/* ROOT */}
                            <div className="relative z-10">
                                <div className="bg-slate-900 text-white p-4 rounded-xl shadow-xl text-center w-64 border-2 border-slate-700">
                                    <div className="font-bold text-lg">COSTO TOTAL</div>
                                    <div className="text-[10px] text-slate-400 uppercase tracking-widest mt-1">Raíz del Proyecto</div>
                                </div>
                                {/* Conectores Root -> Categorias */}
                                <div className="absolute top-full left-1/2 w-px h-8 bg-slate-300 -translate-x-1/2"></div>
                                <div className="absolute top-[calc(100%+32px)] left-1/2 w-[600px] h-px bg-slate-300 -translate-x-1/2"></div>
                            </div>

                            {/* NIVEL 2: CATEGORIAS */}
                            <div className="flex justify-between w-[800px] relative z-10">
                                {[
                                    {id: 'cat-equipos', label: 'Equipos', color: 'border-blue-500 text-blue-700 bg-blue-50'},
                                    {id: 'cat-materiales', label: 'Materiales', color: 'border-amber-500 text-amber-700 bg-amber-50'},
                                    {id: 'cat-mo', label: 'Mano de Obra', color: 'border-emerald-500 text-emerald-700 bg-emerald-50'},
                                    {id: 'cat-gg', label: 'Gastos G.', color: 'border-rose-500 text-rose-700 bg-rose-50'}
                                ].map(cat => (
                                    <div key={cat.id} className="flex flex-col items-center relative">
                                        <div className="h-8 w-px bg-slate-300 -mt-8 mb-2"></div>
                                        <div className={`border-2 rounded-lg p-3 w-40 text-center shadow-sm font-bold ${cat.color}`}>
                                            {cat.label}
                                        </div>
                                        
                                        {/* CRITERIOS ASIGNADOS A ESTA CATEGORIA */}
                                        <div className="mt-4 flex flex-col gap-2 w-full">
                                            {criteriosAdicionales.filter(c => c.parentId === cat.id).map(crit => (
                                                <div key={crit.id} className="bg-white border border-slate-200 p-2 rounded shadow-sm text-xs relative group">
                                                    <input className="font-bold w-full outline-none bg-transparent" value={crit.nombre} onChange={e => setCriteriosAdicionales(prev => prev.map(x => x.id === crit.id ? {...x, nombre: e.target.value}: x))} />
                                                    <div className="flex items-center gap-1 mt-1">
                                                        <span className="text-slate-400">Impacto:</span>
                                                        <input type="number" className="w-12 border rounded bg-slate-50 text-center font-bold" value={crit.impactoPorcentual} onChange={e => setCriteriosAdicionales(prev => prev.map(x => x.id === crit.id ? {...x, impactoPorcentual: parseFloat(e.target.value)}: x))} />
                                                        <span>%</span>
                                                    </div>
                                                    <button onClick={() => setCriteriosAdicionales(prev => prev.filter(x => x.id !== crit.id))} className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-0.5 opacity-0 group-hover:opacity-100"><X size={10}/></button>
                                                    <div className="absolute bottom-full left-1/2 w-px h-2 bg-slate-300"></div>
                                                </div>
                                            ))}
                                            <button onClick={() => setCriteriosAdicionales([...criteriosAdicionales, {id: Date.now(), nombre: 'Nuevo Riesgo', impactoPorcentual: 2, parentId: cat.id}])} 
                                                className="text-[10px] text-slate-400 hover:text-blue-600 border border-dashed border-slate-300 rounded p-1 text-center">
                                                + Criterio Hijo
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* NIVEL GLOBAL (Hijos de Root) */}
                            <div className="w-full border-t border-slate-200 pt-6 mt-4 relative">
                                <span className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-slate-50 px-3 text-xs font-bold text-slate-400 uppercase tracking-widest">Factores Globales (Financieros / Riesgo País)</span>
                                <div className="flex justify-center gap-4 flex-wrap">
                                    {criteriosAdicionales.filter(c => c.parentId === 'root').map(crit => (
                                        <div key={crit.id} className="bg-slate-800 text-white p-3 rounded-lg shadow-lg w-48 relative group border border-slate-600">
                                             <input className="font-bold w-full outline-none bg-transparent border-b border-slate-600 mb-2" value={crit.nombre} onChange={e => setCriteriosAdicionales(prev => prev.map(x => x.id === crit.id ? {...x, nombre: e.target.value}: x))} />
                                             <div className="flex items-center justify-between">
                                                <span className="text-xs text-slate-400">Impacto Total:</span>
                                                <div className="font-bold text-emerald-400">+{crit.impactoPorcentual}%</div>
                                                <input type="number" className="hidden" value={crit.impactoPorcentual} onChange={e => setCriteriosAdicionales(prev => prev.map(x => x.id === crit.id ? {...x, impactoPorcentual: parseFloat(e.target.value)}: x))} />
                                             </div>
                                             <button onClick={() => setCriteriosAdicionales(prev => prev.filter(x => x.id !== crit.id))} className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100"><X size={12}/></button>
                                        </div>
                                    ))}
                                    <button onClick={() => setCriteriosAdicionales([...criteriosAdicionales, {id: Date.now(), nombre: 'Inflación / Contingencia', impactoPorcentual: 3, parentId: 'root'}])} 
                                        className="w-48 border-2 border-dashed border-slate-300 rounded-lg flex items-center justify-center text-slate-400 text-xs font-bold hover:border-slate-500 hover:text-slate-600 h-[86px]">
                                        + Agregar Factor Global
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </section>
      </main>
    </div>
  );
}
