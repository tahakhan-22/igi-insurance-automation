import React, { useState, useEffect } from 'react';
import './styles/globals.css';
import Sidebar from './components/Sidebar';
import MainHeader from './components/MainHeader';
import ClientsForm from './components/forms/ClientsForm';
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
    try {
      // This would open a modal or form to create a new policy
      alert('Create policy functionality - to be implemented in forms');
    } catch (error) {
      console.error('Error creating policy:', error);
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
          {loading && activeModule !== 'clients' ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              {activeModule === 'clients' ? (
                <ClientsForm />
              ) : (
                <div className="form-section">
                  <h3>{activeModule.charAt(0).toUpperCase() + activeModule.slice(1)} Module</h3>
                  <p>
                    This is the {activeModule} module. Full CRUD forms would be implemented here.
                    For now, this demonstrates the layout and structure.
                  </p>
                  {selectedPolicy && (
                    <div style={{ marginTop: '20px' }}>
                      <h4>Selected Policy: {selectedPolicy.policy_number}</h4>
                      <p>Status: <span className={`status-badge ${selectedPolicy.status}`}>
                        {selectedPolicy.status}
                      </span></p>
                      <p>Client ID: {selectedPolicy.client_id}</p>
                      <p>Sum Insured: {selectedPolicy.currency} {selectedPolicy.sum_insured}</p>
                      <p>Net Premium: {selectedPolicy.currency} {selectedPolicy.net_premium}</p>
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
