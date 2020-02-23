#!/bin/bash

## psql_columns.txt must be like:
# table1 COLUMN1 COLUMN2
# table2 COLUMN3
# table3 COLUMN1 COLUMN2 COLUMN3
# etc.
#
# pc_chartoint is function 'function_char2int'. See nikistochka/sql_scripts.
  
input="./psql_columns.txt"
database=postgres
while IFS= read -r line
do
  IFS=' ' read -r -a array <<< "$line"
  for column in "${array[@]: 1:10}"
  do
    echo "I'm working with: ${array[0]}:${column}"
    echo "Creating ${column}_NEW in ${array[0]} table"
    psql -U postgres -d "${database}" -c "ALTER TABLE public.${array[0]}
ADD COLUMN \"${column}_NEW\" character varying COLLATE pg_catalog."default"" &&
    echo "Done!" &&
    echo "Copying data from ${column} to ${column}_NEW in public.${array[0]} table" &&
    psql -U postgres -d "${database}" -c "UPDATE public.${array[0]} SET \"${column}_NEW\"=\"${column}\"" &&
    echo "Done!" &&
    echo "Changing TYPE for ${column}_NEW in ${array[0]} table" &&
    psql -U postgres -d "${database}" -c "ALTER TABLE public.${array[0]} ALTER COLUMN \"${column}_NEW\" TYPE integer USING pc_chartoint(\"${column}_NEW\");" &&
    echo "DONE! `date`"
    echo "_________________________________________________________"
  done
done < "$input"
