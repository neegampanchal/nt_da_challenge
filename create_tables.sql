
CREATE TABLE IF NOT EXISTS "customer" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "orders" (
	"id"	INTEGER NOT NULL,
	"customer_id"	INTEGER NOT NULL,
	"total_price"	NUMERIC NOT NULL,
	"created_at"	TEXT NOT NULL,
	"currency_rate"	NUMERIC NOT NULL,
	CONSTRAINT "pk_order_id" PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "line_items" (
	"id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"sku"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"price"	TEXT NOT NULL,
	"order_id"	INTEGER NOT NULL,
	CONSTRAINT "pk_line_item" PRIMARY KEY("id","order_id","product_id"),
	CONSTRAINT "fk_order_id" FOREIGN KEY("order_id") REFERENCES "orders"("id")
);