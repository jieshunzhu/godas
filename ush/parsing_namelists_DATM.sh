#! /bin/sh
##### 
## "parsing_namelist_FV3.sh"
## This script writes namelist for FV3 model
##
## This is the child script of ex-global forecast,
## writing namelist for FV3
## This script is a direct execution.
#####

DATM_namelists(){

cd $DATA

cat > diag_table << EOF
MOM6 Forecast
$SYEAR $SMONTH $SDAY $SHOUR 0 0
EOF
cat $DIAG_TABLE >> diag_table

cp $SCRIPTDIR/data_table.IN $DATA/data_table

# Copy the ice template into run directory
cp $SCRIPTDIR/datm_data_table.IN tmp1
# Replace values in template
#sed -i -e "s;SOMEVAR;${SOMEVAR};g" tmp1

# Rename to proper input ice input name
mv tmp1 $DATA/datm_data_table

cat > input.nml <<EOF

&fms_nml
  clock_grain = 'ROUTINE'
  clock_flags='NONE'
  domains_stack_size = ${domains_stack_size:-5000000}
  stack_size =0
  $fms_nml
/
EOF

echo "$(cat input.nml)"
}
