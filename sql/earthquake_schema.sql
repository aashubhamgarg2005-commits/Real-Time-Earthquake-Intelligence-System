-------------------------------------------
-- 0. CREATE TABLES FOR EARTHQUAKE DATA
-------------------------------------------

-- 1. CREATE DIM LOCATION TABLE

CREATE TABLE IF NOT EXISTS dim_location(
    location_id BIGINT PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    region VARCHAR(200)
);

-- 2. CREATE DIM TIME TABLE

CREATE TABLE IF NOT EXISTS dim_time(
    time_id BIGINT PRIMARY KEY,
    event_time TIMESTAMP WITH TIME ZONE,
    year INT ,
    month INT ,
    day INT,
    hour INT,
    minute INT,
    second INT,
    day_of_weak INT,
    day_of_year INT
);

-- 3. CREATE DIM EVENT TYPE TABLE

CREATE TABLE IF NOT EXISTS dim_event_type(
    event_type_id BIGINT PRIMARY KEY,
    event_type VARCHAR(50),
    magnitude_type VARCHAR(50)
);

-- 4. CREATE DIM SOURCE TABLE

CREATE TABLE IF NOT EXISTS dim_source(
    source_key BIGINT PRIMARY KEY,
    source_id VARCHAR(50),
    source_catalog VARCHAR(100),
    author VARCHAR(50)
);


-- 5. CREATE FACT TABLE

CREATE TABLE IF NOT EXISTS fact_earthquake(
    event_id VARCHAR(50) PRIMARY KEY,
    location_id BIGINT,
    time_id BIGINT,
    event_type_id BIGINT,
    source_key BIGINT,
    magnitude DOUBLE PRECISION,
    depth_km DOUBLE PRECISION,
    last_update TIMESTAMP WITH TIME ZONE,
    event_action VARCHAR(50),
    magnitude_category VARCHAR(50),
    depth_category VARCHAR(50),

    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    FOREIGN KEY (event_type_id) REFERENCES dim_event_type(event_type_id),
    FOREIGN KEY (source_key) REFERENCES dim_source(source_key)
);

-------------------------------
-- 6. CREATE INDEXES
-------------------------------

-- 7. CREATE INDEX FOR LOCATION

CREATE INDEX IF NOT EXISTS idx_location_id 
ON fact_earthquake(location_id);

-- 8. CREATE INDEX FOR TIME

CREATE INDEX IF NOT EXISTS idx_time_id
ON fact_earthquake(time_id);

-- 9. CREATE INDEX FOR LAST UPDATE

CREATE INDEX IF NOT EXISTS idx_fact_last_update
ON fact_earthquake(last_update)
