import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { delay, Observable, of } from 'rxjs';
import { Report } from '../models/report.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  sendRecording(audioBlob: Blob): Observable<any> {

    const formData = new FormData();
    formData.append('file', audioBlob, 'meeting.webm');
  
    return this.http.post(
      `${this.baseUrl}/createReport`,
      formData
    );
  }

  getReports(): Observable<Report[]> {
    return this.http.get<Report[]>(
      `${this.baseUrl}/getReports`
    );
  }

  deleteReport(id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/deleteReport/${id}`
    );
  }
  updateReportTitle(
    id: number,
    title: string
  ): Observable<any> {
  
    return this.http.patch(
      `${this.baseUrl}/editReport/${id}`,
      { title }
    );
  }
  
}