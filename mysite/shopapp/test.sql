SELECT "auth_user"."id",
		 "auth_user"."password",
		 "auth_user"."last_login",
		 "auth_user"."is_superuser",
		 "auth_user"."username",
		 "auth_user"."first_name",
		 "auth_user"."last_name",
		 "auth_user"."email",
		 "auth_user"."is_staff",
		 "auth_user"."is_active",
		 "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."username" = 'sergei' LIMIT 21; args=('sergei',
		);
SELECT "shopapp_order"."id",
		 "shopapp_order"."delivery_address",
		 "shopapp_order"."promocode",
		 "shopapp_order"."created_at",
		 "shopapp_order"."user_id",
		 "shopapp_order"."receipt"
FROM "shopapp_order"
WHERE ("shopapp_order"."delivery_address" = 'ul Pupkina, d 8'
		AND "shopapp_order"."promocode" = 'SALE123'
		AND "shopapp_order"."user_id" = 1) LIMIT 21; args=('ul Pupkina, d 8', 'SALE123', 1); alias=default INSERT INTO "shopapp_order" ("delivery_address", "promocode", "created_at", "user_id", "receipt") VALUES ('ul Pupkina, d 8', 'SALE123', '2023-07-02 14:21:12.085026', 1, '') RETURNING "shopapp_order"."id"; args=('ul Pupkina, d 8', 'SALE123', '2023-07-02 14:21:12.085026', 1, ''); alias=defaultSELECT "shopapp_product"."id",
		 "shopapp_product"."name",
		 "shopapp_product"."description",
		 "shopapp_product"."price",
		 "shopapp_product"."discount",
		 "shopapp_product"."created_at",
		 "shopapp_product"."archived",
		 "shopapp_product"."created_by_id",
		 "shopapp_product"."preview"
FROM "shopapp_product"
ORDER BY  "shopapp_product"."name" ASC, "shopapp_product"."price" ASC; args=(); alias=default INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id", "product_id") VALUES (4, 3); args=(4, 3); INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id", "product_id") VALUES (4, 8); args=(4, 8); INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id", "product_id") VALUES (4, 6); args=(4, 6); INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id", "product_id") VALUES (4, 5); args=(4, 5); INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id", "product_id") VALUES (4, 7); args=(4, 7); INSERT
		OR IGNORE INTO "shopapp_order_products" ("order_id",
		 "product_id") VALUES (4,
		 9); args=(4,
		 9);UPDATE "shopapp_order" SET "delivery_address" = 'ul Pupkina, d 8', "promocode" = 'SALE123', "created_at" = '2023-07-02 14:21:12.085026', "user_id" = 1, "receipt" = ''
WHERE "shopapp_order"."id" = 4; args=('ul Pupkina, d 8', 'SALE123', '2023-07-02 14:21:12.085026', 1, '', 4); alias=default Created order Order object (4)