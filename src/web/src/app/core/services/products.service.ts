import { Injectable } from '@angular/core';
import { Product } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  url = "http://localhost:5000/api";

  constructor() { }

  async getAllProducts() : Promise<Product[]> {
    const data = await fetch(`${this.url}/products`);
    return await data.json() ?? [];
  }

  async getProductById(id: Number) : Promise<Product | undefined> {
    const data = await fetch(`${this.url}/products/${id}`);
    return await data.json() ?? {};
  }

  // submitApplication(firstName: string, lastName: string, email: string) {
  //   console.log(firstName, lastName, email);
  // }
}
