import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Report } from '../../models/report.model';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  reports: Report[] = [];

  selectedReport?: Report;
  renderedMarkdown: SafeHtml = '';
  editingReportId?: number;
  editedTitle = '';
  constructor(
    private reportService: ApiService,
    private sanitizer: DomSanitizer
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
  startEditing(report: Report): void {
    this.editingReportId = report.id;
    this.editedTitle = report.title;
  }
  saveTitle(report: Report): void {

    this.reportService
      .updateReportTitle(
        report.id,
        this.editedTitle
      )
      .subscribe({
  
        next: () => {
  
          report.title = this.editedTitle;
  
          this.editingReportId = undefined;
        },
  
        error: (err) => {
          console.error(err);
        }
      });
  }
  cancelEditing(): void {
    this.editingReportId = undefined;
  }
  viewReport(report: Report): void {

    this.selectedReport = report;
  
    this.renderedMarkdown =
      this.sanitizer.bypassSecurityTrustHtml(
        marked.parse(report.content || '') as string
      );
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

    a.download = report.title;

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