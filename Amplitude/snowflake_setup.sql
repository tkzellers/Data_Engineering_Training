use database til_data_engineering;

use schema amplitude_des6_tkz_schema;


--Creating a storage integration. This is the 'bridge' that allows a secure connection between
--AWS and Snowflake. The storage integration will sit inside the External Stage. 
CREATE STORAGE INTEGRATION amplitude_des6_tkz_storageintegration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::192699161875:role/amplitude-des6-tkz-snowflakerole' --Make a role on AWS for snowflake, and then put its ARN here.
  STORAGE_ALLOWED_LOCATIONS = ('s3://amplitude-des6-tkz-bucket'); --Point it to the bucket (these could be multiple, with commas)

DESC INTEGRATION amplitude_des6_tkz_storageintegration; --MUST do this
    --From the description results you need rows 5 and 7 to create a Trust Policy definition for the Trust Relationship in your AWS Snowflake Role
    --the STORAGE_AWS_IAM_USER_ARN value will go in the "Principal {AWS: }" spot
    --the STORAGE_AWS_EXTERNAL_ID value will go in the "sts:ExternalId":" spot

--Create the External Stage
CREATE OR REPLACE STAGE amplitude_des6_tkz_stage
    URL = 's3://amplitude-des6-tkz-bucket/python_export/' --include the folder if need be, as here
    STORAGE_INTEGRATION = amplitude_des6_tkz_storageintegration
    FILE_FORMAT = (
        TYPE = 'JSON'
        STRIP_OUTER_ARRAY = FALSE
    );

create or replace table amplitude_raw
    (
    json variant,
    filename string,
    last_modified datetime
    );

copy into amplitude_raw
    from(
        select
            $1, --how we reference the json
            metadata$filename,
            metadata$file_last_modified --see docs, metadata names are fixed by Snowflake
        from @amplitude_des6_tkz_stage
    )
    file_format = (type = 'JSON')
    ;

--Check to see how many files of json were uploaded
select distinct
    filename
from amplitude_raw;

select
    concat((split(concat(split(filename,'_')[2],(' '), split(filename,'_')[3]), '#')[0]),':00:00') :: datetime as event_date, 
    --this ridiculousness gets me a datetime out of the json filename
    count(*) as number_of_events
from amplitude_raw
group by filename
order by 1 asc;