/**
 * Created by Samuel Gratzl on 25.10.2016.
 */
import { EventHandler } from 'phovea_core';
export declare class ProcessingManager extends EventHandler {
    private source;
    constructor();
    private connect;
    private onEvent;
    private static instance;
    static getInstance(): ProcessingManager;
    /**
     * utility to wait for a processing result
     * @param expectedDataType
     * @return {(taskId:string)=>Promise<any>}
     */
    waitForResult(expectedDataType?: string): (taskId: string) => Promise<any>;
    /**
     * api version of getJSON with processing waiter in between
     * @param url api relative url
     * @param data arguments
     * @returns {Promise<any>}
     */
    getAPIJSON(url: string, data?: any): Promise<any>;
    /**
     * api version of getData with processing waiter in between
     * @param url api relative url
     * @param data arguments
     * @param expectedDataType expected data type to return, in case of JSON it will be parsed using JSON.parse
     * @returns {Promise<any>}
     */
    getAPIData(url: string, data?: any, expectedDataType?: string): Promise<any>;
}
