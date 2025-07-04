import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('usuarios')
  const [showEditModal, setShowEditModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({})
  const [actionLoading, setActionLoading] = useState(false)

  // Configuración de las pestañas con sus respectivos endpoints
  const tabs = {
    usuarios: {
      label: 'Usuarios',
      endpoint: 'http://127.0.0.1:5000/api/usuarios',
      columns: [
        { key: 'id', label: 'ID', render: (value) => `#${value.toString().padStart(3, '0')}`, editable: false },
        { key: 'nombre', label: 'Nombre', editable: true, type: 'text' },
        { key: 'correo', label: 'Correo Electrónico', editable: true, type: 'email' },
      ]
    },
    administradores: {
      label: 'Editores',
      endpoint: 'http://127.0.0.1:5000/api/editors',
      columns: [
        { key: 'id', label: 'ID', render: (value) => `#${value.toString().padStart(3, '0')}`, editable: false },
        { key: 'nombre', label: 'Nombre', editable: true, type: 'text' },
        { key: 'correo', label: 'Correo Electrónico', render: (value) => `${value}`, editable: true, type: 'email' },
      ]
    },
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        const currentTab = tabs[activeTab]
        const response = await fetch(currentTab.endpoint)
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const result = await response.json()
        setData(result)
      } catch (error) {
        console.error('Fetch error:', error)
        setError(error.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [activeTab])

  const LoadingSpinner = () => (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <div className="loading-text">Cargando datos...</div>
    </div>
  )

  const ErrorDisplay = ({ message }) => (
    <div className="error-container">
      <div className="error-title">Error al cargar los datos</div>
      <div className="error-message">{message}</div>
    </div>
  )

  const EmptyState = () => (
    <div className="empty-state">
      <h3>No hay {tabs[activeTab].label.toLowerCase()} disponibles</h3>
      <p>No se encontraron datos para mostrar en este momento.</p>
    </div>
  )

  const handleTabChange = (tabKey) => {
    setActiveTab(tabKey)
    setShowEditModal(false)
    setShowCreateModal(false)
    setEditingItem(null)
    setFormData({})
  }

  // Función para manejar la edición de un elemento
  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({ ...item })
    setShowEditModal(true)
  }

  // Función para manejar la creación de un nuevo elemento
  const handleCreate = () => {
    setEditingItem(null)
    setFormData({})
    setShowCreateModal(true)
  }

  // Función para manejar la eliminación de un elemento
  const handleDelete = async (item) => {
    if (!window.confirm(`¿Estás seguro de que deseas eliminar este ${tabs[activeTab].label.toLowerCase()}?`)) {
      return
    }

    setActionLoading(true)
    try {
      const currentTab = tabs[activeTab]
      const response = await fetch(`${currentTab.endpoint}/${item.id}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }

      // Actualizar la lista local eliminando el elemento
      setData(prevData => prevData.filter(dataItem => dataItem.id !== item.id))
      
      // Mostrar mensaje de éxito (opcional)
      alert(`${tabs[activeTab].label.slice(0, -1)} eliminado exitosamente`)
      
    } catch (error) {
      console.error('Delete error:', error)
      alert(`Error al eliminar: ${error.message}`)
    } finally {
      setActionLoading(false)
    }
  }

  // Función para guardar los cambios de edición
  const handleSaveEdit = async () => {
    setActionLoading(true)
    try {
      const currentTab = tabs[activeTab]
      const response = await fetch(`${currentTab.endpoint}/${editingItem.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`)
      }

      const updatedItem = await response.json()
      
      // Actualizar la lista local con el elemento modificado
      setData(prevData => 
        prevData.map(item => 
          item.id === editingItem.id ? updatedItem : item
        )
      )

      setShowEditModal(false)
      setEditingItem(null)
      alert(`${tabs[activeTab].label.slice(0, -1)} actualizado exitosamente`)
      
    } catch (error) {
      console.error('Update error:', error)
      alert(`Error al actualizar: ${error.message}`)
    } finally {
      setActionLoading(false)
    }
  }

  // Función para guardar un nuevo elemento
  const handleSaveCreate = async () => {
    // Validaciones del lado del cliente
    const currentTab = tabs[activeTab]
    const requiredFields = currentTab.columns.filter(col => col.editable)
    
    for (const field of requiredFields) {
      if (!formData[field.key] || formData[field.key].trim() === '') {
        alert(`El campo ${field.label} es requerido`)
        return
      }
    }

    // Validación específica para contraseña
    if (activeTab === 'usuarios' && formData.contraseña && formData.contraseña.length < 6) {
      alert('La contraseña debe tener al menos 6 caracteres')
      return
    }

    setActionLoading(true)
    try {
      const currentTab = tabs[activeTab]
      const response = await fetch(currentTab.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`)
      }

      const newItem = await response.json()
      
      // Agregar el nuevo elemento a la lista local
      setData(prevData => [...prevData, newItem])

      setShowCreateModal(false)
      setFormData({})
      alert(`${tabs[activeTab].label.slice(0, -1)} creado exitosamente`)
      
    } catch (error) {
      console.error('Create error:', error)
      alert(`Error al crear: ${error.message}`)
    } finally {
      setActionLoading(false)
    }
  }

  // Función para manejar cambios en el formulario
  const handleFormChange = (key, value) => {
    setFormData(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const renderTableHeaders = () => {
    const currentTab = tabs[activeTab]
    return [
      ...currentTab.columns
        .filter(column => column.showInTable !== false)
        .map((column) => (
          <th key={column.key}>{column.label}</th>
        )),
      <th key="actions" className="actions-column">Acciones</th>
    ]
  }

  const renderTableRow = (item) => {
    const currentTab = tabs[activeTab]
    return (
      <tr key={item.id}>
        {currentTab.columns
          .filter(column => column.showInTable !== false)
          .map((column) => {
            const value = item[column.key]
            const displayValue = column.render ? column.render(value) : value
            return (
              <td key={column.key} className={`${activeTab}-${column.key}`}>
                {displayValue}
              </td>
            )
          })}
        <td className="actions-cell">
          <div className="action-buttons">
            <button
              className="edit-btn"
              onClick={() => handleEdit(item)}
              disabled={actionLoading}
              title="Editar"
            >
              ✏️
            </button>
            <button
              className="delete-btn"
              onClick={() => handleDelete(item)}
              disabled={actionLoading}
              title="Eliminar"
            >
              🗑️
            </button>
          </div>
        </td>
      </tr>
    )
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>Sistema de Gestión de Usuarios SIGIC</h1>
      </header>

      {/* Menú de navegación por pestañas */}
      <nav className="navigation-tabs">
        {Object.entries(tabs).map(([key, tab]) => (
          <button
            key={key}
            className={`tab-button ${activeTab === key ? 'active' : ''}`}
            onClick={() => handleTabChange(key)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <div className="table-container">
        <div className="table-header">
          <h2 className="table-title">Lista de {tabs[activeTab].label}</h2>
          <div className="table-header-actions">
            <button
              className="add-btn"
              onClick={handleCreate}
              disabled={actionLoading}
              title={`Agregar ${tabs[activeTab].label.slice(0, -1)}`}
            >
              ➕ Agregar {tabs[activeTab].label.slice(0, -1)}
            </button>
            {data.length > 0 && (
              <div className="user-count">
                {data.length} {tabs[activeTab].label.toLowerCase()}{data.length !== 1 ? '' : ''}
              </div>
            )}
          </div>
        </div>

        {loading && <LoadingSpinner />}
        
        {error && <ErrorDisplay message={error} />}
        
        {!loading && !error && data.length === 0 && <EmptyState />}
        
        {!loading && !error && data.length > 0 && (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  {renderTableHeaders()}
                </tr>
              </thead>
              <tbody>
                {data.map((item) => renderTableRow(item))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal de Edición */}
      {showEditModal && editingItem && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Editar {tabs[activeTab].label.slice(0, -1)}</h3>
              <button 
                className="modal-close"
                onClick={() => setShowEditModal(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              {tabs[activeTab].columns
                .filter(column => column.editable)
                .map((column) => (
                  <div key={column.key} className="form-group">
                    <label htmlFor={column.key}>{column.label}:</label>
                    <input
                      id={column.key}
                      type={column.type || 'text'}
                      value={formData[column.key] || ''}
                      onChange={(e) => handleFormChange(column.key, e.target.value)}
                      className="form-input"
                      placeholder={`Ingresa ${column.label.toLowerCase()}`}
                    />
                  </div>
                ))}
            </div>
            
            <div className="modal-footer">
              <button
                className="btn-cancel"
                onClick={() => setShowEditModal(false)}
                disabled={actionLoading}
              >
                Cancelar
              </button>
              <button
                className="btn-save"
                onClick={handleSaveEdit}
                disabled={actionLoading}
              >
                {actionLoading ? 'Guardando...' : 'Guardar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Creación */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Agregar {tabs[activeTab].label.slice(0, -1)}</h3>
              <button 
                className="modal-close"
                onClick={() => setShowCreateModal(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              {tabs[activeTab].columns
                .filter(column => column.editable)
                .map((column) => (
                  <div key={column.key} className="form-group">
                    <label htmlFor={`create-${column.key}`}>{column.label}:</label>
                    <input
                      id={`create-${column.key}`}
                      type={column.type || 'text'}
                      value={formData[column.key] || ''}
                      onChange={(e) => handleFormChange(column.key, e.target.value)}
                      className="form-input"
                      placeholder={`Ingresa ${column.label.toLowerCase()}`}
                    />
                  </div>
                ))}
            </div>
            
            <div className="modal-footer">
              <button
                className="btn-cancel"
                onClick={() => setShowCreateModal(false)}
                disabled={actionLoading}
              >
                Cancelar
              </button>
              <button
                className="btn-save"
                onClick={handleSaveCreate}
                disabled={actionLoading}
              >
                {actionLoading ? 'Creando...' : 'Crear'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
