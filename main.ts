/**
 * Created by Samuel Gratzl on 25.10.2016.
 */

/// <reference path="./tsd.d.ts" />

import {api2absURL, getAPIData} from '../caleydo_core/ajax';
import {EventHandler} from '../caleydo_core/event';

class ProcessingManager extends EventHandler {
  private source: any;

  constructor() {
    super();
    this.connect();
  }

  private connect() {
    this.source = new EventSource(api2absURL('/processing/stream'));
    this.source.onmessage = this.onEvent.bind(this);
  }

  private onEvent(event: any) {
    const data = JSON.parse(event.data);
    console.log(data);
  }
}

var p : ProcessingManager = null;

export function create() {
  if (p === null){
    p = new ProcessingManager();
  }
  return p;
}


{
  let manager = create();
  (<HTMLFormElement>document.querySelector('form')).addEventListener('submit', function(event) {
    const a = +(<HTMLInputElement>document.getElementById('ida')).value;
    const b = +(<HTMLInputElement>document.getElementById('idb')).value;
    getAPIData(`/processing/add/${a}/${b}`, {}, 'text').then((r) => {
      console.log(r);
    });
    event.stopPropagation();
    event.preventDefault();
    return false;
  })
}
