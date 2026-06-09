import { Routes } from '@angular/router';

import { RecordingComponent } from './pages/recording/recording.component';
import { HistoryComponent } from './pages/history/history.component';

export const routes: Routes = [
  { path: '', component: RecordingComponent },
  { path: 'record', component: RecordingComponent },
  { path: 'history', component: HistoryComponent },
];