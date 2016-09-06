import {Component, Input} from '@angular/core';


@Component({
    selector:'mainpage',
    templateUrl:'app/mainPage.component.html',

})


export class MainPageComponent{
    username = 'Lucien';
    age = '26';
    nationality = 'China';
    department = 'USYD';
    filePath = ""

    // myFunction()
    // {
    // document.getElementById("demo").innerHTML="我的第一个 JavaScript 函数";
    // }

    getTask(){
        this.filePath = (<HTMLInputElement>document.getElementById("importFile")).value;
        

        
        alert("username:" + this.username + "age:" + this.age + "filePath:" + this.filePath)
    }


}