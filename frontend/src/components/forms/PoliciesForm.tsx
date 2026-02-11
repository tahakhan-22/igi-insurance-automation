import React, { useState, useEffect } from 'react';
import { policiesApi, clientsApi } from '../../api';
import type { Policy, Client } from '../../types';

const PoliciesForm: React.FC = () => {
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingPolicy, setEditingPolicy] = useState<Policy | null>(null);
  const [formData, setFormData] = useState<Partial<Policy>>({
    client_id: undefined,
    policy_type: 'Motor',
    region: '',
    currency: 'PKR',
    status: 'draft',
    sum_insured: 0,
    cnic_ntn: '',
    claim_limit: 0,
    industry: '',
    notes: '',
  });

  useEffect(() => {
    loadPolicies();
    loadClients();
  }, []);

  const loadPolicies = async () => {
    try {
      setLoading(true);
      const response = await policiesApi.list();
      setPolicies(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load policies');
    } finally {
      setLoading(false);
    }
  };

  const loadClients = async () => {
    try {
      const response = await clientsApi.list();
      setClients(response.data);
    } catch (err) {
      console.error('Failed to load clients:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validation
    if (!formData.client_id) {
      setError('Please select a client');
      return;
    }

    try {
      setLoading(true);
      if (editingPolicy) {
        await policiesApi.update(editingPolicy.id, formData);
        setSuccess('Policy updated successfully');
      } else {
        await policiesApi.create(formData);
        setSuccess('Policy created successfully');
      }
      setShowModal(false);
      resetForm();
      loadPolicies();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save policy');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (policy: Policy) => {
    setEditingPolicy(policy);
    setFormData(policy);
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this policy?')) return;

    try {
      setLoading(true);
      await policiesApi.delete(id);
      setSuccess('Policy deleted successfully');
      loadPolicies();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete policy');
    } finally {
      setLoading(false);
    }
  };

  const handleRecalculate = async (id: number) => {
    try {
      setLoading(true);
      await policiesApi.recalculate(id);
      setSuccess('Policy premiums recalculated successfully');
      loadPolicies();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to recalculate policy');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      client_id: undefined,
      policy_type: 'Motor',
      region: '',
      currency: 'PKR',
      status: 'draft',
      sum_insured: 0,
      cnic_ntn: '',
      claim_limit: 0,
      industry: '',
      notes: '',
    });
    setEditingPolicy(null);
  };

  const filteredPolicies = policies.filter(policy =>
    policy.policy_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    policy.policy_type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    policy.status?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="form-container">
      <div className="form-header">
        <h2>Policies Management</h2>
        <button
          className="btn btn-primary"
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
        >
          Add New Policy
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
          <button onClick={() => setSuccess(null)}>×</button>
        </div>
      )}

      <div className="search-box">
        <input
          type="text"
          placeholder="Search policies by number, type, or status..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading && policies.length === 0 ? (
        <div className="loading">Loading policies...</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Policy Number</th>
                <th>Client ID</th>
                <th>Type</th>
                <th>Status</th>
                <th>Currency</th>
                <th>Sum Insured</th>
                <th>Net Premium</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPolicies.length === 0 ? (
                <tr>
                  <td colSpan={8} style={{ textAlign: 'center' }}>
                    No policies found
                  </td>
                </tr>
              ) : (
                filteredPolicies.map((policy) => (
                  <tr key={policy.id}>
                    <td><strong>{policy.policy_number}</strong></td>
                    <td>{policy.client_id}</td>
                    <td>{policy.policy_type}</td>
                    <td>
                      <span className={`badge badge-${policy.status}`}>
                        {policy.status}
                      </span>
                    </td>
                    <td>{policy.currency}</td>
                    <td>{policy.sum_insured?.toLocaleString()}</td>
                    <td>{policy.net_premium?.toLocaleString()}</td>
                    <td>
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={() => handleEdit(policy)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-sm btn-primary"
                        onClick={() => handleRecalculate(policy.id)}
                        style={{ marginLeft: '5px' }}
                      >
                        Recalc
                      </button>
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => handleDelete(policy.id)}
                        style={{ marginLeft: '5px' }}
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
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingPolicy ? 'Edit Policy' : 'Add New Policy'}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Client <span className="required">*</span></label>
                  <select
                    value={formData.client_id || ''}
                    onChange={(e) => setFormData({ ...formData, client_id: Number(e.target.value) })}
                    required
                  >
                    <option value="">Select Client</option>
                    {clients.map(client => (
                      <option key={client.id} value={client.id}>
                        {client.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Policy Type</label>
                  <input
                    type="text"
                    value={formData.policy_type || ''}
                    onChange={(e) => setFormData({ ...formData, policy_type: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Region</label>
                  <input
                    type="text"
                    value={formData.region || ''}
                    onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Currency</label>
                  <select
                    value={formData.currency || 'PKR'}
                    onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                  >
                    <option value="PKR">PKR</option>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Status</label>
                  <select
                    value={formData.status || 'draft'}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="draft">Draft</option>
                    <option value="active">Active</option>
                    <option value="expired">Expired</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Sum Insured</label>
                  <input
                    type="number"
                    value={formData.sum_insured || ''}
                    onChange={(e) => setFormData({ ...formData, sum_insured: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label>CNIC/NTN</label>
                  <input
                    type="text"
                    value={formData.cnic_ntn || ''}
                    onChange={(e) => setFormData({ ...formData, cnic_ntn: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label>Claim Limit</label>
                  <input
                    type="number"
                    value={formData.claim_limit || ''}
                    onChange={(e) => setFormData({ ...formData, claim_limit: Number(e.target.value) })}
                  />
                </div>

                <div className="form-group">
                  <label>Industry</label>
                  <input
                    type="text"
                    value={formData.industry || ''}
                    onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  />
                </div>

                <div className="form-group full-width">
                  <label>Notes</label>
                  <textarea
                    value={formData.notes || ''}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows={3}
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Saving...' : editingPolicy ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PoliciesForm;
