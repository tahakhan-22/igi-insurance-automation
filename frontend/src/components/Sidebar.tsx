import React from 'react';
import type { Policy } from '../types';

interface SidebarProps {
  activeModule: string;
  onModuleChange: (module: string) => void;
  selectedPolicy: Policy | null;
}

const modules = [
  'clients',
  'policies',
  'banks',
  'documents',
  'product-setup',
  'items',
  'perils',
  'vehicles',
  'discounts',
  'deductibles',
  'clauses',
  'warranties',
  'agencies',
  'computational-sheet',
  'final-policy',
];

const Sidebar: React.FC<SidebarProps> = ({ activeModule, onModuleChange, selectedPolicy }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>IGI Insurance</h2>
        <p>Policy Management System</p>
        {selectedPolicy && (
          <div style={{ marginTop: '10px', fontSize: '11px' }}>
            Policy: {selectedPolicy.policy_number}
          </div>
        )}
      </div>
      <ul className="sidebar-menu">
        {modules.map((module) => (
          <li
            key={module}
            className={activeModule === module ? 'active' : ''}
            onClick={() => onModuleChange(module)}
          >
            {module.split('-').map(word => 
              word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ')}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
