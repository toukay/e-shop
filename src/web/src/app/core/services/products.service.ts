import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  url = "http://localhost:5000/api/";

  constructor() { }

}
