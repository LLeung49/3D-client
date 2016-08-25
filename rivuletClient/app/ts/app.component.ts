import {Component} from 'angular2/core';
import {Config} from './config.service';
import {MainPageComponent} from "./mainPage.component";

@Component({
    selector: 'my-app',
    templateUrl: 'app/ts/app.component.html',
    directives: [MainPageComponent]
})

export class AppComponent {
    mainHeading = Config.MAIN_HEADING;
    
}
