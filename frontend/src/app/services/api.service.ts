import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  sendRecording(audioBlob: Blob): Observable<any> {

    const formData = new FormData();

    formData.append(
      'file',
      audioBlob,
      'meeting.webm'
    );

    return this.http.post(
      `${this.baseUrl}/createReport`,
      formData
    );
  }
}