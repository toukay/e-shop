import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Product } from '../../../../core/models/product';

@Component({
  selector: 'app-product-listing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <section class="listing">
      <!-- Wrap the image in a container to control the overflow and centering -->
      <div class="listing-photo-container">
        <img class="listing-photo" [src]="product.imageUrl" alt="photo of {{product.name}}">
      </div>
      <h3 class="listing-heading">{{ product.name }}</h3>
      <p class="listing-price">\${{ product.price }}</p>
      <!-- <a [routerLink]="['/details', product.id]">Learn more</a> -->
    </section>

  `,
  styleUrl: './product-listing.component.css'
})
export class ProductListingComponent {
  @Input() product!:Product;
}
