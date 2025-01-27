CREATE TABLE specialization (
id 				INTEGER,
name			VARCHAR2(50),
PRIMARY KEY (id)
);

CREATE TABLE internal_doctor (
id 			 	INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
specialization 	INTEGER NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE external_doctor (
id 				INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
street			VARCHAR2(50),
postcode		VARCHAR2(10),
city	 		VARCHAR2(50),
specialization	INTEGER NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE diagnosis (
code	 		INTEGER,
text 			VARCHAR2(100),
specialization	INTEGER NOT NULL,
PRIMARY KEY (code),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE patient (
id				INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
birthdate		DATE,
street			VARCHAR2(50),
postcode		VARCHAR2(10),
city	 		VARCHAR2(50),
PRIMARY KEY (id)
);
 
CREATE TABLE visit (
v_number 		INTEGER,
v_date			DATE,
internal_doctor INTEGER NOT NULL,
external_doctor INTEGER NOT NULL,
patient 		INTEGER NOT NULL,
PRIMARY KEY (v_number),
FOREIGN KEY (internal_doctor) REFERENCES internal_doctor,
FOREIGN KEY (external_doctor) REFERENCES external_doctor,
FOREIGN KEY (patient) REFERENCES patient
);



CREATE TABLE report (
visit 			INTEGER,
diagnosis 		INTEGER,
PRIMARY KEY (visit, diagnosis),
FOREIGN KEY (visit) REFERENCES visit,
FOREIGN KEY (diagnosis) REFERENCES diagnosis
);


CREATE TABLE repeatable_prescription (
issue_date                          DATE,
patient 		                    INTEGER,
quantity                            INTEGER,
times_presc_can_be_used             INTEGER,
interval_day_period_between_presc   INTEGER,
prescription_name                   VARCHAR2(50),
direction_of_use                    VARCHAR2(500),
medication_strength                 VARCHAR2(10),
internal_doctor                     INTEGER,
dosage_form                         VARCHAR2(50),
PRIMARY KEY (issue_date, prescription_name),
FOREIGN KEY (patient) REFERENCES patient,
FOREIGN KEY (internal_doctor) REFERENCES internal_doctor
);



CREATE TABLE prescription (
issue_date                          DATE,
patient 		                    INTEGER,
quantity                            INTEGER,
prescription_name                   VARCHAR2(50),
direction_of_use                    VARCHAR2(500),
medication_strength                 VARCHAR2(10),
internal_doctor                     INTEGER,
dosage_form                         VARCHAR2(50),
PRIMARY KEY (issue_date, prescription_name),
FOREIGN KEY (patient) REFERENCES patient,
FOREIGN KEY (internal_doctor) REFERENCES internal_doctor
);


