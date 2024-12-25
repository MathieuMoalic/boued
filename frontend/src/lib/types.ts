export interface Item {
    id?: number;
    name: string;
    category: string;
    is_active?: boolean;
    notes?: string;
    quantity?: number;
    unit?: string;
}

export interface ItemFilter {
    category?: string;
    is_active?: boolean;
}