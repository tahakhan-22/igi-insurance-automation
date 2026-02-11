import React, { useState, useEffect } from 'react';
import './styles/globals.css';
import Sidebar from './components/Sidebar';
import MainHeader from './components/MainHeader';
import ClientsForm from './components/forms/ClientsForm';
import PoliciesForm from './components/forms/PoliciesForm';
import { policiesApi } from './api';
import type { Policy } from './types';

function App() {
  const [activeModule, setActiveModule] = useState('clients');
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPolicies();
  }, []);

  const loadPolicies = async () => {
    try {
      setLoading(true);
      const response = await policiesApi.list();
      setPolicies(response.data);
      if (response.data.length > 0 && !selectedPolicy) {
        setSelectedPolicy(response.data[0]);
      }
    } catch (error) {
      console.error('Error loading policies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePolicy = async () => {
    // Switch to policies module to create policy
    setActiveModule('policies');
  };

  const renderModuleContent = () => {
    switch (activeModule) {
      case 'clients':
        return <ClientsForm />;
      
      case 'policies':
        return <PoliciesForm />;
      
      case 'banks':
      case 'documents':
      case 'product-setup':
      case 'items':
      case 'perils':
      case 'vehicles':
      case 'discounts':
      case 'deductibles':
      case 'clauses':
      case 'warranties':
      case 'agencies':
        return (
          <div className="form-section">
            <h3>{activeModule.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} Module</h3>
            {!selectedPolicy ? (
              <div className="alert alert-info">
                <strong>No Policy Selected</strong>
                <p>Please select or create a policy from the header to manage {activeModule}.</p>
                <button 
                  className="btn btn-primary"
                  onClick={() => setActiveModule('policies')}
                  style={{ marginTop: '10px' }}
                >
                  Go to Policies
                </button>
              </div>
            ) : (
              <div className="policy-context-form">
                <div className="policy-info-card">
                  <h4>Managing {activeModule.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} for:</h4>
                  <div className="policy-details">
                    <div className="detail-row">
                      <span className="label">Policy Number:</span>
                      <span className="value"><strong>{selectedPolicy.policy_number}</strong></span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Status:</span>
                      <span className={`badge badge-${selectedPolicy.status}`}>
                        {selectedPolicy.status}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Client ID:</span>
                      <span className="value">{selectedPolicy.client_id}</span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Sum Insured:</span>
                      <span className="value">{selectedPolicy.currency} {selectedPolicy.sum_insured?.toLocaleString()}</span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Net Premium:</span>
                      <span className="value">{selectedPolicy.currency} {selectedPolicy.net_premium?.toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                <div className="module-placeholder">
                  <div className="placeholder-icon">📋</div>
                  <h3>{activeModule.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} Management</h3>
                  <p>Full CRUD interface for this module is being implemented.</p>
                  <p className="status-text">
                    ✅ Backend API ready<br/>
                    ⏳ Frontend form in development
                  </p>
                  <div className="api-info">
                    <strong>Available API Endpoints:</strong>
                    <ul>
                      <li>GET /api/policies/{selectedPolicy.id}/{activeModule}/</li>
                      <li>POST /api/policies/{selectedPolicy.id}/{activeModule}/</li>
                      <li>PUT /api/policies/{selectedPolicy.id}/{activeModule}/{{'{id}'}}</li>
                      <li>DELETE /api/policies/{selectedPolicy.id}/{activeModule}/{{'{id}'}}</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      
      case 'computational-sheet':
        return (
          <div className="form-section">
            <h3>Computational Sheet</h3>
            {!selectedPolicy ? (
              <div className="alert alert-info">
                <strong>No Policy Selected</strong>
                <p>Please select a policy to view its computational sheet.</p>
              </div>
            ) : (
              <div className="policy-context-form">
                <div className="policy-info-card">
                  <h4>Computational Sheet for Policy: {selectedPolicy.policy_number}</h4>
                </div>
                <div className="module-placeholder">
                  <div className="placeholder-icon">📊</div>
                  <h3>Read-Only Computational Sheet</h3>
                  <p>This view shows aggregated premium calculations, charges, discounts, and perils.</p>
                  <p className="status-text">
                    ✅ Backend calculation engine ready<br/>
                    ⏳ Frontend view in development
                  </p>
                </div>
              </div>
            )}
          </div>
        );
      
      case 'final-policy':
        return (
          <div className="form-section">
            <h3>Final Policy Document</h3>
            {!selectedPolicy ? (
              <div className="alert alert-info">
                <strong>No Policy Selected</strong>
                <p>Please select a policy to view or download its final document.</p>
              </div>
            ) : (
              <div className="policy-context-form">
                <div className="policy-info-card">
                  <h4>Final Policy Document for: {selectedPolicy.policy_number}</h4>
                </div>
                <div className="module-placeholder">
                  <div className="placeholder-icon">📄</div>
                  <h3>Policy Document Generation</h3>
                  <p>View complete policy details and download as PDF.</p>
                  <p className="status-text">
                    ✅ PDF generation engine ready<br/>
                    ✅ Templates configured<br/>
                    ⏳ Frontend download UI in development
                  </p>
                  <div className="api-info">
                    <strong>Available Downloads:</strong>
                    <ul>
                      <li>Policy Document PDF</li>
                      <li>Cover Letter PDF</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      
      default:
        return (
          <div className="form-section">
            <h3>Module Not Found</h3>
            <p>The selected module is not available.</p>
          </div>
        );
    }
  };

  return (
    <div className="app">
      <Sidebar 
        activeModule={activeModule}
        onModuleChange={setActiveModule}
        selectedPolicy={selectedPolicy}
      />
      <div className="main-content">
        <MainHeader
          selectedPolicy={selectedPolicy}
          policies={policies}
          onPolicyChange={setSelectedPolicy}
          onCreatePolicy={handleCreatePolicy}
        />
        <div className="content-area">
          {loading && (activeModule !== 'clients' && activeModule !== 'policies') ? (
            <div className="loading">Loading...</div>
          ) : (
            renderModuleContent()
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
