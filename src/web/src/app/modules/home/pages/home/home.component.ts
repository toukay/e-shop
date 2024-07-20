import { Component, inject, OnInit } from '@angular/core';
import { ProductListingComponent } from '../../components/product-listing/product-listing.component';
import { Product } from '../../../../core/models/product';
import { ProductsService } from '../../../../core/services/products.service';
import { HomeModule } from '../../home.module';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { BadgeModule } from 'primeng/badge';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { FloatLabelModule } from 'primeng/floatlabel';
import { FormsModule } from '@angular/forms';
import { Brand } from '../../../../core/models/brand';
import { ProductType } from '../../../../core/models/product-type';
import { Category } from '../../../../core/models/category';
import { CheckboxModule } from 'primeng/checkbox';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    HomeModule,
    ProductListingComponent,
    MenubarModule,
    AvatarModule,
    BadgeModule,
    InputTextModule,
    RippleModule,
    InputTextModule,
    FloatLabelModule,
    FormsModule,
    CheckboxModule
  ],
  templateUrl:'home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  productList: Product[] = [];
  brandList: Brand[] = [];
  productTypeList: ProductType[] = [];
  categoryList: ProductType[] = [];
  productsService: ProductsService = inject(ProductsService);

  searchValue: string | undefined;

  selectedCategories: Category[] = [];
  categoryValue: Category | undefined;

  constructor() {
    this.productsService.getAllProducts().then((dataList: Product[]) => {
      this.productList = dataList;
    });
    this.productsService.getAllBrands().then((dataList: Brand[]) => {
        this.brandList = dataList;
    })
    this.productsService.getAllProductTypes().then((dataList: ProductType[]) => {
        this.productTypeList = dataList;
    })
    this.productsService.getAllCategories().then((dataList: Category[]) => {
        this.categoryList = dataList;
    })
  }
}
