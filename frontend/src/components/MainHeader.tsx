import React from 'react';
import type { Policy } from '../types';

interface MainHeaderProps {
  selectedPolicy: Policy | null;
  policies: Policy[];
  onPolicyChange: (policy: Policy) => void;
  onCreatePolicy: () => void;
}

const MainHeader: React.FC<MainHeaderProps> = ({
  selectedPolicy,
  policies,
  onPolicyChange,
  onCreatePolicy,
}) => {
  return (
    <div className="main-header">
      <div>
        <h1>Insurance Policy Management</h1>
      </div>
      <div className="header-actions">
        <select
          value={selectedPolicy?.id || ''}
          onChange={(e) => {
            const policy = policies.find(p => p.id === parseInt(e.target.value));
            if (policy) onPolicyChange(policy);
          }}
          style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
        >
          <option value="">Select Policy</option>
          {policies.map((policy) => (
            <option key={policy.id} value={policy.id}>
              {policy.policy_number} - {policy.status}
            </option>
          ))}
        </select>
        <button className="btn btn-primary" onClick={onCreatePolicy}>
          + New Policy
        </button>
      </div>
    </div>
  );
};

export default MainHeader;
