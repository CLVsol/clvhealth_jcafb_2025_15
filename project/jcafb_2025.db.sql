BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "clv_global_tag" (
"id" INTEGER,
  "name" TEXT,
  "description" TEXT,
  "color" INTEGER,
  "notes" INTEGER,
  "active" INTEGER
);
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
	"district"	TEXT,
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
	"code"	TEXT DEFAULT NULL,
	"notes"	TEXT DEFAULT NULL,
	"active"	INTEGER,
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
	"zip"	TEXT,
	"city_id"	INTEGER,
	"city"	TEXT,
	"state_id"	INTEGER,
	"country_state"	INTEGER,
	"country_id"	INTEGER,
	"country"	TEXT,
	"active"	INTEGER
);
CREATE TABLE IF NOT EXISTS "res_users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"partner_id"	INTEGER,
	"partner"	TEXT,
	"company_id"	INTEGER,
	"company"	TEXT,
	"parent_id"	INTEGER,
	"parent"	TEXT,
	"tz"	TEXT,
	"lang"	TEXT,
	"country_id"	INTEGER,
	"country"	TEXT,
	"login"	TEXT,
	"password"	TEXT,
	"active"	INTEGER,
	"image_1920"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "survey_question" (
	"id"	INTEGER,
	"title"	TEXT,
	"code"	TEXT,
	"description"	TEXT,
	"parameter"	TEXT,
	"survey_id"	INTEGER,
	"survey"	TEXT,
	"sequence"	INTEGER,
	"is_page"	INTEGER,
	"page_id"	INTEGER,
	"page"	TEXT,
	"question_type"	TEXT,
	"matrix_subtype"	TEXT,
	"column_nb"	TEXT,
	"comments_allowed"	INTEGER,
	"comments_message"	TEXT,
	"comment_count_as_answer"	INTEGER,
	"validation_required"	INTEGER,
	"validation_email"	TEXT,
	"validation_length_min"	INTEGER,
	"validation_length_max"	INTEGER,
	"validation_min_float_value"	REAL,
	"validation_max_float_value"	REAL,
	"validation_min_date"	TEXT,
	"validation_max_date"	TEXT,
	"validation_min_datetime"	TEXT,
	"validation_max_datetime"	TEXT,
	"validation_error_msg"	TEXT,
	"constr_mandatory"	INTEGER,
	"constr_error_msg"	TEXT,
	"is_conditional"	INTEGER,
	"triggering_question_id"	INTEGER,
	"triggering_question"	TEXT,
	"triggering_answer_id"	INTEGER,
	"triggering_answer"	TEXT
);
CREATE TABLE IF NOT EXISTS "survey_question_answer" (
"id" INTEGER,
  "question_id" INTEGER,
  "question" TEXT,
  "matrix_question_id" INTEGER,
  "matrix_question" TEXT,
  "sequence" INTEGER,
  "value" TEXT,
  "code" TEXT,
  "is_correct" INTEGER,
  "answer_score" REAL
);
CREATE TABLE IF NOT EXISTS "survey_survey" (
	"id"	INTEGER,
	"title"	TEXT,
	"code"	TEXT,
	"description"	TEXT,
	"access_token"	TEXT,
	"phase_id"	INTEGER,
	"phase"	TEXT,
	"users_login_required"	INTEGER,
	"is_attempts_limited"	INTEGER,
	"attempts_limit"	INTEGER,
	"users_can_go_back"	INTEGER,
	"questions_layout"	TEXT,
	"color"	INTEGER,
	"questions_selection"	TEXT,
	"access_mode"	TEXT,
	"session_code"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE UNIQUE INDEX "idx_clv_patient_code" ON "clv_patient" (
	"code"	ASC
);
CREATE INDEX "idx_clv_patient_name" ON "clv_patient" (
	"name"	ASC
);
COMMIT;
