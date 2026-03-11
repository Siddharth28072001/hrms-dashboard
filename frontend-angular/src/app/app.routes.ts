import { Routes } from '@angular/router';
import { Employees } from './employees/employees';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    component: Employees
  }
];