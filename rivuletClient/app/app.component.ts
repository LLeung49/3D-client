import { Component } from '@angular/core';
import {MainPageComponent} from "./mainPage.component";
@Component({
  selector: 'my-app',
  templateUrl: 'app/app.component.html',
  // directives:[MainPageComponent]
})
export class AppComponent { 
  title = 'Tour of Heroes';
  name = 'Lucien';
    p1 = '1'
}
