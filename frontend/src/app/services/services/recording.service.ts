import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class RecordingService {

  private mediaRecorder?: MediaRecorder;
  private chunks: Blob[] = [];
  private stream?: MediaStream;

  async startRecording() {

    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: true
    });

    this.chunks = [];

    this.mediaRecorder = new MediaRecorder(this.stream);

    this.mediaRecorder.ondataavailable = (event) => {
      this.chunks.push(event.data);
    };

    this.mediaRecorder.start();

    return this.stream;
  }

  getStream(): MediaStream | undefined {
    return this.stream;
  }

  pauseRecording() {
    this.mediaRecorder?.pause();
  }

  resumeRecording() {
    this.mediaRecorder?.resume();
  }

  stopRecording(): Promise<Blob> {

    return new Promise((resolve) => {

      if (!this.mediaRecorder) {
        throw new Error('No recording');
      }

      this.mediaRecorder.onstop = () => {

        const blob = new Blob(
          this.chunks,
          { type: 'audio/webm' }
        );

        this.stream?.getTracks().forEach(track => track.stop());

        resolve(blob);
      };

      this.mediaRecorder.stop();
    });
  }
}