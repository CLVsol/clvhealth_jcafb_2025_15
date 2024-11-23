BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "clv_partner_entity_contact_information_pattern" (
	"id"	INTEGER,
	"name"	TEXT,
	"street"	TEXT,
	"street_number"	TEXT,
	"street_number2"	TEXT,
	"street2"	TEXT,
	"notes"	TEXT,
	"active"	INTEGER
);
CREATE TABLE IF NOT EXISTS "clv_partner_entity_street_pattern" (
	"id"	INTEGER,
	"street"	TEXT,
	"street2"	TEXT,
	"notes"	TEXT,
	"active"	INTEGER
);
CREATE TABLE IF NOT EXISTS "clv_patient" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"code"	TEXT,
	"gender"	TEXT,
	"birthday"	TEXT,
	"phase_id"	INTEGER,
	"phase"	TEXT,
	"address_name"	TEXT,
	"street_name"	TEXT,
	"street"	TEXT,
	"street_number"	TEXT,
	"street2"	TEXT,
	"street_number2"	TEXT,
	"zip"	TEXT,
	"city_id"	INTEGER,
	"city"	TEXT,
	"state_id"	INTEGER,
	"country_state"	TEXT,
	"country_id"	INTEGER,
	"country"	TEXT,
	"mobile"	TEXT,
	"email"	TEXT,
	"category_ids"	TEXT,
	"categories"	TEXT,
	"marker_ids"	TEXT,
	"markers"	TEXT,
	"tag_ids"	TEXT,
	"tags"	TEXT,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_category" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_marker" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_tag" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_phase" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_company" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_country" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"code"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_partner" (
	"id"	INTEGER,
	"name"	TEXT,
	"type"	TEXT,
	"street_name"	TEXT,
	"street"	TEXT,
	"street_number"	TEXT,
	"street_number2"	TEXT,
	"street2"	TEXT,
	"district"	TEXT,
	"active"	INTEGER
);
CREATE TABLE IF NOT EXISTS "res_users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"partner_id"	INTEGER,
	"company_id"	INTEGER,
	"parent_id"	INTEGER,
	"tz"	TEXT,
	"lang"	TEXT,
	"country_id"	INTEGER,
	"login"	TEXT,
	"password"	TEXT,
	"active"	INTEGER,
	"image_1920"	TEXT,
	PRIMARY KEY("id")
);
CREATE UNIQUE INDEX "idx_clv_patient_code" ON "clv_patient" (
	"code"	ASC
);
CREATE INDEX "idx_clv_patient_name" ON "clv_patient" (
	"name"	ASC
);
COMMIT;
