## Example GET
curl http://localhost:8082/doc.txt

## Example POST
curl -X POST -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}' http://localhost:8082/test.txt

## Example PUT
curl -X PUT -H "Content-Type: text/plain" -d 'This is some text content' http://localhost:8082/test.txt

## Example DELETE
curl -X DELETE http://localhost:8082/test.txt