/**
 * Created by Samuel Gratzl on 25.10.2016.
 */

import {getAPIJSON} from './main';

(<HTMLFormElement>document.querySelector('form')).addEventListener('submit', function(event) {
  const a = +(<HTMLInputElement>document.getElementById('ida')).value;
  const b = +(<HTMLInputElement>document.getElementById('idb')).value;

  //use getAPIJSON as usual
  getAPIJSON(`/processing/add/${a}/${b}`, {}).then((r) => {
    (<HTMLInputElement>document.getElementById('idr')).value = String(r);
  }).catch((error) => {
    console.log(error);
  });

  event.stopPropagation();
  event.preventDefault();
  return false;
});
