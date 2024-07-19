import { Brand } from "./brand";
import { Category } from "./category";
import { ProductType } from "./product-type";

export interface Product {
    id: number,
    name: string,
    description: string,
    price: number,
    brand: Brand,
    productType: ProductType,
    categories: Category[],
}
