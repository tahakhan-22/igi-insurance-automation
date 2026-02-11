import React, { useState, useEffect } from 'react';
import { clientsApi } from '../../api';
import type { Client, AddressType } from '../../types';

const ClientsForm: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingClient, setEditingClient] = useState<Client | null>(null);
  const [formData, setFormData] = useState<Partial<Client>>({
    name: '',
    address_type: 'Home',
    address: '',
    country: '',
    city: '',
    phone1: '',
    phone2: '',
    fax: '',
    email: '',
  });

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await clientsApi.list();
      setClients(response.data);
    } catch (err: any) {
      console.error('Error loading clients:', err);
      let errorMessage = 'Failed to load clients';
      
      if (err.response) {
        // Server responded with error
        errorMessage = err.response?.data?.detail || `Server error: ${err.response.status}`;
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to server. Please ensure the backend is running.';
      } else {
        // Something else happened
        errorMessage = err.message || 'An unexpected error occurred';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateForm = (): boolean => {
    if (!formData.name?.trim()) {
      setError('Name is required');
      return false;
    }
    if (!formData.address_type) {
      setError('Address type is required');
      return false;
    }
    if (!formData.address?.trim()) {
      setError('Address is required');
      return false;
    }
    if (!formData.country?.trim()) {
      setError('Country is required');
      return false;
    }
    if (!formData.city?.trim()) {
      setError('City is required');
      return false;
    }
    if (formData.email && !isValidEmail(formData.email)) {
      setError('Invalid email format');
      return false;
    }
    return true;
  };

  const isValidEmail = (email: string): boolean => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);
      if (editingClient) {
        await clientsApi.update(editingClient.id, formData);
        setSuccess('Client updated successfully');
      } else {
        await clientsApi.create(formData);
        setSuccess('Client created successfully');
      }
      await loadClients();
      handleCloseModal();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save client');
      console.error('Error saving client:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (client: Client) => {
    setEditingClient(client);
    setFormData({
      name: client.name,
      address_type: client.address_type,
      address: client.address,
      country: client.country,
      city: client.city,
      phone1: client.phone1 || '',
      phone2: client.phone2 || '',
      fax: client.fax || '',
      email: client.email || '',
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this client?')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await clientsApi.delete(id);
      setSuccess('Client deleted successfully');
      await loadClients();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete client');
      console.error('Error deleting client:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingClient(null);
    setFormData({
      name: '',
      address_type: 'Home',
      address: '',
      country: '',
      city: '',
      phone1: '',
      phone2: '',
      fax: '',
      email: '',
    });
    setError(null);
  };

  const handleOpenCreateModal = () => {
    setEditingClient(null);
    setFormData({
      name: '',
      address_type: 'Home',
      address: '',
      country: '',
      city: '',
      phone1: '',
      phone2: '',
      fax: '',
      email: '',
    });
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const filteredClients = clients.filter(client =>
    client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.country.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="clients-form">
      <div className="form-header">
        <h2>Clients Management</h2>
        <button className="btn btn-primary" onClick={handleOpenCreateModal}>
          + Add New Client
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={() => setError(null)} className="alert-close">×</button>
          {error.includes('Cannot connect') && (
            <div style={{ marginTop: '10px' }}>
              <button onClick={loadClients} className="btn btn-secondary" style={{ marginRight: '10px' }}>
                🔄 Retry Connection
              </button>
              <small>Make sure backend is running: docker compose up</small>
            </div>
          )}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
          <button onClick={() => setSuccess(null)} className="alert-close">×</button>
        </div>
      )}

      <div className="search-box">
        <input
          type="text"
          placeholder="Search clients by name, email, city, or country..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading && !showModal ? (
        <div className="loading">Loading clients...</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Address Type</th>
                <th>City</th>
                <th>Country</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredClients.length === 0 ? (
                <tr>
                  <td colSpan={8} className="no-data">
                    {searchTerm ? 'No clients found matching your search' : 'No clients available. Click "Add New Client" to create one.'}
                  </td>
                </tr>
              ) : (
                filteredClients.map(client => (
                  <tr key={client.id}>
                    <td>{client.id}</td>
                    <td><strong>{client.name}</strong></td>
                    <td><span className="badge">{client.address_type}</span></td>
                    <td>{client.city}</td>
                    <td>{client.country}</td>
                    <td>{client.email || '-'}</td>
                    <td>{client.phone1 || '-'}</td>
                    <td className="actions">
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={() => handleEdit(client)}
                        title="Edit"
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => handleDelete(client.id)}
                        title="Delete"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingClient ? 'Edit Client' : 'Create New Client'}</h3>
              <button className="modal-close" onClick={handleCloseModal}>×</button>
            </div>

            <form onSubmit={handleSubmit} className="modal-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="name">Name <span className="required">*</span></label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    placeholder="Enter client name"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="address_type">Address Type <span className="required">*</span></label>
                  <select
                    id="address_type"
                    name="address_type"
                    value={formData.address_type}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="Home">Home</option>
                    <option value="Office">Office</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="address">Address <span className="required">*</span></label>
                <textarea
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  required
                  rows={3}
                  placeholder="Enter complete address"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="country">Country <span className="required">*</span></label>
                  <input
                    type="text"
                    id="country"
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    required
                    placeholder="e.g., Pakistan"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="city">City <span className="required">*</span></label>
                  <input
                    type="text"
                    id="city"
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    required
                    placeholder="e.g., Karachi"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="phone1">Phone 1</label>
                  <input
                    type="tel"
                    id="phone1"
                    name="phone1"
                    value={formData.phone1}
                    onChange={handleInputChange}
                    placeholder="+92-XXX-XXXXXXX"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="phone2">Phone 2</label>
                  <input
                    type="tel"
                    id="phone2"
                    name="phone2"
                    value={formData.phone2}
                    onChange={handleInputChange}
                    placeholder="+92-XXX-XXXXXXX"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="example@domain.com"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="fax">Fax</label>
                  <input
                    type="text"
                    id="fax"
                    name="fax"
                    value={formData.fax}
                    onChange={handleInputChange}
                    placeholder="Fax number"
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={handleCloseModal}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : (editingClient ? 'Update Client' : 'Create Client')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientsForm;
