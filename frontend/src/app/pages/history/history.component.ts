import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Report } from '../../models/report.model';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  reports: Report[] = [];

  selectedReport?: Report;

  constructor(
    private reportService: ApiService
  ) {}

  ngOnInit(): void {
    this.loadReports();
  }

  loadReports(): void {

    this.reportService.getReports()
      .subscribe({
        next: (reports) => {
          this.reports = reports;
        }
      });
  }

  viewReport(report: Report): void {
    this.selectedReport = report;
  }

  closeModal(): void {
    this.selectedReport = undefined;
  }

  downloadReport(report: Report): void {

    const blob = new Blob(
      [report.content],
      { type: 'text/markdown' }
    );

    const url =
      URL.createObjectURL(blob);

    const a =
      document.createElement('a');

    a.href = url;

    a.download = report.filename;

    a.click();

    URL.revokeObjectURL(url);
  }

  deleteReport(id: number): void {

    if (!confirm('Supprimer ce compte-rendu ?')) {
      return;
    }

    this.reportService
      .deleteReport(id)
      .subscribe({
        next: () => {
          this.loadReports();
        }
      });
  }
}