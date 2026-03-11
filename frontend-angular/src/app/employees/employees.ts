import { Component, OnInit,ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Employee } from '../services/employee';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-employees',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees.html',
  styleUrls: ['./employees.css'],
})
export class Employees implements OnInit {
  employees: any[] = [];

  employeeForm!: FormGroup;
  showEmployeeModal = false;

  attendanceForm!: FormGroup;
  showAttendanceModal = false;
  selectedEmployee: any = null;
  today: string = new Date().toISOString().split('T')[0];
  showViewAttendanceModal: boolean = false;
  attendanceRecords: any[] = [];

  constructor(
    private empService: Employee,
    private fb: FormBuilder,
    private toastr: ToastrService,
    private cd:ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.initEmployeeForm();
    this.initAttendanceForm();
    this.loadEmployees();
  }

  initEmployeeForm() {
    this.employeeForm = this.fb.group({
      employee_id: ['', Validators.required],
      full_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      department: ['', Validators.required],
    });
  }

  initAttendanceForm() {
    this.attendanceForm = this.fb.group({
      date: [this.today, Validators.required],
      status: ['', Validators.required],
    });
  }

  loadEmployees() {
    this.empService.getEmployeeList().subscribe(
      (res: any) => {
        if (res.status) {
          this.employees = res.data;
        } else {
          this.toastr.error(res.message);
        }
        this.cd.detectChanges();
      },
      () => {
        this.toastr.error('Failed to load employees');
      },
    );
  }

  openEmployeeModal() {
    this.showEmployeeModal = true;
  }

  closeEmployeeModal() {
    this.employeeForm.reset();
    this.showEmployeeModal = false;
  }

  addEmployee() {
    if (this.employeeForm.invalid) {
      this.toastr.error('Please fill all required fields!');
      return;
    }

    this.empService.addEmployee(this.employeeForm.value).subscribe({
      next: (res: any) => {
        if (res.status) {
          this.toastr.success(res.message, 'Success');
          this.loadEmployees();
          this.employeeForm.reset();
          this.showEmployeeModal = false;
        } else {
          this.toastr.error(res.message, 'Error');
        }
      },
      error: () => {
        this.toastr.error('Server error. Please try again.', 'Error');
      },
    });
  }

  deleteEmployee(id: number) {
    this.empService.deleteEmployee(id).subscribe({
      next: (res: any) => {
        if (res.status) {
          this.toastr.success(res.message, 'Success');
        } else {
          this.toastr.error(res.message, 'Error');
        }
        this.loadEmployees();
      },
      error: () => {
        this.toastr.error('Server error. Please try again.', 'Error');
      },
    });
  }

  openAttendanceModal(emp: any) {
    this.selectedEmployee = emp;
    this.attendanceForm.patchValue({ date: this.today, status: '' }); // reset status
    this.showAttendanceModal = true;
  }

  closeAttendanceModal() {
    this.showAttendanceModal = false;
  }

  saveAttendance() {
    if (this.attendanceForm.invalid || !this.selectedEmployee) {
      this.toastr.error('Please select date and status');
      return;
    }

    const payload = {
      employee_id: this.selectedEmployee.id,
      date: this.attendanceForm.value.date,
      status: this.attendanceForm.value.status,
    };

    this.empService.markAttendance(payload).subscribe({
      next: (res: any) => {
        if (res.status) {
          this.toastr.success(res.message, 'Success');
          this.attendanceForm.reset({ date: this.today, status: '' });
          this.showAttendanceModal = false;
        } else {
          this.toastr.error(res.message, 'Error');
        }
      },
      error: () => {
        this.toastr.error('Server error. Please try again.', 'Error');
      },
    });
  }

  openViewAttendanceModal(emp: any) {
    this.selectedEmployee = emp;
    this.attendanceRecords = [];
    this.showViewAttendanceModal = true;

    this.empService.getEmployeeAttendance(emp.id).subscribe({
      next: (res: any) => {
        if (res.status) {
          this.attendanceRecords = res.data;
        } else {
          this.toastr.error(res.message, 'Error');
        }
        this.cd.detectChanges();
      },
      error: () => {
        this.toastr.error('Failed to load attendance', 'Error');
      },
    });
  }

  closeViewAttendanceModal() {
    this.showViewAttendanceModal = false;
  }
}
