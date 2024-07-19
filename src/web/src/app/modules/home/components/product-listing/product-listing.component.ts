import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Product } from '../../../../core/models/product';

@Component({
  selector: 'app-product-listing',
  standalone: true,
  imports: [RouterModule],
  template: `
    <section class="listing">
      <!-- <img class="listing-photo" [src]="product.photo" alt="photo of {{product.name}}"> -->
      <img class="listing-photo" src="assets/drone.jpg" alt="photo of {{product.name}}">
      <h2 class="listing-heading">{{ product.name }}</h2>
      <p class="listing-location">{{ product.price }}</p>
      <!-- <a [routerLink]="['/details', product.id]">Learn more</a> -->
    </section>
  `,
  styleUrl: './product-listing.component.css'
})
export class ProductListingComponent {
  @Input() product!:Product;
}
