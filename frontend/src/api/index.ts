import axios from 'axios';
import type {
  Client, Policy, Bank, ProductSetup, ItemDetail, PerilCalculation,
  Vehicle, Discount, PolicyDiscount, Deductible, Clause, Warranty, Agency,
  ComputationalSheet
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Clients API
export const clientsApi = {
  list: () => api.get<Client[]>('/api/clients/'),
  get: (id: number) => api.get<Client>(`/api/clients/${id}`),
  create: (data: Partial<Client>) => api.post<Client>('/api/clients/', data),
  update: (id: number, data: Partial<Client>) => api.put<Client>(`/api/clients/${id}`, data),
  delete: (id: number) => api.delete(`/api/clients/${id}`),
};

// Policies API
export const policiesApi = {
  list: () => api.get<Policy[]>('/api/policies/'),
  get: (id: number) => api.get<Policy>(`/api/policies/${id}`),
  create: (data: Partial<Policy>) => api.post<Policy>('/api/policies/', data),
  update: (id: number, data: Partial<Policy>) => api.put<Policy>(`/api/policies/${id}`, data),
  delete: (id: number) => api.delete(`/api/policies/${id}`),
  recalculate: (id: number) => api.post(`/api/policies/${id}/recalculate`),
};

// Banks API
export const banksApi = {
  list: (policyId: number) => api.get<Bank[]>(`/api/policies/${policyId}/banks/`),
  get: (policyId: number, id: number) => api.get<Bank>(`/api/policies/${policyId}/banks/${id}`),
  create: (policyId: number, data: Partial<Bank>) => api.post<Bank>(`/api/policies/${policyId}/banks/`, data),
  update: (policyId: number, id: number, data: Partial<Bank>) => api.put<Bank>(`/api/policies/${policyId}/banks/${id}`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/banks/${id}`),
};

// Product Setup API
export const productSetupApi = {
  get: (policyId: number) => api.get<ProductSetup>(`/api/policies/${policyId}/product-setup/`),
  create: (policyId: number, data: Partial<ProductSetup>) => api.post<ProductSetup>(`/api/policies/${policyId}/product-setup/`, data),
  update: (policyId: number, data: Partial<ProductSetup>) => api.put<ProductSetup>(`/api/policies/${policyId}/product-setup/`, data),
};

// Items API
export const itemsApi = {
  list: (policyId: number) => api.get<ItemDetail[]>(`/api/policies/${policyId}/items/`),
  get: (policyId: number, id: number) => api.get<ItemDetail>(`/api/policies/${policyId}/items/${id}`),
  create: (policyId: number, data: Partial<ItemDetail>) => api.post<ItemDetail>(`/api/policies/${policyId}/items/`, data),
  update: (policyId: number, id: number, data: Partial<ItemDetail>) => api.put<ItemDetail>(`/api/policies/${policyId}/items/${id}`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/items/${id}`),
};

// Perils API
export const perilsApi = {
  list: (policyId: number, itemId: number) => api.get<PerilCalculation[]>(`/api/policies/${policyId}/items/${itemId}/perils/`),
  create: (policyId: number, itemId: number, data: Partial<PerilCalculation>) => api.post<PerilCalculation>(`/api/policies/${policyId}/items/${itemId}/perils/`, data),
  update: (policyId: number, itemId: number, id: number, data: Partial<PerilCalculation>) => api.put<PerilCalculation>(`/api/policies/${policyId}/items/${itemId}/perils/${id}`, data),
  delete: (policyId: number, itemId: number, id: number) => api.delete(`/api/policies/${policyId}/items/${itemId}/perils/${id}`),
};

// Vehicles API
export const vehiclesApi = {
  list: (policyId: number) => api.get<Vehicle[]>(`/api/policies/${policyId}/vehicles/`),
  get: (policyId: number, id: number) => api.get<Vehicle>(`/api/policies/${policyId}/vehicles/${id}`),
  create: (policyId: number, data: Partial<Vehicle>) => api.post<Vehicle>(`/api/policies/${policyId}/vehicles/`, data),
  update: (policyId: number, id: number, data: Partial<Vehicle>) => api.put<Vehicle>(`/api/policies/${policyId}/vehicles/${id}`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/vehicles/${id}`),
};

// Discounts API (item-level)
export const discountsApi = {
  list: (policyId: number, itemId: number) => api.get<Discount[]>(`/api/policies/${policyId}/items/${itemId}/discounts/`),
  create: (policyId: number, itemId: number, data: Partial<Discount>) => api.post<Discount>(`/api/policies/${policyId}/items/${itemId}/discounts/`, data),
  delete: (policyId: number, itemId: number, id: number) => api.delete(`/api/policies/${policyId}/items/${itemId}/discounts/${id}`),
};

// Policy Discounts API
export const policyDiscountsApi = {
  list: (policyId: number) => api.get<PolicyDiscount[]>(`/api/policies/${policyId}/policy-discounts/`),
  create: (policyId: number, data: Partial<PolicyDiscount>) => api.post<PolicyDiscount>(`/api/policies/${policyId}/policy-discounts/`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/policy-discounts/${id}`),
};

// Deductibles API
export const deductiblesApi = {
  list: (policyId: number) => api.get<Deductible[]>(`/api/policies/${policyId}/deductibles/`),
  create: (policyId: number, data: Partial<Deductible>) => api.post<Deductible>(`/api/policies/${policyId}/deductibles/`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/deductibles/${id}`),
};

// Clauses API
export const clausesApi = {
  list: (policyId: number) => api.get<Clause[]>(`/api/policies/${policyId}/clauses/`),
  create: (policyId: number, data: Partial<Clause>) => api.post<Clause>(`/api/policies/${policyId}/clauses/`, data),
  update: (policyId: number, id: number, data: Partial<Clause>) => api.put<Clause>(`/api/policies/${policyId}/clauses/${id}`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/clauses/${id}`),
};

// Warranties API
export const warrantiesApi = {
  list: (policyId: number) => api.get<Warranty[]>(`/api/policies/${policyId}/warranties/`),
  create: (policyId: number, data: Partial<Warranty>) => api.post<Warranty>(`/api/policies/${policyId}/warranties/`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/warranties/${id}`),
};

// Agencies API
export const agenciesApi = {
  list: (policyId: number) => api.get<Agency[]>(`/api/policies/${policyId}/agencies/`),
  create: (policyId: number, data: Partial<Agency>) => api.post<Agency>(`/api/policies/${policyId}/agencies/`, data),
  delete: (policyId: number, id: number) => api.delete(`/api/policies/${policyId}/agencies/${id}`),
};

// Computational Sheet API
export const computationalSheetApi = {
  get: (policyId: number) => api.get<ComputationalSheet>(`/api/policies/${policyId}/computational-sheet/`),
};

// Final Policy API
export const finalPolicyApi = {
  get: (policyId: number) => api.get(`/api/policies/${policyId}/final-policy/`),
  downloadPDF: (policyId: number) => `${API_BASE_URL}/api/policies/${policyId}/final-policy/pdf`,
  downloadCoverLetter: (policyId: number) => `${API_BASE_URL}/api/policies/${policyId}/final-policy/cover-letter/pdf`,
};

// Reminders API
export const remindersApi = {
  list: () => api.get('/api/reminders/'),
  trigger: () => api.post('/api/reminders/trigger'),
};

// Gmail API
export const gmailApi = {
  getAuthUrl: () => api.get('/api/gmail/auth-url'),
  poll: () => api.post('/api/gmail/poll'),
  getDrafts: () => api.get('/api/gmail/drafts'),
};

export default api;
