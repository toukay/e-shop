import { inject, Injectable } from '@angular/core';
import { Product } from '../models/product';
import { Brand } from '../models/brand';
import { ProductType } from '../models/product-type';
import { Category } from '../models/category';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  url = "http://localhost:5000/api";

  constructor() { }

  async getAllProducts() : Promise<Product[]> {
    const data = await fetch(`${this.url}/products`);
    const jsonData = await data.json() ?? {};
    return jsonData.map((product: any) => this.transformProduct(product)) ?? [];
  }

  async getProductById(id: Number) : Promise<Product | undefined> {
    const data = await fetch(`${this.url}/products/${id}`);
    const jsonData = await data.json() ?? {};
    return this.transformProduct(jsonData) ?? {};
  }

  transformProduct(apiProduct: any): Product {
    return {
      ...apiProduct,
      imageUrl: apiProduct.image_url // Map image_url to imageUrl
    };
  }

  async getAllBrands() : Promise<Brand[]> {
    const data = await fetch(`${this.url}/brands`);
    return await data.json() ?? [];
  }

  async getBrandById(id: Number) : Promise<Brand | undefined> {
    const data = await fetch(`${this.url}/brands/${id}`);
    return await data.json() ?? {};
  }

  async getAllProductTypes() : Promise<ProductType[]> {
    const data = await fetch(`${this.url}/product-types`);
    return await data.json() ?? [];
  }

  async getProductTypeById(id: Number) : Promise<ProductType | undefined> {
    const data = await fetch(`${this.url}/product-types/${id}`);
    return await data.json() ?? {};
  }

  async getAllCategories() : Promise<Category[]> {
    const data = await fetch(`${this.url}/categories`);
    return await data.json() ?? [];
  }

  async getCategoryById(id: Number) : Promise<Category | undefined> {
    const data = await fetch(`${this.url}/categories/${id}`);
    return await data.json() ?? {};
  }

  // submitApplication(firstName: string, lastName: string, email: string) {
  //   console.log(firstName, lastName, email);
  // }
}
