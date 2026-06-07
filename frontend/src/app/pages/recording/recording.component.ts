import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecordingService } from '../../services/services/recording.service';

@Component({
  selector: 'app-recording',
  imports: [CommonModule],
  templateUrl: './recording.component.html',
  styleUrls: ['./recording.component.css']
})
export class RecordingComponent {

  @ViewChild('waveCanvas', { static: false })
  canvasRef!: ElementRef<HTMLCanvasElement>;
  constructor(
    private recordingService: RecordingService
  ) {}
  isRecording = false;
  isPaused = false;
  isDrawing = false; 
  private audioContext!: AudioContext;
  private analyser!: AnalyserNode;
  private dataArray!: Uint8Array;
  private mediaStream!: MediaStream;
  private source!: MediaStreamAudioSourceNode;
  private animationId!: number;
  

  async startRecording() {

    this.isRecording = true;
  
    this.mediaStream =
      await this.recordingService.startRecording();
  
    this.audioContext = new AudioContext();
  
    this.analyser =
      this.audioContext.createAnalyser();
  
    this.analyser.fftSize = 256;
  
    this.dataArray =
      new Uint8Array(
        this.analyser.frequencyBinCount
      );
  
    this.source =
      this.audioContext.createMediaStreamSource(
        this.mediaStream
      );
  
    this.source.connect(this.analyser);
  
    setTimeout(
      () => this.drawWaveform(),
      0
    );
  }

  private drawWaveform = () => {
    const canvas = this.canvasRef.nativeElement;
    const ctx = canvas.getContext('2d')!;
  
    canvas.width = canvas.offsetWidth || 300 ;
    canvas.height = 100;
  
    this.isDrawing = true;
  
    const render = () => {
      if (!this.isDrawing) return;
  
      this.animationId = requestAnimationFrame(render);
  
      this.analyser.getByteFrequencyData(this.dataArray);
  
      ctx.clearRect(0, 0, canvas.width, canvas.height);
  
      const barWidth = (canvas.width / this.dataArray.length) * 2;
      let x = 0;
  
      for (let i = 0; i < this.dataArray.length; i++) {
        const barHeight = this.dataArray[i];
  
        ctx.fillStyle = '#4f46e5';
  
        ctx.fillRect(
          x,
          canvas.height - barHeight / 2,
          barWidth,
          barHeight / 2
        );
  
        x += barWidth + 1;
      }
    };
  
    render();
  };

  pauseRecording() {

    this.isPaused = true;
  
    this.recordingService.pauseRecording();
  
    this.audioContext.suspend();
  
    this.isDrawing = false;
  
    cancelAnimationFrame(
      this.animationId
    );
  }

  resumeRecording() {

    this.isPaused = false;
  
    this.recordingService.resumeRecording();
  
    this.audioContext.resume();
  
    this.drawWaveform();
  }

  async stopRecording() {

    const audioBlob =
      await this.recordingService.stopRecording();
  
    console.log(audioBlob);
  
    this.isRecording = false;
    this.isPaused = false;
    this.isDrawing = false;
  
    cancelAnimationFrame(
      this.animationId
    );
  
    await this.audioContext.close();
  
    // API UPLOAD
    // Sauvegarde locale
    const url = URL.createObjectURL(audioBlob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `meeting-${Date.now()}.webm`;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
  }
}