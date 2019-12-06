
MOM6_namelists(){

# MOM6 namelists generation

cd $DATA

  cat >> input.nml <<EOF

&MOM_input_nml
  output_directory = 'MOM6_OUTPUT/',
  input_filename = 'r'
  restart_input_dir = 'INPUT/',
  restart_output_dir = 'MOM6_RESTART/',
  parameter_filename = 'INPUT/MOM_input',
                       'INPUT/MOM_override'
/
EOF

echo "Creating MOM_input and MOM_override"

# Copy the ice template into run directory
cp $SCRIPTDIR/MOM_input_template tmp1
# Replace values in template
sed -i -e "s;DT_THERM_MOM6;${DT_THERM_MOM6};g" tmp1
sed -i -e "s;DT_DYNAM_MOM6;${DT_DYNAM_MOM6};g" tmp1
# Rename to proper input ice input name
mv tmp1 $DATA/INPUT/MOM_input

cp $SCRIPTDIR/MOM_override $DATA/INPUT/MOM_override

echo "$(cat input.nml)"
}
