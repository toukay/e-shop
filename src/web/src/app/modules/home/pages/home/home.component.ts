import { Component, inject } from '@angular/core';
import { ProductListingComponent } from '../../components/product-listing/product-listing.component';
import { CommonModule } from '@angular/common';
import { Product } from '../../../../core/models/product';
import { ProductsService } from '../../../../core/services/products.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, ProductListingComponent],
  template: `
    <section>
      <form action="">
        <input type="text" placeholder="Filter by city" #filter>
        <button class="primary" type="button">Search</button>
      </form>
    </section>
    <section class="results">
      <app-product-listing
        *ngFor="let product of productList"
        [product]="product">
      </app-product-listing>
    </section>
  `,
  styleUrl: './home.component.css'
})
export class HomeComponent {
  productList: Product[] = [];
  productsService: ProductsService = inject(ProductsService);

  constructor() {
    this.productsService.getAllProducts().then((productList: Product[]) => {
      this.productList = productList;
    });
  }
}
