import { Component } from '@angular/core';
import { Task }    from './task';
@Component({
  selector: 'task-form',
  templateUrl: 'app/hero-form.component.html'
})
export class TaskFormComponent {
  powers = ['Really Smart', 'Super Flexible',
            'Super Hot', 'Weather Changer'];
  model = new Task(18, 'Dr IQ', this.powers[0]);
  submitted = false;
  onSubmit() { this.submitted = true; }
  // TODO: Remove this when we're done
  get diagnostic() { return JSON.stringify(this.model); }
}
