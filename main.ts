/**
 * Created by Samuel Gratzl on 25.10.2016.
 */

/// <reference path="./tsd.d.ts" />

import {api2absURL, getAPIData as getBaseAPIData} from '../caleydo_core/ajax';
import {EventHandler, IEvent} from '../caleydo_core/event';

interface ITaskMessage {
  task_id: string;
  task_name: string;
  task_status: string; //success, failure
}

class ProcessingManager extends EventHandler {
  private source: any;

  constructor() {
    super();
    this.connect();
  }

  private connect() {
    //use an event source to listen for results
    this.source = new EventSource(api2absURL('/processing/stream'));
    this.source.onmessage = this.onEvent.bind(this);
  }

  private onEvent(event: any) {
    const data = JSON.parse(event.data);
    this.fire('status,'+data.task_status, data);
  }
}

var p : ProcessingManager = null;

export function create() {
  if (p === null){
    p = new ProcessingManager();
  }
  return p;
}

/**
 * utility to wait for a processing result
 * @param expectedDataType
 * @return {(taskId:string)=>Promise<any>}
 */
function waitForResult(expectedDataType = 'json'): (taskId: string)=>Promise<any> {
  const manager = create();

  const cache = {};
  function waitingHandler(event: IEvent, data: ITaskMessage) {
    //maybe soo fast that the success message is earlier than the result
    cache[data.task_id] = data;
  }
  manager.on('status', waitingHandler);

  /**
   * wait for task result
   * @param taskId
   * @return {any}
   */
  function waitForTaskResult(taskId: string) {
    console.log(taskId);
    //no more waiting
    manager.off('status', waitingHandler);

    //check if we already have the result
    if (taskId in cache) {
      return Promise.resolve(cache[taskId]);
    }

    //use the task id and wait for the result by waiting for an result
    return new Promise((resolve) => {
      function waitForResult(event: IEvent, data: ITaskMessage) {
        if (data.task_id !== taskId) {
          return;
        }
        //hit
        //no more waiting
        manager.off('status', waitForResult);
        resolve(data);
      }
      manager.on('status', waitForResult);
    });
  }

  /**
   * use the given task result message and fetch the underlying data if it was a success
   * @param taskMessage
   * @return {Promise<any>}
   */
  function getTaskResult(taskMessage: ITaskMessage) {
    if (taskMessage.task_status === 'failure') {
      return Promise.reject(`task ${taskMessage.task_id} (${taskMessage.task_name}) failed`);
    }
    //get the real data
    return getBaseAPIData('/processing/res/'+taskMessage.task_id, {}, expectedDataType);
  }


  return (taskId: string) => waitForTaskResult(taskId).then(getTaskResult);
}

/**
 * api version of getJSON with processing waiter in between
 * @param url api relative url
 * @param data arguments
 * @returns {Promise<any>}
 */
export function getAPIJSON(url: string, data : any = {}): Promise<any> {
  return getAPIData(url, data, 'json');
}

/**
 * api version of getData with processing waiter in between
 * @param url api relative url
 * @param data arguments
 * @param expectedDataType expected data type to return, in case of JSON it will be parsed using JSON.parse
 * @returns {Promise<any>}
 */
export function getAPIData(url: string, data : any = {}, expectedDataType = 'json'): Promise<any> {
  const waiter = waitForResult(expectedDataType);
  return getBaseAPIData(url, data, 'text').then(waiter);
}
