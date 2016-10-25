/**
 * Created by Samuel Gratzl on 25.10.2016.
 */

interface Callback { (data: any): void; }

declare class EventSource {
  onmessage: Callback;

  addEventListener(event: string, cb: Callback): void;

  constructor(name: string);
}
