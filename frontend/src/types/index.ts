// TypeScript types matching backend schemas

export type AddressType = 'Home' | 'Office' | 'Other';
export type PolicyStatus = 'draft' | 'active' | 'expired' | 'cancelled';
export type RegistrationStatus = 'registered' | 'unregistered';
export type CalculationBasis = 'percentage' | 'flat' | 'per_mille';

export interface Client {
  id: number;
  name: string;
  address_type: AddressType;
  address: string;
  country: string;
  city: string;
  phone1?: string;
  phone2?: string;
  fax?: string;
  email?: string;
  created_at: string;
  updated_at?: string;
}

export interface Policy {
  id: number;
  policy_number: string;
  client_id: number;
  policy_type?: string;
  region?: string;
  currency: string;
  start_date?: string;
  end_date?: string;
  status: PolicyStatus;
  sum_insured: number;
  gross_premium: number;
  net_premium: number;
  premium_payable: number;
  cnic_ntn?: string;
  claim_limit?: number;
  industry?: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Bank {
  id: number;
  policy_id: number;
  serial_no?: number;
  bank_type?: string;
  limits?: number;
  created_at: string;
}

export interface ProductSetup {
  id: number;
  policy_id: number;
  legal_liability: boolean;
  accident_passengers: boolean;
  insured_estimated_value: boolean;
  rsd_md_terrorism: boolean;
  basic_premium_flag: boolean;
  pa_to_insured: boolean;
  admin_sub_charges: boolean;
  sales_tax_fed: boolean;
  federal_insurance_fee: boolean;
  stamp_duty: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ItemDetail {
  id: number;
  policy_id: number;
  schedule_id?: string;
  item_no?: number;
  sum_insured: number;
  basic_premium: number;
  gross_premium: number;
  risk_peril_reference?: string;
  created_at: string;
  updated_at?: string;
}

export interface PerilCalculation {
  id: number;
  item_id: number;
  peril_type: string;
  base_value: number;
  rate_percent: number;
  percent_of_rate: number;
  calculation_basis: CalculationBasis;
  flat_amount: number;
  basic_premium: number;
  created_at: string;
}

export interface Vehicle {
  id: number;
  policy_id: number;
  item_id?: number;
  registration_status: RegistrationStatus;
  registration_no?: string;
  engine_no?: string;
  chassis_no?: string;
  make?: string;
  model?: string;
  passengers?: number;
  body_type?: string;
  engine_cc?: number;
  year_of_manufacturing?: number;
  vehicle_age?: number;
  color?: string;
  accessories_sum_insured: number;
  cnic?: string;
  license_no?: string;
  loan_po_no?: string;
  contact_details?: string;
  created_at: string;
  updated_at?: string;
}

export interface Discount {
  id: number;
  item_id: number;
  discount_type: string;
  rate_percent: number;
  amount: number;
  created_at: string;
}

export interface PolicyDiscount {
  id: number;
  policy_id: number;
  unique_identifier?: string;
  discount_type: string;
  rate_percent: number;
  amount: number;
  created_at: string;
}

export interface Deductible {
  id: number;
  policy_id: number;
  deductible_type: string;
  amount: number;
  conditions?: string;
  created_at: string;
}

export interface Clause {
  id: number;
  policy_id: number;
  clause_name: string;
  description?: string;
  clause_limit?: number;
  remarks?: string;
  is_checked: boolean;
  created_at: string;
}

export interface Warranty {
  id: number;
  policy_id: number;
  warranty_type: string;
  details?: string;
  is_active: boolean;
  created_at: string;
}

export interface Agency {
  id: number;
  policy_id: number;
  agent_name: string;
  apportionment_percent: number;
  amount: number;
  premium_share_percent: number;
  created_at: string;
}

export interface ComputationalSheet {
  charges: Array<{name: string; amount: number}>;
  clauses: Array<{name: string; limit?: number; description?: string}>;
  warranties: Array<{type: string; details?: string}>;
  item_discounts: Array<{item_no?: number; discount_type: string; amount: number}>;
  policy_discounts: Array<{type: string; amount: number}>;
  perils: Array<{item_no?: number; peril_type: string; premium: number}>;
  total_basic_premium: number;
  total_charges: number;
  gross_premium: number;
  total_discounts: number;
  net_premium: number;
  sum_insured: number;
}
