import { Component } from '@angular/core'; //pour @ngif
import { SidebarModule } from 'primeng/sidebar';
import { ButtonModule } from 'primeng/button';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  imports: [SidebarModule,ButtonModule, CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css',
  standalone: true
})
export class SidebarComponent {
  sidebarVisible = false;
  constructor(private router: Router) {}

  goToRecord(): void {
    this.router.navigate(['/record']);
  }

  goToHistory(): void {
    this.router.navigate(['/history']);
  }
}
