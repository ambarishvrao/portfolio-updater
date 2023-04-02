import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { AppComponent } from './app.component';
import {HttpClientModule} from
	'@angular/common/http';
@NgModule({
declarations: [
	AppComponent,
	FileUploadComponent,
],
imports: [
	BrowserModule,
	AppRoutingModule,
	HttpClientModule
],
providers: [],
bootstrap: [AppComponent]
})
export class AppModule { }
