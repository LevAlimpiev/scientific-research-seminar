go run .

В migrations:

psql -U postgres -f db.sql


curl -X POST http://localhost:8082/add_product \
-H "Content-Type: application/json" \
-d '{"name": "Меч Света Звёздный Воин", "description": "Игрушечный световой меч с 5 цветами и звуковыми эффектами", "sku": "LWSW123", "price": 1990}'


curl -X POST http://localhost:8082/add_product \
-H "Content-Type: application/json" \
-d '{"name": "Игровой набор Кухня шефа", "description": "Игрушечная кухня с посудой и наборами продуктов", "sku": "CHFKI002", "price": 2590}'


curl -X POST http://localhost:8082/add_product \
-H "Content-Type: application/json" \
-d '{"name": "Телепортатор 5000 Мультипространство", "description": "Вымышленный телепорт, который обязательно переместит тебя в дивный мир приключений", "sku": "TP5000", "price": 9990}'


curl "http://localhost:8082/search_products?query=Смартфон"

curl "http://localhost:8082/dump"
