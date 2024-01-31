## WEBSOCKET TASK

Creates a asynchronous WS connection and returns a ws object which can be further used to send and recieve messages

## AIOSERIAL TASK

Which is used to get data from the rs485 serial connection and send that data through the websocket


## Need to make a mechanism in which the websocket task and the aioserial taks should be separated and if one goes through an exception the other should not be stopped working cause the tasks will be run forever
