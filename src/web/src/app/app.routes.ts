import { Routes } from '@angular/router';
import { HomeComponent } from './modules/home/pages/home/home.component';
import { DetailsComponent } from './modules/home/pages/details/details.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
        title: 'eShop'
    },
    {
        path: 'details/:id',
        component: DetailsComponent,
        title: 'Details Page'
    }
];
