`/api/` and `/api/health` should return `{"status": "OK"}` - `GET, POST`

**/api/login** 2 required params: - точно такая же история как с отелями:)
`{
"username": username,
"password": password
}`


**/api/all_guests** method POST - take no params: получишь данные списком, аналог get_guests с отелей

**/api/individual** 1 required param: отправляешь req_id юзера получаешь доп инфу, фото и тд
`{
"req_id": request_id
}`

**/api/accept** 1 required param: для одобрения, просто пустой post с req_id
`{
"req_id": request_id
}`

**/api/decline** 2 required params: для отказа, post с req_id и комментом отказа
`{
"req_id": request_id,
"comment": comment
}`

**/api/generate** POST with no params
response should be .csv file


**/api/upload** POST with 1 param uploaded .csv file
`{
"file_bytes": bytes,
}`




