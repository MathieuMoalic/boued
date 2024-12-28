export interface Item {
    id: number;
    name: string;
    category: string;
    is_active?: boolean;
    notes?: string;
    quantity?: number;
    unit?: string;
}

export interface ItemForm {
    name: string;
    category: string;
    notes?: string;
    quantity?: number;
    unit?: string;
}

export interface ItemFilter {
    category?: string;
    is_active?: boolean;
}

export let possibleUnits = ["None", "kg", "g", "l", "ml", "pcs", "cans", "bottles"];

export let possibleCategories = ["Other", "Fruit", "Vegetable", "Bread", "Canned", "Frozen", "Beverage", "Snack", "Alcohol", "Cleaning"];
