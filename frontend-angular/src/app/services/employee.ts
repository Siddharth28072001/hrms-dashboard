import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Employee {
  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getEmployeeList() {
    return this.http.get(`${this.apiUrl}/employees/getEmployeeList`);
  }

  addEmployee(data: any) {    
    return this.http.post(`${this.apiUrl}/employees/addEmployee`, data);
  }

  deleteEmployee(id: number) {
    return this.http.delete(`${this.apiUrl}/employees/deleteEmployee/${id}`);
  }

  markAttendance(payload: any) {
    return this.http.post(`${this.apiUrl}/attendance/markAttendance`, payload);
  }

  getEmployeeAttendance(employeeId: number) {
    return this.http.get(`${this.apiUrl}/attendance/getEmployeeAttendance/${employeeId}`);
  }
}