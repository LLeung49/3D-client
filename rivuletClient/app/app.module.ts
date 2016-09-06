import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { AppComponent }   from './app.component';
import { MainPageComponent }   from './mainPage.component';
import {TaskFormComponent} from "./task-form.component";


@NgModule({
  imports:      [ BrowserModule,FormsModule ],
  declarations: [ AppComponent ,MainPageComponent,TaskFormComponent],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
